import sys
import json
import led_admin

json_string = sys.argv[1]

data = json.loads(json_string)

led_admin.give_data(data)
