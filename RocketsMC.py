import serial as pySerial
import matplotlib.pyplot as plt
import json
import simplekml
import time
import sys
import os

def plotData(data):
    fig.suptitle('Stanford SSI IREC 2018 Groundstation')
    times.append(time.time()-startTime)
    altitude.append(data[u'altitude'])
    battery.append(data[u'battery'])
    vsense1.append(data[u'vsense1'])
    vsense2.append(data[u'vsense2'])
    rssi.append(data[u'rssi'])
    gps_lock.append(data[u'gps_lock'])
    charges_blown.append(data[u'charges_blown'])
    max_t = times[len(times)-1]

    alt_ax = plt.subplot(2,4,1)
    alt_ax.set_title('Altitude (m)')
    alt_ax.set_ylabel('Altitude (m)')
    alt_ax.set_xlabel('Time (s)')
    alt_gr = plt.plot(times,altitude,'r')[0]
    #alt_ax.xla

    batt_ax = plt.subplot(2,4,2)
    batt_ax.set_title('Skybass Battery Voltage (V)')
    batt_ax.set_ylabel('Voltage (V)')
    batt_ax.set_xlabel('Time (s)')
    batt_gr = plt.plot(times,battery,'r')[0]

    v1_ax = plt.subplot(2,4,3)
    v1_ax.set_title('Stratologger Battery Voltage (V)')
    v1_ax.set_ylabel('Voltage (V)')
    v1_ax.set_xlabel('Time (s)')
    v1_gr = plt.plot(times,vsense1,'r')[0]

    v2_ax = plt.subplot(2,4,4)
    v2_ax.set_title('Raven Battery Voltage (V)')
    v1_ax.set_ylabel('Voltage (V)')
    v1_ax.set_xlabel('Time (s)')
    v2_gr = plt.plot(times,vsense2,'r')[0]

    rssi_ax = plt.subplot(2,4,5)
    rssi_ax.set_title('RSSI')
    rssi_ax.set_ylabel('RSSI')
    rssi_ax.set_xlabel('Time (s)')
    rssi_gr = plt.plot(times,rssi,'r')[0]

    gps_ax = plt.subplot(2,4,6)
    gps_ax.set_title('GPS Lock Enable')
    gps_ax.set_ylabel('GPS Enable?')
    gps_ax.set_xlabel('Time (s)')
    gps_gr = plt.plot(times,gps_lock,'b')[0]

    charges_ax = plt.subplot(2,4,7)
    charges_ax.set_title('Charges Enable')
    gps_ax.set_ylabel('Charges Blown?')
    gps_ax.set_xlabel('Time (s)')
    charges_gr = plt.plot(times,charges_blown,'b')[0]

    plt.draw()

    plt.pause(5)
def main():
    serial = pySerial.Serial("COM26", 115200)

    startTime = time.time()
    altitude = [0]
    rssi = [0]
    vsense1 =[0]
    vsense2 = [0]
    battery = [0]
    charges_blown = [0]
    gps_lock = [0]

    fig = plt.figure()

    times = [time.time()-startTime]

    min_t = times[0]

    gpsPath = []

    kml = simplekml.Kml()
    kmlPath = kml.newlinestring(name="Redshift Path")
    kmlPath.altitudemode = simplekml.AltitudeMode.absolute
    kmlPath.linestyle.color = simplekml.Color.red
    kmlPath.linestyle.width = 2

    kmlPoint = kml.newpoint(name="Redshift")
    kmlPoint.altitudemode = simplekml.AltitudeMode.absolute

    filename = 'Logs/'+time.strftime("%Y-%m-%d-%H.%M.%S") + ".log"
    print(filename)

    with open(filename, 'w') as file:
        file.write("Opening Log: "+filename+"\n")


        while True:
            rawData = serial.readline()
            rawData = rawData.decode('utf-8')
            try:
                packet = json.loads(rawData)
                packet["groundTime"] = time.asctime()
                packet['lat'] = packet['lat'] + 30.0
                packet['lon'] = packet['lon'] - 130.0
                print(packet)
                rawData = json.dumps(packet)
                file.write(rawData+"\n")
                location = [(packet['lon'], packet['lat'], packet['altitude'])]
                kmlPoint.coords = location
                print(kmlPoint.coords)
                gpsPath += location
                kmlPath.coords = gpsPath
                kmlPoint.timestamp.when = time.asctime()
                kml.save("gps.kml")
                plotData(packet)
            except json.decoder.JSONDecodeError:
                print("Parse Error")
                file.write(rawData+"\n")
                print(rawData)
            except:
                print("Unexpected error:", sys.exc_info()[0])

try:
    main()
except KeyboardInterrupt:
    pass
