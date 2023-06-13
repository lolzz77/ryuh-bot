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
monday = monday.strftime("%d %b")
first_day_of_week_offset+=1

# days=first_day_of_week_offset+7 == next tuesday
tuesday = now + timedelta(days=first_day_of_week_offset+7)
tuesday = tuesday.strftime("%d %b")
first_day_of_week_offset+=1

# days=first_day_of_week_offset+7 == next wednesday
wednesday = now + timedelta(days=first_day_of_week_offset+7)
wednesday = wednesday.strftime("%d %b")
first_day_of_week_offset+=1

# days=first_day_of_week_offset == this week's thursday
thursday = now + timedelta(days=first_day_of_week_offset)
thursday = thursday.strftime("%d %b")
first_day_of_week_offset+=1

# days=first_day_of_week_offset == this week's friday
friday = now + timedelta(days=first_day_of_week_offset)
friday = friday.strftime("%d %b")
first_day_of_week_offset+=1

# days=first_day_of_week_offset == this week's saturday
saturday = now + timedelta(days=first_day_of_week_offset)
saturday = saturday.strftime("%d %b")
first_day_of_week_offset+=1

# days=first_day_of_week_offset == this week's sunday
sunday = now + timedelta(days=first_day_of_week_offset)
sunday = sunday.strftime("%d %b")

# Emoji
emoji_cat_angery = '<:cat_angery:814753563854503966>' # From Jumping Sushi server

# e8_pm = emoji 8 pm, variable cannot start with number
e8_pm = "🐱"
e9_pm = "🐶"
e10_pm = "🐰"
e11_pm = "🐹"
e12_am = "🐻"
e_wednesday = "3️⃣"
e_thursday = "4️⃣"
e_friday = "5️⃣"
e_saturday = "6️⃣"
e_sunday = "7️⃣"
e_monday = "1️⃣"
e_tuesday = "2️⃣"
all_cannot = "🙃"

emoji_time_dict = {
    e8_pm : "[8pm]",
    e9_pm : "[9pm]",
    e10_pm : "[10pm]",
    e11_pm : "[11pm]",
    e12_am : "[12am]",
}

emoji_day_dict = {
    e_wednesday : None,
    e_thursday : None,
    e_friday : None,
    e_saturday : None,
    e_sunday : None,
    e_monday : None,
    e_tuesday : None,
    all_cannot : None,
}

schedule_message = '''\
{e8_pm} = 8pm
{e9_pm} = 9pm
{e10_pm} = 10pm
{e11_pm} = 11pm
{e12_am} = 12am

:three: - Wednesday **({wednesday})**
:four: - Thusrday **({thursday})**
:five: - Friday **({friday})**
:six: - Saturday **({saturday})**
:seven: - Sunday **({sunday})**
:one: - Monday **({monday})**
:two: - Tuesday **({tuesday})**

{all_cannot} - Probably OT\
'''.format( e8_pm=e8_pm,
            e9_pm=e9_pm,
            e10_pm=e10_pm,
            e11_pm=e11_pm,
            e12_am=e12_am,
            wednesday=wednesday,
            thursday=thursday,
            friday=friday, 
            saturday=saturday, 
            sunday=sunday,
            monday=monday, 
            tuesday=tuesday,
            all_cannot=all_cannot)
