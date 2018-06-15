import serial as pySerial
import json
import simplekml
import time
import sys


def main():
    serial = pySerial.Serial("COM26", 115200)

    gpsPath = []

    kml = simplekml.Kml()
    kmlPath = kml.newlinestring(name="Redshift Path")
    kmlPath.altitudemode = simplekml.AltitudeMode.absolute
    kmlPath.linestyle.color = simplekml.Color.red
    kmlPath.linestyle.width = 2

    kmlPoint = kml.newpoint(name="Redshift")
    kmlPoint.altitudemode = simplekml.AltitudeMode.absolute

    filename = time.strftime("%Y-%m-%d-%H.%M.%S") + ".log"
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