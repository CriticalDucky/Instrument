import sys
import json
import led_admin

json_string = sys.argv[1]

data = json.loads(json_string)
\

for idx, val in enumerate(data):
    strip.setPixelColor(idx, Color(val[0], val[1], val[2]))

strip.show()
