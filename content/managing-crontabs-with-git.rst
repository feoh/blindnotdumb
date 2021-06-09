Managing crontabs with Git
##########################
:date: 2010-10-20 15:24
:author: cpatti
:category: Geekery
:tags: administration, bourne shell, cron, crontab, Git, management, SCM, script, shell, sysadmin, UNIX
:slug: managing-crontabs-with-git
:status: published

April 2012 Update: Nowadays we use\ `Chef <https://www.opscode.com/chef/>`__\ from Opscode solutions to manage our crontabs, and just about everything else in our enterprise infrastructure. It rocks :)

Time and time again over the years I've dealt with the same problem - who took a random pot shot at some critical user's crontab file and deleted things without asking?

| 
| All of a sudden, someone realizes that some function that's supposed to run every so often has stopped, and in fact hasn't run in weeks. You sniff around - nope, no errors in the logs, in fact no logs at all!

Then you look at the crontab for the user in question and realize that the lines invoking the script that used to be there have either been deleted or commented out. What the? Who did this, and why?

Git to the rescue! With the help of a simple Bourne Shell script, you can keep your crontab managed so you'll not just be able to see who changed what and when, but if you have the Git hook installed to send mail on commits, you can be notified of those changes in real time. Pretty cool eh? :)

Since crontab has no built in security precautions other than requiring you to BE the user whose crontab you're submitting, we can't lock people not using this script out, but if you tell everyone that changes they make outside of the script may be summarily ignored and overwritten (and put something to that effect in the comment block at the top of your crontab) you should be in good shape. The script will compare what's in Git with what's currently installed in cron, and if there are discrepancies it will give you a chance to cleanly exit and resolve them, or allow you to ignore them and roll forward with editing and submitting what's in Git.

Here's the script. It assumes you're running as your regular user and have sudo privs to the user whose crontab you wish to edit. It also assumes you've created a Git repository called system_cron.git

To set it up, just edit reponame and gitrepo to appropriate values for your site and copy the script to somewhere folks can access it in their PATH.

To use it, just invoke it with the user whose crontab you want to edit - for example:``edit_crontab.sh build``

::

   #!/bin/sh

   export tmpdir="/tmp/crontab_$$"

   if [ $# -lt 1 ]; then
       echo "Usage: $0 "
       exit 1;
   fi

   if [ -z "$EDITOR" ]; then
       echo "No editor found.  Using vim."
       export EDITOR="/usr/bin/vim"
   fi

   crontab_user=$1

   crontab_file="`uname -n`-$crontab_user.crontab"
   echo "crontab_file=$crontab_file"

   git clone /home/git/system_cron.git $tmpdir
   cd $tmpdir

   sudo -u $crontab_user crontab -l > currcrontab_$$

   if [ $? -ne 0 ]; then
       echo "sudo to user $crontab_user failed! Do you have sudo privs?"
       exit 1;
   fi

   diff=`diff currcrontab_$$ $crontab_file`

   if [ $? -ne 0 ]; then
       echo "Currently running crontab for $crontab_user differs from Git!"
       echo "Here are the differences:"
       echo $diff
       echo 
       echo -n "Continue editing / submitting what's in Git? (Y/n): "
       read yesorno
       if [ "$yesorno" != "Y" ]; then
           echo "Very good.  Exiting." 
           exit 1;        
       fi
   fi

   $EDITOR $crontab_file

   echo "Here are your changes:"
   git diff --exit-code $crontab_file
   if [ $? -eq 0 ]; then
       echo "No changes made.  Not submitting anything."
       exit 1;
   fi

   echo -n "Submit these changes to Git and crontab? (Y/n): "
   read yesorno
   if [ "$yesorno" != "Y" ]; then
       echo "Your changes are in $tmpdir/system_cron/$crontab_file."
       echo "Please clean up this directory when you're done with it."
       exit 1;        
   else
       git commit $crontab_file
       if [ $? -ne 0 ]; then
           echo "There was a problem committing your crontab to git!"
           exit 1;
       fi
       git push origin master
       if [ $? -ne 0 ]; then
           echo "There was a problem pushing your crontab to git!"
           exit 1;
       fi

       # if we made it this far. We're all good.  Install that puppy!

       echo "Installing your crontab."
       sudo -u $crontab_user crontab $crontab_file
       if [ $? -ne 0 ]; then
           echo "ERROR! Your changes were NOT installed! Something went wrong."
           exit 1;
       fi
   fi

   echo "Cleaning up tmp directory..."
   #rm -rf $tmpdir
