#!/bin/bash

# make executable file
pyinstaller --name main.out --onefile main.py
# write my current version into text.file
echo $(git describe) >| dist/VERSION.md
# move the executable file out to current directory
mv dist/main.out .
# run it
./main.out