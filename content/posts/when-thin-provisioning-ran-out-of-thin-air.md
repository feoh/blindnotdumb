---
title: "When Thin Provisioning Ran Out of Thin Air: A Homelab Postmortem"
slug: when-thin-provisioning-ran-out-of-thin-air
date: '2026-08-10T08:02:05-04:00'
author: Chris Patti
draft: true
description: Infrastructure Engineering In The Age of Ultron
tags:
- homelab
- proxmox
- linkding
- incident-response
- postmortem
- storage
- selfhosting
---

I woke up to two unpleasant facts:

1. My [Linkding](https://linkding.link/) server was down.
2. The web interface for the Proxmox host running it was also unavailable.

My first hunch was that the server had run out of disk space. That hunch was right, but the interesting part was *how* it had run out.

The physical filesystem was not full. The SSD had not failed. The Linkding database was not corrupt.

Instead, Proxmox's LVM thin pool had reached **100% utilization**, even though the volume group still had nearly 15 GiB sitting unused beside it. Automatic pool growth was effectively disabled, discard was not enabled for the VMs, and nothing was warning me as the pool approached the cliff.

Thin provisioning had successfully hidden the problem right up until it couldn't.

This is the postmortem.

## Executive summary

On August 9, 2026, the `pve/data` LVM thin pool on my Proxmox server reached 100%. Linux first put the pool into queued-I/O mode, then switched it into error-I/O mode. Linkding eventually stopped responding over the network. By the time I investigated the next morning, both Linkding and the Proxmox web interface were unavailable from where I was sitting.

I rebooted the host and deleted an obsolete, stopped VM because I suspected storage pressure. The VMs had already begun their automatic startup, but deleting that VM restored roughly 18.5 GiB of desperately needed thin-pool headroom.

Further investigation found three underlying prevention failures:

- the pool had less physical capacity than its VMs had actually consumed;
- automatic extension was disabled despite free extents being available;
- discard/TRIM and capacity alerting were absent.

Recovery risk was compounded by the lack of a dependable off-host Linkding backup. No Linkding data loss was detected. Both SQLite databases passed integrity checks, and a full official Linkding backup was successfully written to my NAS.

## Impact

- Linkding was unavailable over the tailnet for roughly 21 hours, based on Tailscale's last-seen data. That is an upper-bound proxy, not an exact application-availability measurement.
- The Proxmox management interface was unavailable when I began investigating.
- Normal management access returned after a clean host reboot.
- The IRC VM and Linkding VM each had a short, planned restart during remediation.
- No confirmed data loss occurred.
- The Linkding application and databases were healthy after recovery.

For a personal homelab this was annoying rather than catastrophic. But Linkding contains years of accumulated bookmarks, so the absence of a tested, automated, off-host backup made the incident much more serious than it needed to be.

## The root cause in one sentence

I treated thin provisioning as a substitute for capacity management, while the system had no automatic growth, reclamation, or alerting path to stop a completely predictable storage exhaustion event.

## The five whys

### 1. Why was Linkding unavailable?

The Linkding VM stopped serving the application and disappeared from the tailnet during the incident window.

The Proxmox management path was also unavailable when I started investigating, so I could not initially inspect or operate the VM through the normal web interface.

### 2. Why did the VM stop operating normally?

Its virtual disk was backed by an LVM thin pool that had run out of physical data extents.

At 05:04 on August 9, the kernel logged that the pool had reached its low-water mark and was switching to out-of-data-space queued-I/O mode. At 05:05 it switched to error-I/O mode.

At that point, virtual disk capacity still looked generous *inside* the guest, but the host could no longer reliably provide new blocks underneath it.

### 3. Why did the thin pool run out of physical extents?

The VMs had collectively consumed all 65.49 GiB assigned to the pool.

One stopped VM alone retained about 18.5 GiB of real thin-pool allocation. Linkding's nominal 124 GiB disk had consumed about 27.4 GiB in the pool, even though the guest filesystem reported far more free space. Deleted blocks inside the guests were not being returned to LVM.

A stopped VM is not an empty VM, and free space inside a guest is not necessarily free space on the hypervisor.

### 4. Why didn't the pool grow, reclaim space, or warn me?

All three safety mechanisms were missing or ineffective:

- `thin_pool_autoextend_threshold` was set to `100`, which disables useful preemptive extension.
- The volume group had 14.75 GiB free, but LVM was not configured to use it before the pool filled.
- `discard=on` was not enabled for the VM disks, so guest TRIM could not reclaim thin-pool blocks.
- No alert fired at 75%, 85%, or even 100% utilization.

The server had room to save itself. It simply had not been told to do so.

### 5. Why were those controls missing?

Because the homelab evolved one useful VM at a time rather than from an explicit storage reliability design.

I had created oversized thin virtual disks because doing so was convenient. I had not paired that convenience with a documented capacity budget, warning thresholds, automated pool growth, or block reclamation.

Nothing individually looked reckless. Together, those omissions formed a complete failure path. The separate lack of a restore-tested backup did not cause the outage, but it sharply increased the potential consequences.

## Root cause versus contributing factors

The root cause was **a storage capacity-control failure around the Proxmox thin pool**.

Deleting the obsolete VM fixed the immediate pressure, but the existence of that VM was not the root cause. If I had deleted it months earlier, some other workload could eventually have consumed the same unguarded pool.

A separate NFS configuration problem also appeared during recovery. The Linkding VM mounted configuration data from my NAS using its Tailscale name. That mount timed out during boot and left the guest in a degraded state. It did not cause the original storage exhaustion, and Linkding's live database was on local VM storage, but it made recovery slower and more fragile.

The physical SSD does not currently appear to have caused the incident. SMART reported healthy status, zero reallocated sectors, and zero interface CRC errors. It is an old SSD, however, and age is not a backup strategy.

## What went well

### My first hunch was useful

I suspected disk pressure and deleted a stopped VM I no longer needed. That recovered enough space to get the system operating again.

It was not the complete fix, but it was a good emergency move.

### The host rebooted cleanly

The logs show an orderly, requested reboot rather than a kernel panic or sudden power loss. Both production VMs returned automatically.

### Linkding's data survived

Before making further storage changes, I copied transactionally consistent SQLite backups off the VM. The main and task databases both passed `PRAGMA integrity_check`.

I then used Linkding's official `full_backup` management command to create a complete archive containing the database and assets. The resulting ZIP contained 3,882 entries, passed a full archive test, and received a SHA-256 checksum.

### The remediation was deliberately boring

Changes were made in a safe order:

1. capture rollback copies;
2. add pool headroom;
3. enable automatic growth and monitoring;
4. establish the NAS-backed application backup;
5. enable discard;
6. restart one VM at a time;
7. verify each application before touching the next VM;
8. run TRIM and check for storage errors.

No VM was force-stopped.

## What went poorly

### Detection was entirely human

The first alert was me noticing that services were gone. The machine knew the pool was nearly full long before I did.

### The emergency control plane shared the failure domain

The web interface I normally use to manage the VMs lived on the same host experiencing the storage incident. Tailscale was also part of my normal access path. When both looked unavailable, diagnosis became needlessly awkward even though the host's LAN interface eventually remained reachable.

### I had backups, but not *the* backup I needed

There were old ad hoc files in Linkding's data directory, but no current, scheduled, validated, off-host full backup. A file named `backup.zip` is not a backup program.

### Thin provisioning obscured the real budget

The configured virtual disks totalled far more than the physical SSD could ever hold. That is normal for thin provisioning, but only when monitoring and reclamation make the oversubscription explicit and controlled.

Mine did not.

## Corrective actions

The immediate controls are now in place: more pool headroom, automatic extension, five-minute capacity monitoring, discard/TRIM, resilient LAN-based NAS mounts, and a daily validated Linkding backup retained off-host.

The monitor is configured to send warning and critical state changes through the host's mail system, although external delivery still needs to be tested.

The durable work remains: upgrade the old operating systems, conduct a Linkding restore drill, add full-VM backups, and either add physical capacity or migrate important VMs before growth consumes the reserve.

The exact controls and their status are listed in Appendix G.

## The lesson

Thin provisioning is a promise that capacity will probably be available later.

It is not capacity.

If I want the flexibility of oversized virtual disks, I also need all of the machinery that makes that flexibility safe: thresholds, automatic extension, discard, monitoring, off-host backups, and restore tests.

The most important remediation was not deleting a VM or adding five GiB to a logical volume. It was turning an invisible cliff into a managed limit.

---

## Appendix A: Detailed timeline

All host timestamps are Eastern Daylight Time unless otherwise noted. Guest logs used UTC.

| Time | Event |
| --- | --- |
| Aug 9, 05:04:31 | Device Mapper reports the thin pool low-water mark and switches to out-of-data-space queued-I/O mode. |
| Aug 9, 05:04:36 | LVM reports `pve-data-tpool` at 100%. |
| Aug 9, 05:05:33 | Device Mapper switches the thin pool to error-I/O mode. |
| Aug 9, approximately 09:14 | Tailscale later reports this as Linkding's last-seen time before recovery. |
| Aug 10, 06:48 | A clean, requested Proxmox reboot begins. |
| Aug 10, 06:49 | The host boots successfully. |
| Aug 10, 06:50 | The IRC and Linkding VMs begin automatic startup. |
| Aug 10, 06:51 | I delete obsolete VM 102, recovering roughly 18.5 GiB of thin-pool allocation. |
| Aug 10, 06:54 | Transactionally consistent Linkding SQLite backups are copied off the VM and pass integrity checks. |
| Aug 10, 07:07 | The thin pool is extended by 5 GiB; automatic extension is set to 80%/10%. |
| Aug 10, 07:08 | Linkding's NFS mounts are changed to the NAS LAN address and verified. |
| Aug 10, 07:11 | The first scheduled-style official Linkding full backup begins. |
| Aug 10, 07:12 | The 456.8 MB full backup completes and passes ZIP and SHA-256 verification. |
| Aug 10, 07:15 | The IRC VM is gracefully restarted with discard enabled; The Lounge returns HTTP 200. |
| Aug 10, 07:16 | The Linkding VM is gracefully restarted with discard enabled; Linkding returns healthy. |
| Aug 10, 07:17 | Linkding guest TRIM completes. Pool utilization falls to 45.73%. |
| Aug 10, 07:20 | The recurring Proxmox thin-pool capacity monitor is enabled and reports normal state. |

## Appendix B: Storage evidence

### Thin-pool state before recovery

The pool was 65.49 GiB and 100% consumed.

Approximate per-VM physical thin-pool consumption before VM 102 was removed:

| VM | Role | Virtual disk | Thin volume data percentage | Approximate consumed blocks |
| --- | --- | ---: | ---: | ---: |
| 100 | IRC / The Lounge | 32 GiB | 47.28% | 15.1 GiB |
| 101 | Docker template, stopped | 100 GiB | 4.42% | 4.4 GiB |
| 102 | Obsolete multihack VM, stopped | 200 GiB | 9.27% | 18.5 GiB |
| 104 | Linkding | 124 GiB | 22.10% | 27.4 GiB |

Those values sum to approximately the entire 65.49 GiB pool.

The key detail is that the thin volumes' *virtual* sizes totalled 456 GiB on a host with a 128 GB SSD. Oversubscription itself was intentional. Oversubscription without guardrails was the mistake.

### State after each major action

| Stage | Pool size | Pool utilization | VG free space |
| --- | ---: | ---: | ---: |
| Incident | 65.49 GiB | 100% | 14.75 GiB |
| After deleting VM 102 | 65.49 GiB | 71.70% | 14.75 GiB |
| After extending the pool | 70.49 GiB | 66.61% | 9.75 GiB |
| After Linkding TRIM | 70.49 GiB | 45.73% | 9.75 GiB |

Linkding's thin-volume data percentage fell from 22.10% to 10.23% after discard was activated and TRIM ran.

### Automatic extension policy

Before:

```text
thin_pool_autoextend_threshold = 100
thin_pool_autoextend_percent = 20
```

After:

```text
thin_pool_autoextend_threshold = 80
thin_pool_autoextend_percent = 10
```

The remaining 9.75 GiB in the volume group is a buffer, not a long-term capacity plan. It can support approximately one automatic 10% pool extension at the current size.

## Appendix C: Data protection evidence

### Emergency SQLite copies

The main Linkding database and task database were copied using SQLite's online backup API, not a raw copy of live database files.

Results:

| Database | Size | Integrity result |
| --- | ---: | --- |
| Main database | 4,907,008 bytes | `ok` |
| Task database | 1,421,312 bytes | `ok` |

### Official Linkding full backup

The recurring job runs Linkding's own management command:

```text
python manage.py full_backup <destination>
```

The first archive had these properties:

| Property | Value |
| --- | --- |
| Filename | `linkding-full-20260810T111153Z.zip` |
| Size | 456,755,511 bytes |
| ZIP entries | 3,882 |
| ZIP integrity | No bad members |
| Checksum | SHA-256 sidecar generated and verified |
| Permissions | Owner read/write only |

The job stages the archive under a partial filename, validates it, atomically renames it, writes the checksum, and only then prunes archives beyond the newest 30.

It also checks that the destination is backed by the expected NAS NFS export. If the NAS is unavailable, the job fails rather than writing hundreds of megabytes into an unmounted local directory.

## Appendix D: NFS recovery issue

The Linkding guest originally mounted its container configuration directory using the NAS's Tailscale DNS name.

During recovery that mount waited 90 seconds, timed out, and left the guest in a degraded systemd state. The Linkding container still returned because Docker retained the existing container definition and the live Linkding data directory was local to the VM.

Both required NAS exports now use the NAS's LAN address with these behavioral properties:

- network filesystem classification;
- boot continues if the NAS is unavailable;
- systemd automount triggers access on demand;
- mount attempts have a bounded timeout;
- normal NFS hard-mount data semantics remain in place.

After a full VM reboot, both mounts resolved over NFSv4 from the LAN and the guest reported `running`, not `degraded`.

## Appendix E: Hardware evidence

The host uses a 128 GB SATA SSD with 47,854 power-on hours at the time of the incident.

SMART evidence:

| Attribute | Result |
| --- | --- |
| Overall self-assessment | Passed |
| Reallocated sectors | 0 |
| UDMA CRC errors | 0 |
| Temperature | 48°C during inspection |

The boot log contained an ATA command timeout while querying an unsupported log page, but no corresponding reallocated sectors, uncorrectable sectors, filesystem errors, or sustained interface errors were found.

That does not make the drive immortal. It does mean there is no current evidence that hardware failure caused this incident.

## Appendix F: Confidence and open questions

### High-confidence findings

- The thin pool reached 100%.
- Device Mapper entered queued-I/O and then error-I/O mode.
- Automatic extension was effectively disabled.
- Free volume-group extents existed during the incident.
- VM discard was disabled.
- Deleting VM 102 reclaimed the amount of space expected from its thin-volume usage.
- Linkding databases and the official full backup passed integrity checks.

### Medium-confidence findings

- Thin-pool exhaustion caused Linkding's loss of service. The timing and storage evidence strongly support this, but the guest did not record a neat single application error saying "the hypervisor has run out of thin extents."
- Tailscale's last-seen timestamp approximates the service outage duration, but it is not a proper availability probe.

### Not proven

- Thin-pool exhaustion directly stopped the Proxmox web proxy. The proxy runs from the host root filesystem, which was not full. The interface recovered after a clean reboot, and the management-path failure occurred during the same incident window, but the logs do not prove a single causal chain between those two facts.
- External delivery of the new warning email has not yet been tested.
- A full restore from the new Linkding archive has not yet been performed.

## Appendix G: Corrective-action register

### Completed

- Expanded the thin pool from 65.49 GiB to 70.49 GiB.
- Configured automatic extension at 80% utilization in 10% increments.
- Added a five-minute monitor configured to send warning and critical state changes through the host's mail system.
- Enabled `discard=on` for all remaining VM disks.
- Restarted the IRC and Linkding VMs gracefully so discard became active.
- Ran TRIM in the Linkding guest, reducing thin-pool utilization from 66.65% to 45.73%.
- Confirmed the IRC guest's weekly `fstrim` timer is enabled.
- Moved NFS mounts from Tailscale addressing to the NAS's LAN address.
- Made the NFS mounts non-blocking at boot with systemd automount and bounded mount timeouts.
- Installed a daily official Linkding full backup at 03:15 UTC.
- Configured retention for the newest 30 validated archives.
- Required the backup job to prove that the NAS export is mounted before writing, preventing an NFS failure from silently filling local storage.
- Added ZIP validation, atomic publication, SHA-256 checksums, and restrictive file permissions.

### Remaining

- Upgrade the old Proxmox and Ubuntu releases during a separate maintenance window.
- Test external delivery of the new capacity alert, not merely the local monitor state.
- Perform a documented Linkding restore drill from the NAS archive.
- Decide whether to add physical storage or migrate important VMs to a larger pool before growth consumes the remaining reserve.
- Add a guest agent to the IRC VM so operations such as on-demand TRIM can be verified centrally.
- Establish full VM backups in addition to application-level Linkding backups.
