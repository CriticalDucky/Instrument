import subprocess
import json

def write(data):
    data = json.dumps(data)

    command = ["python3", "scripts/LED_admin.py", data]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("Error:", e)

write([[i, i, i] for i in range(136)])