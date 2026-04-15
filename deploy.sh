#!/bin/sh

uv run zensical build && aws s3 cp --recursive site s3://blindnotdumb --profile personal && aws cloudfront create-invalidation --distribution-id E9NOZU9W34CCS --paths "/*" --profile personal
