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
    "🐻‍❄️" : ["Monday",       "8pm"],
    "🐨" : ["Monday",       "9pm"],
    "🐠" : ["Monday",       "10pm"],
    "🐟" : ["Monday",       "11pm"],
    "🐸" : ["Tuesday",      "8pm"],
    "🐵" : ["Tuesday",      "9pm"],
    "🐬" : ["Tuesday",      "10pm"],
    "🐳" : ["Tuesday",      "11pm"],
    "🐔" : ["Wednesday",    "8pm"],
    "🐧" : ["Wednesday",    "9pm"],
    "🐙" : ["Wednesday",    "10pm"],
    "🐦" : ["Curseday",     "8pm"],
    "🐤" : ["Curseday",     "9pm"],
    "🐱" : ["Curseday",     "10pm"],
    "🐶" : ["Curseday",     "11pm"],
    "🐣" : ["Friday",       "8pm"],
    "🦆" : ["Friday",       "9pm"],
    "🐰" : ["Friday",       "10pm"],
    "🐹" : ["Friday",       "11pm"],
    "🐻" : ["Friday",       "12am"],
    "🦅" : ["Saturday",     "8pm"],
    "🦉" : ["Saturday",     "9pm"],
    "🐯" : ["Saturday",     "10pm"],
    "🦁" : ["Saturday",     "11pm"],
    "🐼" : ["Saturday",     "12am"],
    "🐩" : ["Sunday",       "8pm"],
    "🐴" : ["Sunday",       "9pm"],
    "🐷" : ["Sunday",       "10pm"],
    "🐮" : ["Sunday",       "11pm"],
    "🙃" : ["Probably OT"]
}

# Get the list of keys. In other words, get the emoji
reaction_mapping_keys = list(reaction_mapping)

# Construct string in this format
# mon_10_pm = "10pm - 🐠"
mon_8_pm    = reaction_mapping[reaction_mapping_keys[0]][1] + " - " + reaction_mapping_keys[0]
mon_9_pm    = reaction_mapping[reaction_mapping_keys[1]][1] + " - " + reaction_mapping_keys[1]
mon_10_pm   = reaction_mapping[reaction_mapping_keys[2]][1] + " - " + reaction_mapping_keys[2]
mon_11_pm   = reaction_mapping[reaction_mapping_keys[3]][1] + " - " + reaction_mapping_keys[3]
tue_8_pm    = reaction_mapping[reaction_mapping_keys[4]][1] + " - " + reaction_mapping_keys[4]
tue_9_pm    = reaction_mapping[reaction_mapping_keys[5]][1] + " - " + reaction_mapping_keys[5]
tue_10_pm   = reaction_mapping[reaction_mapping_keys[6]][1] + " - " + reaction_mapping_keys[6]
tue_11_pm   = reaction_mapping[reaction_mapping_keys[7]][1] + " - " + reaction_mapping_keys[7]
wed_8_pm    = reaction_mapping[reaction_mapping_keys[8]][1] + " - " + reaction_mapping_keys[8]
wed_9_pm    = reaction_mapping[reaction_mapping_keys[9]][1] + " - " + reaction_mapping_keys[9]
wed_10_pm   = reaction_mapping[reaction_mapping_keys[10]][1] + " - " + reaction_mapping_keys[10]
thu_8_pm    = reaction_mapping[reaction_mapping_keys[11]][1] + " - " + reaction_mapping_keys[11]
thu_9_pm    = reaction_mapping[reaction_mapping_keys[12]][1] + " - " + reaction_mapping_keys[12]
thu_10_pm   = reaction_mapping[reaction_mapping_keys[13]][1] + " - " + reaction_mapping_keys[13]
thu_11_pm   = reaction_mapping[reaction_mapping_keys[14]][1] + " - " + reaction_mapping_keys[14]
fri_8_pm    = reaction_mapping[reaction_mapping_keys[15]][1] + " - " + reaction_mapping_keys[15]
fri_9_pm    = reaction_mapping[reaction_mapping_keys[16]][1] + " - " + reaction_mapping_keys[16]
fri_10_pm   = reaction_mapping[reaction_mapping_keys[17]][1] + " - " + reaction_mapping_keys[17]
fri_11_pm   = reaction_mapping[reaction_mapping_keys[18]][1] + " - " + reaction_mapping_keys[18]
fri_12_am   = reaction_mapping[reaction_mapping_keys[19]][1] + " - " + reaction_mapping_keys[19]
sat_8_pm    = reaction_mapping[reaction_mapping_keys[20]][1] + " - " + reaction_mapping_keys[20]
sat_9_pm    = reaction_mapping[reaction_mapping_keys[21]][1] + " - " + reaction_mapping_keys[21]
sat_10_pm   = reaction_mapping[reaction_mapping_keys[22]][1] + " - " + reaction_mapping_keys[22]
sat_11_pm   = reaction_mapping[reaction_mapping_keys[23]][1] + " - " + reaction_mapping_keys[23]
sat_12_am   = reaction_mapping[reaction_mapping_keys[24]][1] + " - " + reaction_mapping_keys[24]
sun_8_pm    = reaction_mapping[reaction_mapping_keys[25]][1] + " - " + reaction_mapping_keys[25]
sun_9_pm    = reaction_mapping[reaction_mapping_keys[26]][1] + " - " + reaction_mapping_keys[26]
sun_10_pm   = reaction_mapping[reaction_mapping_keys[27]][1] + " - " + reaction_mapping_keys[27]
sun_11_pm   = reaction_mapping[reaction_mapping_keys[28]][1] + " - " + reaction_mapping_keys[28]
all_cannot  = reaction_mapping[reaction_mapping_keys[29]][0] + " - " + reaction_mapping_keys[29]

