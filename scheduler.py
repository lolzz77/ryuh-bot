from datetime import date, timedelta, datetime
import pytz

# Resets every monday
# if you call it on monday, the schedule on monday will be next week's one

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
first_day_of_week_offset = -today_weekday

monday = now + timedelta(days=first_day_of_week_offset+7)
monday_midnight = monday
monday_midnight = monday_midnight.replace(hour=0, minute=0, second=0, microsecond=0)
monday = monday.strftime("%d/%b/%y")
first_day_of_week_offset+=1

tuesday = now + timedelta(days=first_day_of_week_offset+7)
tuesday = tuesday.strftime("%d/%b/%y")
first_day_of_week_offset+=1

wednesday = now + timedelta(days=first_day_of_week_offset+7)
wednesday = wednesday.strftime("%d/%b/%y")
first_day_of_week_offset+=1

thursday = now + timedelta(days=first_day_of_week_offset)
thursday = thursday.strftime("%d/%b/%y")
first_day_of_week_offset+=1

friday = now + timedelta(days=first_day_of_week_offset)
friday = friday.strftime("%d/%b/%y")
first_day_of_week_offset+=1

saturday = now + timedelta(days=first_day_of_week_offset)
saturday = saturday.strftime("%d/%b/%y")
first_day_of_week_offset+=1

sunday = now + timedelta(days=first_day_of_week_offset)
sunday_before_midnight = sunday
sunday_before_midnight = sunday_before_midnight.replace(hour=23, minute=59, second=59, microsecond=59)
sunday = sunday.strftime("%d/%b/%y")


mon_10_pm = "10pm - 🐠"
mon_11_pm = "11pm - 🐟"
tue_10_pm = "10pm - 🐬"
tue_11_pm = "11pm - 🐳"
wed_10_pm = "10pm - 🐙"

thu_10_pm = "10pm - 🐱"
thu_11_pm = "11pm - 🐶"
fri_10_pm = "10pm - 🐰"
fri_11_pm = "11pm - 🐹"
fri_12_am = "12am - 🐻"
sat_10_pm = "10pm - 🐯"
sat_11_pm = "11pm - 🦁"
sat_12_am = "12am - 🐼"
sun_10_pm = "10pm - 🐷"
sun_11_pm = "11pm - 🐮"

all_cannot = "all cannot - 🙃"


schedule_message = '''\
Thursday Night - **{thursday}**
{thu_10_pm}
{thu_11_pm}

Friday Night - **{friday}**
{fri_10_pm}
{fri_11_pm}
{fri_12_am}

Saturday Night - **{saturday}**
{sat_10_pm}
{sat_11_pm}
{sat_12_am}

Sunday Night - **{sunday}**
{sun_10_pm}
{sun_11_pm}

Monday Night - **{monday}**
{mon_10_pm}
{mon_11_pm}

Tuesday Night - **{tuesday}**
{tue_10_pm}
{tue_11_pm}

Wednesday Night - **{wednesday}**
{wed_10_pm}

{all_cannot}\
'''.format( thursday=thursday, 
            friday=friday, 
            saturday=saturday, 
            sunday=sunday,
            monday=monday, 
            tuesday=tuesday,
            wednesday=wednesday,
            thu_10_pm=thu_10_pm,
            thu_11_pm=thu_11_pm,
            fri_10_pm=fri_10_pm,
            fri_11_pm=fri_11_pm,
            fri_12_am=fri_12_am,
            sat_10_pm=sat_10_pm,
            sat_11_pm=sat_11_pm,
            sat_12_am=sat_12_am,
            sun_10_pm=sun_10_pm,
            sun_11_pm=sun_11_pm,
            mon_10_pm=mon_10_pm,
            mon_11_pm=mon_11_pm,
            tue_10_pm=tue_10_pm,
            tue_11_pm=tue_11_pm,
            wed_10_pm=wed_10_pm,
            all_cannot=all_cannot)
