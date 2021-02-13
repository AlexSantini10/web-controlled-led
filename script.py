
ledPin = 7
iAmOnRaspberry = False
debug = False

ledState = False

import mysql.connector

if iAmOnRaspberry:
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ledPin, GPIO.OUT)
    GPIO.output(ledPin, ledState)

import time
import json
import traceback

def connect():
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "5ATL",
        passwd = "sistemi",
        database = "led"
    )

    return mydb

def changeState(state):
    mydb = connect()
    mycursor = mydb.cursor()

    query = f"UPDATE ledtable SET ledState={int(state)}"
    mycursor.execute(query)
    mydb.commit()


try:
    toChange = 0

    changeState(0)

    while True:
        
        mydb = connect()

        mycursor = mydb.cursor()

        query = f"SELECT * FROM ledtable"
        mycursor.execute(query)
        toChange = mycursor.fetchall()
        toChange = toChange[0][0]
        toChange = int(toChange)


        if debug:
            print(toChange)

        if toChange==1:

            if debug:
                print('cambio stato del led')

            ledState = not ledState
            
            query = f"UPDATE ledtable SET toChange=0"
            mycursor.execute(query)
            mydb.commit()

        if iAmOnRaspberry:
            GPIO.output(ledPin, ledState)
            changeState(ledState)

        mydb.close()
        time.sleep(0.2)


except:
    traceback.print_exc()
    if iAmOnRaspberry:
        GPIO.cleanup()