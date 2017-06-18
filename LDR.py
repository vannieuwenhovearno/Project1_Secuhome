import RPi.GPIO as GPIO
import spidev
import time

import mysql.connector as mc

time.sleep(30)

ledPin = 21

GPIO.setmode(GPIO.BCM) # Zet de pinmode op Broadcom SOC.
GPIO.setwarnings(False) # Zet waarschuwingen uit.
GPIO.setup(ledPin, GPIO.OUT) # Zet de GPIO pin als uitgang.

spi = spidev.SpiDev()
spi.open(0,0)

def read_spi(channel):
    spidata = spi.xfer2([1,(8+channel)<<4,0])
    return ((spidata[1] & 3) << 8) + spidata[2]

sensorDetect = False
try:
    while not sensorDetect:
        channeldata = read_spi(0)
        LastStatus = GPIO.input(ledPin)
        if channeldata > 1000 :
            GPIO.output(ledPin, 1) # Zet de LED aan.
        else:
            GPIO.output(ledPin, 0) # Zet de LED uit.
            sensorDetect = False
        time.sleep(0.1)

        currentStatus = GPIO.input(ledPin)

        if LastStatus != currentStatus:
            if currentStatus == 1:
                connection = mc.connect(host="localhost", user="Arno", passwd="Arnoenbobby1998.98", db="db_project_secuhome")
                cursor = connection.cursor()
                cursor.execute("INSERT INTO datalichtout(DatumIN, TijdIN,Aan,lichtenbuiten_IDLichtenbuiten,systeem_IDSysteem) VALUES (CURDATE(), CURTIME(), 1, 1, 1)")
                connection.commit()
                print("geimporteerd")
            else:
                print("no import")
        else:
            print("same state")

except KeyboardInterrupt:
    spi.close()
    GPIO.cleanup() # GPIO netjes afsluiten.

