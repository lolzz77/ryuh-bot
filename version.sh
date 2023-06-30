#!/bin/bash

# To re-version
# intended for main branch
# after you merge with 'dev' branch
# i will manually re-tag the version
# then, the source code version needs to re-version as well
# this script will re-version it

# Currently, you want git tags and your source code version match
# The only way to do this is to update your source code
# commit
# only then you do the git tag thing
# cannot terbalik, because everytime you commit, a new tag with your commit hash is created
# resulting your current tag and your source code version not match

# count how many param passed in
# Only need to pass one, that is the release tag version you want
# e.g: v1.1
if [ $# != 1 ]
then
	echo "Invalid number of param"
	exit
fi

# empty the file
> module/version.py

# rewrite the new version into the file
echo "version = '$1'" >> module/version.py

# commit & push
git add module/version.py
git commit -m "VERSION"
git push

# now you do the git tag
git tag -a $1

# push the new tag
git push --tags

