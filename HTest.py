import requests
import urllib.request
import utm
import numpy as np
import math
import time
from PIL import Image

############################################################################################
############################################################################################

EarthRadius = 6378137
MinLatitude = -85.05112878
MaxLatitude = 85.05112878
MinLongitude = -180
MaxLongitude = 180

def Clip(n,minValue, maxValue):
    return min(max(n, minValue), maxValue)

def MapSize(levelOfDetail):
    return np.uint((int)(256 << levelOfDetail))

def  GroundResolution( latitude,  levelOfDetail):
    latitude = Clip(latitude, MinLatitude, MaxLatitude)
    return math.cos(latitude * math.pi / 180) * 2 * math.pi * EarthRadius / MapSize(levelOfDetail)

def MapScale(latitude, levelOfDetail, screenDpi):
    return GroundResolution(latitude, levelOfDetail) * screenDpi / 0.0254

def LatLongToPixelXY(latitude, longitude, levelOfDetail):
    latitude = Clip(latitude, MinLatitude, MaxLatitude)
    longitude = Clip(longitude, MinLongitude, MaxLongitude)
    x = (longitude + 180) / 360
    sinLatitude = math.sin(latitude * math.pi / 180)
    y = 0.5 - math.log((1 + sinLatitude) / (1 - sinLatitude)) / (4 * math.pi)
    mapSize = MapSize(levelOfDetail)
    pixelX = int(Clip(x * mapSize + 0.5, 0, mapSize - 1))
    pixelY = int(Clip(y * mapSize + 0.5, 0, mapSize - 1))
    return pixelX, pixelY

def PixelXYToLatLong(pixelX, pixelY, levelOfDetail):
    mapSize = MapSize(levelOfDetail)
    x = (Clip(pixelX, 0, mapSize - 1) / mapSize) - 0.5
    y = 0.5 - (Clip(pixelY, 0, mapSize - 1) / mapSize)
    latitude = 90 - 360 * math.atan(math.exp(-y * 2 * math.pi)) / math.pi
    longitude = 360 * x
    return latitude, longitude

################################################################################
################################################################################

#urllib.request.urlretrieve("https://www.mapquestapi.com/staticmap/v4/getplacemap?location=31.645015381132502%2C54.962968826293945&size=1000%2C846&type=sat&zoom=15&imagetype=png&scalebar=false&key=aTrzS6yVWcHMaimAczjk6IVrX3iobhyc", "ali" + '.png')
#exit()

#latCorner_TL = 35.970178
#longCorner_TL = 51.019000000000005
#latCorner_BR = 35.922929
#longCorner_BR= 51.116824

#------ Delta 25
#latCorner_TL = 32.170443999999996
#longCorner_TL = 54.641088
#latCorner_BR = 31.629555999999997
#longCorner_BR= 55.278912
#------------------

#------ Tehran Azadi
latCorner_TL = 35.970178
longCorner_TL = 51.019000000000005
latCorner_BR = 35.42929
longCorner_BR = 51.656824
#------------------

#API parameters
apiKey = "aTrzS6yVWcHMaimAczjk6IVrX3iobhyc"
area = "Delta25"
MapZoom = 15   #  mode1:15   mode2:17
distanceDiffkm = 7.4   #  mode1:7.4   mode2:1.8
wSize = 1000             #  mode1:1850   mode2:1950
hSize = 1000
getType = 'sat'   #sat-hyb-map
edgeHalfLen = 30    #Half len of edge in kilometer
secNum = 9
zone = 39

wSizeOrg = wSize

latlong = [0.1,0.1]
XCorner_TL, YCorner_TL =LatLongToPixelXY(latCorner_TL, longCorner_TL, MapZoom)
XCorner_BR, YCorner_BR =LatLongToPixelXY(latCorner_BR, longCorner_BR, MapZoom)
print ("TL:", XCorner_TL, YCorner_TL)
print ("BR:", XCorner_BR, YCorner_BR)

XImageCap = XCorner_TL
YImageCap = YCorner_TL
YImageCap_Row = YImageCap
yc = 0
xc = 0
XcenIm = 0
YcenIm = 0

dstImage = Image.new('RGB', (XCorner_BR - XCorner_TL, YCorner_BR - YCorner_TL))
print ("FinalImage:", dstImage.size)

while (YImageCap <= YCorner_BR):
    while (XImageCap < XCorner_BR):
        try:
            YImageCap = YImageCap_Row

            XcenIm = XImageCap + (wSize / 2)
            YcenIm = YImageCap + (hSize / 2)

            XImageCap = XImageCap + wSize
            print("X>>>>>" , XImageCap, XcenIm, YcenIm)
            if(XImageCap > XCorner_BR):
                print("X***********************")
                diffX = XImageCap-XCorner_BR
                XcenIm = XcenIm - (diffX/2)
                wSize = wSize - diffX
                XImageCap = XCorner_BR

            YImageCap = YImageCap + hSize
            print("Y>>>>>", YImageCap, XcenIm, YcenIm)
            if (YImageCap > YCorner_BR):
                print("Y***********************")
                diffY = YImageCap - YCorner_BR
                YcenIm = YcenIm - (diffY / 2)
                hSize = hSize - diffY
                YImageCap = YCorner_BR

            Latcen, LongCen = PixelXYToLatLong(XcenIm, YcenIm, MapZoom)

            latlong = [Latcen, LongCen]
            # print("latlong: ", latlong)
            address = "https://www.mapquestapi.com/staticmap/v4/getplacemap?location=" + str(latlong[0]) + "%2C" + str(
                latlong[1]) + "&size=" + str(wSize) + "%2C" + str(hSize + 24) + "&type=" + getType + "&zoom=" + str(
                MapZoom) + "&imagetype=png&scalebar=false&key=" + apiKey
            print(address)
            name = area + '_' + getType + '_' + 'Y_' +  str(yc) + '_' + 'X_' +  str(xc) + "_Lat_" + str(latlong[0]) + "_Long_" + str(latlong[1])
            print(name)
            # Method1
            urllib.request.urlretrieve(address, name + '.png')

            time.sleep(0.5)
            im1 = Image.open(name + '.png')
            #im1.show(name)
            #im1.crop(0, 0,  im1.size[0]-1, im1.size[1]-24-1)
            dstImage.paste(im1, (XImageCap-wSize-XCorner_TL,  YImageCap-hSize-YCorner_TL))
            xc = xc + 1
        except:
            print('Error along get :' + area + '_' + 'Y_' + str(yc) + '_' + 'X_' + str(xc))

    if( YImageCap == YCorner_BR):
        break

    XImageCap = XCorner_TL
    YImageCap_Row = YImageCap
    yc = yc + 1
    xc = 0
    wSize = wSizeOrg

dstImage.save("XXXX.png")