# ryuh-bot

## preparation
1. create .env file that contains your bot token
2. Remember to setup 'post-commit' script for your git repo

## Setup
To find out what libraries needed to install

pip3 install pipreqs (pip requirements)

pipreqs /path/to/project

Then it will create requirements.txt for you

Before you install the requirement.txt, create virtual environment first
python3 -m venv virtual_env
source virtual_env/bin/activate

Then to intall the libraries, run
pip3 install -r requirements.txt


To run the bot, 
depending on what is your python version
To install python, run

apt-get install python3

Now, you installed python3, so you use python3 command

To run the bot,
python3 main.py


To build an executable python file
pip3 install pyinstaller
pyinstaller --onefile main.py
outputfile will be in /dist/main.out

How to create executable python file and run on docker
git clone
create .env file
run pyinstaller
run .out file

How to create bash script that make your file
touch make.sh
[input code]
chmod u+x make.sh
./make.sh

Then, in docker, you can put in .bashrc, so that everytime you start container, it will run
But, probably this is not a good idea
once the docker run, dont know how to stop it unless u edit the bashrc, and restart the whole container
if u dont, your vs code cannot start your bot, because container is already started it
# run ryuh bot
# cannot do like './~/ryuh-bot/main' it has a lot environment errors
cd ~/ryuh-bot
./main


If you get error after built, cannot run
Then you tried to do code change in this vs code,
and rebuild again and realize same error
rmb, your vs code currently is opening file from your local computer
whereas ur docker, is opening another file within that docker
2 different folders/repo you're editting



------------------------
![image](https://github.com/lolzz77/ryuh-bot/assets/61287457/ed6004bb-a0bf-4aa0-b09b-6767b460afd4)

![image](https://github.com/lolzz77/ryuh-bot/assets/61287457/bd54da48-edc7-4f20-9fce-f9356ac7e1b8)

------------------------
When you run, you will realize '__pycache__' is generated
this is generated whereever ur source file is, including all sub source file
if you put sub soruce file in /dirA/,
dirA will have '__pycache__'