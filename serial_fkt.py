import serial
try:
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
except: pass

def serialData():
    rData = open("messdaten Serial.txt", "w")

    ser.write(str.encode('s'))

    daten = ser.readline()
    daten = daten.decode('utf8')
    rData.writelines(daten)

    rData.close()
    ser.close()
    ser.open()
