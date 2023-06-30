#!/bin/bash

# To re-version
# intended for main branch
# after you merge with 'dev' branch
# i will manually re-tag the version
# then, the source code version needs to re-version as well
# this script will re-version it


# Just re-run the hook script
./.git/hooks/post-commit
