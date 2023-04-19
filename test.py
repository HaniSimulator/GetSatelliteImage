import requests
import urllib.request
from UTMtoGeo import utmToLatLng

#API parameters
apiKey = "aTrzS6yVWcHMaimAczjk6IVrX3iobhyc"
area = "Delta25"
zoom = 15   #  mode1:15   mode2:17
distanceDiffkm = 7.4   #  mode1:7.4   mode2:1.8
wSize = 1850             #  mode1:1850   mode2:1950
hSize = 1850
getType = 'map'   #sat-hyb-map
edgeHalfLen = 30    #Half len of edge in kilometer
secNum = 9

# lat&long Center
latBaseCenter = 31.9
longBaseCenter = 54.96

# UTM center parameter of top left part
xtl = 711853    #X of center top left part
ytl = 3575913   #Y of center top left
zone = 39
isNorthHemi = True



latDiff1000m = 0.0090148
longDiff1000m = 0.0106304


lattlCorner = latBaseCenter + edgeHalfLen * latDiff1000m
longtlCorner = longBaseCenter - edgeHalfLen * longDiff1000m

latbrCorner = latBaseCenter - edgeHalfLen * latDiff1000m
longbrCorner = longBaseCenter + edgeHalfLen * longDiff1000m

print('lattlCorner : ' + str(lattlCorner))
print('longtlCorner : ' + str(longtlCorner))
print('latbrCorner : ' + str(latbrCorner))
print('longbrCorner : ' + str(longbrCorner))


# lat&long corner top left
# lattlCorner = 32.2358
# longtlCorner= 53.39392

# lat&long center top left
lattlCenter = lattlCorner - latDiff1000m * distanceDiffkm / 2
longtlCenter= longtlCorner + longDiff1000m * distanceDiffkm / 2

latlong = [0.1,0.1]
for xc in range(0,secNum):
    for yc in range(0,secNum):
        try:
            # calc by UTM
            # x = xtl + (xc * 7600)
            # y = ytl - (yc * 7600)
            # latlong = utmToLatLng(zone, x, y, isNorthHemi)

            # calc by Geo
            latlong = [lattlCenter - (yc * latDiff1000m * distanceDiffkm) , longtlCenter + (xc * longDiff1000m * distanceDiffkm) ]

            # print("latlong: ", latlong)
            address = "https://www.mapquestapi.com/staticmap/v4/getplacemap?location=" + str(latlong[0]) + "%2C" + str(latlong[1]) + "&size=" + str(wSize) + "%2C" + str(hSize) + "&type=" + getType + "&zoom=" + str(zoom) + "&imagetype=png&scalebar=false&key=" + apiKey
            print(address)
            name = area + '_' + getType + '_' + 'Y_' +  str(yc) + '_' + 'X_' +  str(xc) + "_Lat_" + str(latlong[0]) + "_Long_" + str(latlong[1])
            print(name)

            # Method1
            # urllib.request.urlretrieve(address, name +'.png')
        except:
            print('Error along get :' + area + '_' + 'Y_' +  str(yc) + '_' + 'X_' +  str(xc))
        #Method2
        # response = requests.get(address)
        # file = open(name +'.png', "wb")
        # file.write(response.content)
        # file.close()




