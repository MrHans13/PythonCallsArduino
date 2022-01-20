import os
import time
import requests

# import subprocess as subp

ssid1 = 'http://192.168.43.228'
ssid2 = 'http://192.168.0.186'
ssid = ssid1
dcwlan = 0
rstarttime = ''


def steckdoseEins():
    os.system('curl ' + ssid + '/R1')


def steckdoseZwei():
    rdata = requests.get(ssid + "/R2")
    data = open('.S2stat.txt', 'w')
    data.write(rdata.text)
    data.close()


def steckdoseDrei():
    os.system('curl ' + ssid + '/R3')


def steckdosenAlle():
    os.system('curl ' + ssid + '/alles')


def steckdosenDataW():
    global dcwlan
    now = str(time.asctime())
    rdata = requests.get(ssid + "/data")
    global rstarttime
    daten = open('messdaten WLAN.txt', 'w')

    if dcwlan == 0:
        rstarttime = str(time.asctime())
        daten.write("*****************************************\n"
                    "***   Programm wurde neu gestartet.   ***\n"
                    "*****************************************\n")
    dcwlan += 1
    daten.write("***** Statusdaten ESP8266 *****\n")
    daten.write("letzter Neustart der App: " + str(rstarttime) + "\n")

    if 0 < dcwlan < 10:
        daten.write("App-Messung Nr. " + str(dcwlan) + "         " + now + "\n")
    if dcwlan >= 10:
        daten.write("App-Messung Nr. " + str(dcwlan) + "        " + now + "\n")

    daten.write("ESP8266-")
    daten.writelines(rdata.text)

    daten.close()


def wDatenLoeschen():
    global dcwlan
    daten = open('messdaten WLAN.txt', 'w')
    daten.write("")
    daten.close()
    dcwlan = 0
