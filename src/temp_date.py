import datetime
import json

a = datetime.datetime.now()
new = datetime.datetime(a.year,a.month,a.day,a.hour,a.minute,a.second)
formatted_datetime = new.isoformat()
json_datetime = json.dumps(formatted_datetime)
print(json_datetime)
