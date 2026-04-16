#!/bin/sh
set -exo pipefail

if command -v hugo >/dev/null 2>&1; then
  HUGO=hugo
elif [ -x ./.tools/hugo/hugo ]; then
  HUGO=./.tools/hugo/hugo
else
  echo "hugo not found" >&2
  exit 1
fi

$HUGO build --cleanDestinationDir
python3 scripts/generate_legacy_feeds.py
aws s3 cp --recursive public s3://blindnotdumb --profile personal
aws cloudfront create-invalidation --distribution-id E9NOZU9W34CCS --paths "/*" --profile personal
