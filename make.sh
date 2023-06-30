#!/bin/bash

# make executable file
pyinstaller --onefile main.py
# cd into output folder
cd dist/
# write my current version into text.file
echo $(git describe) >| VERSION.md
cd ../
# move the executable file out to current directory
mv dist/main .
# run it
./main