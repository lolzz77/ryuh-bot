# Cake emoji
# <:pepe_birthday:1087764773615194212>
# 🍰
# <a:cake2:1087764775754280961>
# 🎂
# <a:cake1:1087763631346810912>
# 🧁

from datetime import date, timedelta, datetime
import pytz

# Resets every monday
# if you call it on monday, the schedule on monday will be next week's one

# Bossing resets on Thursday 12am
# So, mon, tues, wed date calculation will be next week's
# Thus, fri, sat, sun will be this week's date

# datetime.datetime.today().weekday()
# output:
# 0 = Monday
# 6 = Sunday
#
# date.today().strftime("%d/%b/%y")
# date format = dd/Jan/23

# not sure if this works, that is, i scare the .weekday() still uses default timezone
# this can be seen if you datetime.now(ytz.timezone('Asia/Singapore')).today()
# perhaps .today() is similar to .now() and it overwrites

SCHEDULE_PATH = './schedule/'

my_timezone = pytz.timezone('Asia/Singapore')
now = datetime.now(my_timezone)
today_weekday = now.weekday()
# Get negative value, for calculation
first_day_of_week_offset = -today_weekday

# days=first_day_of_week_offset+7 == next monday
monday = now + timedelta(days=first_day_of_week_offset+7)
monday = monday.strftime("%d/%b/%y")
first_day_of_week_offset+=1

# days=first_day_of_week_offset+7 == next tuesday
tuesday = now + timedelta(days=first_day_of_week_offset+7)
tuesday = tuesday.strftime("%d/%b/%y")
first_day_of_week_offset+=1

# days=first_day_of_week_offset+7 == next wednesday
wednesday = now + timedelta(days=first_day_of_week_offset+7)
wednesday = wednesday.strftime("%d/%b/%y")
first_day_of_week_offset+=1

# days=first_day_of_week_offset == this week's thursday
thursday = now + timedelta(days=first_day_of_week_offset)
thursday = thursday.strftime("%d/%b/%y")
first_day_of_week_offset+=1

# days=first_day_of_week_offset == this week's friday
friday = now + timedelta(days=first_day_of_week_offset)
friday = friday.strftime("%d/%b/%y")
first_day_of_week_offset+=1

# days=first_day_of_week_offset == this week's saturday
saturday = now + timedelta(days=first_day_of_week_offset)
saturday = saturday.strftime("%d/%b/%y")
first_day_of_week_offset+=1

# days=first_day_of_week_offset == this week's sunday
sunday = now + timedelta(days=first_day_of_week_offset)
sunday = sunday.strftime("%d/%b/%y")

# Emoji
# From Jumping Sushi server
emoji_cat_angery = '<:cat_angery:814753563854503966>' 
# From my server
emoji_monkey_how_1 = '<:how1:1138852944519897159>'
emoji_monkey_how_2 = '<:how2:1138852939025354782>'

# For printing out the schedule message
schedule_message = ''

reaction_mapping = {
    "🐱" : ["Curseday",     "8pm"],
    "🐹" : ["Curseday",     "9pm"],
    "🦁" : ["Curseday",     "10pm+"],
    "🐶" : ["Friday",       "8pm"],
    "🐻" : ["Friday",       "9pm"],
    "🐯" : ["Friday",       "10pm"],
    "🐰" : ["Friday",       "11pm"],
    "🐼" : ["Friday",       "12am"],
    "🦜" : ["Saturday",     "Afternoon"],
    "🐷" : ["Saturday",     "8pm"],
    "🐮" : ["Saturday",     "9pm"],
    "🐔" : ["Saturday",     "10pm"],
    "🐻‍❄️" : ["Saturday",     "11pm"],
    "🦉" : ["Saturday",     "12am"],
    "🐸" : ["Sunday",       "Afternoon"],
    "🐣" : ["Sunday",       "8pm"],
    "🐩" : ["Sunday",       "9pm"],
    "🐵" : ["Sunday",       "10pm+"],
    "1️⃣" : ["Monday",       "I can do on Monday"],
    "2️⃣" : ["Tuesday",      "I can do on Tuesday"],
}
