import datetime
from datetime import datetime
from pytz import timezone

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def current_day():
  now_utc = datetime.now(timezone('Asia/Almaty'))
  return days[now_utc.weekday()]
  
def current_time_in_minutes():
  now_utc = datetime.now(timezone('Asia/Almaty'))
  hours = now_utc.strftime('%H')
  minutes = now_utc.strftime('%M')
  return int(hours) * 60 + int(minutes)

def am_to_pm(current_time):
  hours = int(current_time[:2])
  minutes = int(current_time[3:5])
  if 'AM' in current_time:
    return hours * 60 + minutes
  else:
    if (hours < 12):
      hours += 12
    return hours * 60 + minutes
