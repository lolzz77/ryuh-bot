# ryuh-bot

To find out what libraries needed to install

pip install pipreqs (pip requirements)

pipreqs /path/to/project

Then it will create requirements.txt for you

Then to intall the libraries, run

pip install -r requirements.txt


To run the bot, 
depending on what is your python version
To install python, run

apt-get install python3

Now, you installed python3, so you use python3 command

To run the bot,
python3 main.py


To build an executable pytohn file
pip3 install pyinstaller
pyinstaller --onefile main.py
outputfile will be in /dist/main.out
