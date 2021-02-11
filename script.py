
ledPin = 7
iAmOnRaspberry = True
debug = False

if iAmOnRaspberry:
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
import time
import json
import traceback

try:
    read = open("led.json")
    read_str = str(read.read())
    read_data = json.loads(read_str)

    read_data['acceso'] = not read_data['acceso']
    if iAmOnRaspberry:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(ledPin, GPIO.OUT)
        GPIO.output(ledPin, read_data['acceso'])

    if debug:
        print(read_data['acceso'])

    with open('led.json', 'w') as ledFile:
        ledFile.write(json.dumps(read_data, indent = 4, sort_keys=True))
except:
    traceback.print_exc()
    if iAmOnRaspberry:
        GPIO.cleanup()