# argv.py
import sys
import json

json_file = json.loads(sys.argv[1])
#shelf = get_db()
print(json_file["chipid"])
#devices = []
#devices.append(shelf[key_chipid])

#print(devices)