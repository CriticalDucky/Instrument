import sys
import json
import time
start_time = time.time()
import led_admin
print(f"Imported led_admin in {time.time() - start_time} seconds")

json_string = sys.argv[1]

data = json.loads(json_string)

led_admin.give_data(data)
