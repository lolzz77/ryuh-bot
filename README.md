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

------------------------
![image](https://github.com/lolzz77/ryuh-bot/assets/61287457/ed6004bb-a0bf-4aa0-b09b-6767b460afd4)

![image](https://github.com/lolzz77/ryuh-bot/assets/61287457/bd54da48-edc7-4f20-9fce-f9356ac7e1b8)



------------------------
Install NLTK

pip3 install nltk
python3
import nltk
nltk.download()
# download 'brown' package
# verify that it is downlaoded
from nltk.corpus import brown
brown.words()

# Now download the rest of the packages
nltk.download('punkt')
nltk.download('wordnet')

