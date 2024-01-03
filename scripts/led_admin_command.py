import sys
import json
import led_admin
import time

json_string = sys.argv[1]

data = json.loads(json_string)

begin_time = time.time()

led_admin.give_data(data)

end_time = time.time()

print(f'LED update took {end_time - begin_time} seconds')
