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
emoji_cat_angery = '<:cat_angery:814753563854503966>' # From Jumping Sushi server


reaction_mapping = {
    "🐱" : ["Curseday",     "8pm"],
    "🐹" : ["Curseday",     "9pm"],
    "🦁" : ["Curseday",     "10pm+"],
    "🐶" : ["Friday",       "8pm"],
    "🐻" : ["Friday",       "9pm"],
    "🐯" : ["Friday",       "10pm"],
    "🐰" : ["Friday",       "11pm"],
    "🐼" : ["Friday",       "12am"],
    "🐷" : ["Saturday",     "8pm"],
    "🐮" : ["Saturday",     "9pm"],
    "🐔" : ["Saturday",     "10pm"],
    "🐻‍❄️" : ["Saturday",     "11pm"],
    "🦉" : ["Saturday",     "12am"],
    "🐣" : ["Sunday",       "8pm"],
    "🐩" : ["Sunday",       "9pm"],
    "🐵" : ["Sunday",       "10pm+"],
    "1️⃣" : ["I can do on Monday", None],
    "2️⃣" : ["I can do on Tuesday", None],
    "🙃" : ["Probably OT", None]
}

# Get the list of keys. In other words, get the emoji
reaction_mapping_keys = list(reaction_mapping)

# Construct string in this format
# mon_10_pm = "🐠 - 10pm"
thu_8_pm    = reaction_mapping_keys[0] + " - " + reaction_mapping[reaction_mapping_keys[0]][1]
thu_9_pm    = reaction_mapping_keys[1] + " - " + reaction_mapping[reaction_mapping_keys[1]][1]
thu_10_pm   = reaction_mapping_keys[2] + " - " + reaction_mapping[reaction_mapping_keys[2]][1]
fri_8_pm    = reaction_mapping_keys[3] + " - " + reaction_mapping[reaction_mapping_keys[3]][1]
fri_9_pm    = reaction_mapping_keys[4] + " - " + reaction_mapping[reaction_mapping_keys[4]][1]
fri_10_pm   = reaction_mapping_keys[5] + " - " + reaction_mapping[reaction_mapping_keys[5]][1]
fri_11_pm   = reaction_mapping_keys[6] + " - " + reaction_mapping[reaction_mapping_keys[6]][1]
fri_12_am   = reaction_mapping_keys[7] + " - " + reaction_mapping[reaction_mapping_keys[7]][1]
sat_8_pm    = reaction_mapping_keys[8] + " - " + reaction_mapping[reaction_mapping_keys[8]][1]
sat_9_pm    = reaction_mapping_keys[9] + " - " + reaction_mapping[reaction_mapping_keys[9]][1]
sat_10_pm   = reaction_mapping_keys[10] + " - " + reaction_mapping[reaction_mapping_keys[10]][1]
sat_11_pm   = reaction_mapping_keys[11] + " - " + reaction_mapping[reaction_mapping_keys[11]][1]
sat_12_am   = reaction_mapping_keys[12] + " - " + reaction_mapping[reaction_mapping_keys[12]][1]
sun_8_pm    = reaction_mapping_keys[13] + " - " + reaction_mapping[reaction_mapping_keys[13]][1]
sun_9_pm    = reaction_mapping_keys[14] + " - " + reaction_mapping[reaction_mapping_keys[14]][1]
sun_10_pm   = reaction_mapping_keys[15] + " - " + reaction_mapping[reaction_mapping_keys[15]][1]
mon_time    = reaction_mapping_keys[16] + " - " + reaction_mapping[reaction_mapping_keys[16]][0]
tue_time    = reaction_mapping_keys[17] + " - " + reaction_mapping[reaction_mapping_keys[17]][0]
all_cannot  = reaction_mapping_keys[18] + " - " + reaction_mapping[reaction_mapping_keys[18]][0]

schedule_message = '''\
Curseday - **{thursday}**
{thu_8_pm}
{thu_9_pm}
{thu_10_pm}
{thu_11_pm}
{thu_12_am}

Friday - **{friday}**
{fri_8_pm}
{fri_9_pm}
{fri_10_pm}
{fri_11_pm}
{fri_12_am}

Saturday - **{saturday}**
{sat_11_am}
{sat_12_pm}
{sat_1_pm}
{sat_2_pm}
{sat_3_pm}
{sat_4_pm}
{sat_5_pm}
{sat_6_pm}
{sat_7_pm}
{sat_8_pm}
{sat_9_pm}
{sat_10_pm}
{sat_11_pm}
{sat_12_am}

Sunday - **{sunday}**
Reminder - Guild Skill reset after 12
{sun_11_am}
{sun_12_pm}
{sun_1_pm}
{sun_2_pm}
{sun_3_pm}
{sun_4_pm}
{sun_5_pm}
{sun_6_pm}
{sun_7_pm}
{sun_8_pm}
{sun_9_pm}
{sun_10_pm}
{sun_11_pm}
{sun_12_am}

Monday - **{monday}**
{mon_8_pm}
{mon_9_pm}
{mon_10_pm}
{mon_11_pm}
{mon_12_am}

Tuesday - **{tuesday}**
{tue_8_pm}
{tue_9_pm}
{tue_10_pm}
{tue_11_pm}
{tue_12_am}

Wednesday - **{wednesday}**
{wed_8_pm}
{wed_9_pm}
{wed_10_pm}
{wed_11_pm}
{wed_12_am}

{all_cannot}\
'''.format( 
thursday=thursday, 
friday=friday, 
saturday=saturday, 
sunday=sunday,
monday=monday, 
tuesday=tuesday,
wednesday=wednesday,
thu_8_pm=thu_8_pm,
thu_9_pm=thu_9_pm,
thu_10_pm=thu_10_pm,
fri_8_pm=fri_8_pm,
fri_9_pm=fri_9_pm,
fri_10_pm=fri_10_pm,
fri_11_pm=fri_11_pm,
fri_12_am=fri_12_am,
sat_8_pm=sat_8_pm,
sat_9_pm=sat_9_pm,
sat_10_pm=sat_10_pm,
sat_11_pm=sat_11_pm,
sat_12_am=sat_12_am,
sun_8_pm=sun_8_pm,
sun_9_pm=sun_9_pm,
sun_10_pm=sun_10_pm,
mon_time=mon_time,
tue_time=tue_time,
all_cannot=all_cannot
)
