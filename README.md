# ryuh-bot

![image](https://github.com/lolzz77/ryuh-bot/assets/61287457/ed6004bb-a0bf-4aa0-b09b-6767b460afd4)

![image](https://github.com/lolzz77/ryuh-bot/assets/61287457/bd54da48-edc7-4f20-9fce-f9356ac7e1b8)

# preparation

1. create .env file that contains your bot token
- ```vim .env```
- ```BOT_TOKEN="STRING"```
2. Remember to setup 'post-commit' script for your git repo


# Setup
```apt-get install python3```

```pip3 install pyinstaller```

To find out what libraries needed to install

```pip3 install pipreqs``` (pip requirements)

```pipreqs /path/to/project```

Then it will create requirements.txt for you

Before you install the requirement.txt, create virtual environment first

```apt install python3.10-venv -y```

```python3 -m venv venv_python3```

Then, activate the environment

```source venv_python3/bin/activate```

In case of you're having multiple environment, just activate the one you want

That is, you have `venv_a` and `venv_b`

`venv_a` has installed all packages

`venv_b` has no

Activating `venv_b` then run `python3 main.py` will output error because no module installed

Next, to intall the libraries, run

```pip3 install -r requirements.txt```

To run the bot, 
depending on what is your python version
To install python, run

```apt-get install python3```

Now, you installed python3, so you use python3 command to run the bot

```python3 main.py```

To run debugger in VS Code, you have to make VS code to use your python environment file

```First, install python extension in vscode```

```CTRL + SHIFT + P```

Choose `Python: Create Environemnt`

Choose `venv`

Choose your environment

`Enter interpreter path...` -> `Find` -> `your virtual environment/bin/python3.10`

It will ask to install dependencies, choose `requirements.txt`

Then, status bar below will show progress

To ensure you have selected the correct python interpreter

`CTRL+SHIFT+P` -> `PythonL Seelct Interpreter` -> `select yoru correct virtual environment python interpreter`

To build an executable python file

```pip3 install pyinstaller```

```pyinstaller --onefile main.py```

outputfile will be in 

```/dist/main.out```

How to create bash script that make your file

```touch make.sh```

```input code```

```chmod u+x make.sh```

```./make.sh```

Then, in docker, you can put ```./main``` in .bashrc, so that everytime you start container, it will run the bot

But, probably this is not a good idea
once the docker run, dont know how to stop it unless u edit the bashrc, and restart the whole container

if u dont stop it, your vs code cannot start your bot, because container is already started it

Well, there is one way, in docker terminal or vs code terminal that runs the container, run

```ps aux | grep <executable name>```

```kill <PID>```

Okay, that's how to stop it

Now, this is how you put in .bashrc to run the bot

```
# run ryuh bot
# cannot do like './~/ryuh-bot/main' it has a lot environment errors
cd /workspace/ryuh-bot/
# 'pgrep main' will check if 'main' exe is running
# It will output PID if it is running
# This `if` checks if the command got output
# if no, then run the 'main' exe
# this is to prevent running container/connecting container resulting running the exe multiple times
if ! pgrep main.out > /dev/null
then
        ./main.out
fi
```

If you get error after built, cannot run,

Then you tried to do code change in this vs code,

and rebuild again and realize same error

rmb, your vs code currently is opening file from your local computer

whereas ur docker, is opening another file within that docker

2 different folders/repo you're editting

# Branch
1. `main` branch is for original template
```
DAY1 - @DAY1@
emoji1 - 8pm
emoji2 - 9pm
DAY2 - @DAY2@
emoji1 - 8pm
emoji2 - 9pm
etc
```

2. `main_2` branch is for simpler template
This is decided after we realize we dont need that complex template
We just want pick day, dont care time
```
DAY1 - @DAY1@
DAY2 - @DAY2@
```
Then bot just react emoji 1,2,3,4...