schedule_message = '''\
Curseday Night - **{thursday}**
{thu_8_pm}
{thu_9_pm}
{thu_10_pm}
{thu_11_pm}

Friday Night - **{friday}**
{fri_8_pm}
{fri_9_pm}
{fri_10_pm}
{fri_11_pm}
{fri_12_am}

Saturday Night - **{saturday}**
{sat_8_pm}
{sat_9_pm}
{sat_10_pm}
{sat_11_pm}
{sat_12_am}

Sunday Night - **{sunday}**
{sun_8_pm}
{sun_9_pm}
{sun_10_pm}
{sun_11_pm}

Monday Night - **{monday}**
{mon_8_pm}
{mon_9_pm}
{mon_10_pm}
{mon_11_pm}

Tuesday Night - **{tuesday}**
{tue_8_pm}
{tue_9_pm}
{tue_10_pm}
{tue_11_pm}

Wednesday Night - **{wednesday}**
{wed_8_pm}
{wed_9_pm}
{wed_10_pm}

{all_cannot}\
'''.format( thursday=thursday, 
            friday=friday, 
            saturday=saturday, 
            sunday=sunday,
            monday=monday, 
            tuesday=tuesday,
            wednesday=wednesday,
            thu_8_pm=thu_8_pm,
            thu_9_pm=thu_9_pm,
            thu_10_pm=thu_10_pm,
            thu_11_pm=thu_11_pm,
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
            sun_11_pm=sun_11_pm,
            mon_8_pm=mon_8_pm,
            mon_9_pm=mon_9_pm,
            mon_10_pm=mon_10_pm,
            mon_11_pm=mon_11_pm,
            tue_8_pm=tue_8_pm,
            tue_9_pm=tue_9_pm,
            tue_10_pm=tue_10_pm,
            tue_11_pm=tue_11_pm,
            wed_8_pm=wed_8_pm,
            wed_9_pm=wed_9_pm,
            wed_10_pm=wed_10_pm,
            all_cannot=all_cannot)
