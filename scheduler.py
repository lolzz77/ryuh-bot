from datetime import date, timedelta, datetime
import pytz

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

my_timezone = pytz.timezone('Asia/Singapore')
now = datetime.now()
today_weekday = now.weekday()
first_day_of_week_offset = -today_weekday

monday = now + timedelta(days=first_day_of_week_offset+7)
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


schedule_weekend_msg = '''\
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
{all_cannot}\
'''.format( thursday=thursday, 
            friday=friday, 
            saturday=saturday, 
            sunday=sunday,
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
            all_cannot=all_cannot)

schedule_weekday_msg = '''\
Monday Night - **{monday}**

{mon_10_pm}
{mon_11_pm}

Tuesday Night - **{tuesday}**

{tue_10_pm}
{tue_11_pm}

Wednesday Night - **{wednesday}**

{wed_10_pm}
{all_cannot}\
'''.format( monday=monday, 
            tuesday=tuesday,
            wednesday=wednesday,
            mon_10_pm=mon_10_pm,
            mon_11_pm=mon_11_pm,
            tue_10_pm=tue_10_pm,
            tue_11_pm=tue_11_pm,
            wed_10_pm=wed_10_pm,
            all_cannot=all_cannot)