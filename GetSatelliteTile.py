import requests
import urllib.request
import utm
import numpy as np
import math
import time
import os
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
#latCenter = 31.9
#longCenter = 54.96
#Resolution = 16000
#MapZoom = 15   #  mode1:15   mode2:17
#area = "Delta25"
#getType = 'map'   #sat-hyb-map
#>>LatLong TL : 32.19101272231434 54.616684913635254
#>>LatLong BR : 31.60807169015679 55.303330421447754
#------------------

#------ Tehran Azadi
#latCenter = 35.699734
#longCenter = 51.337912
#Resolution = 16000
#MapZoom = 17   #  mode1:15   mode2:17
#area = "Tehran_Azadi"
#getType = 'sat'   #sat-hyb-map
#>>LatLong TL : 35.97804090977126 50.99458694458008
#>>LatLong BR : 35.42042651838322 51.68123245239258
#------------------

#------ Lowshan
#latCenter = 36.66667
#longCenter = 49.5
#Resolution = 16000
#area = "Lowshan"
#MapZoom = 15   #  mode1:15   mode2:17
#getType = 'sat'   #sat-hyb-map
#15 zoom
#>>LatLong TL : 36.941557331985436 49.156694412231445
#>>LatLong BR : 36.39078396650731 49.843339920043945
#17 zoom
#>>LatLong TL : 36.73548793168048 49.414165019989014
#>>LatLong BR : 36.59779438415188 49.58582639694214
#------------------

#------ Alghadir yazd
#latCenter = 31.74862
#longCenter = 54.381923
#Resolution = 16000
#area = "Alghadir"
#MapZoom = 15   #  mode1:15   mode2:17
#getType = 'sat'   #sat-hyb-map
#15 zoom
#>>LatLong TL : 32.0400945059217 54.038615226745605
#>>LatLong BR : 31.456196738293727 54.725260734558105
#17 zoom
#>>LatLong TL : 31.82158274738066 54.29609656333923
#>>LatLong BR : 31.675607968788633 54.46775794029236
#------------------

#------ Alghadir yazd
#latCenter = 31.74862
#longCenter = 54.381923
#Resolution = 16000
#area = "Alghadir"
#MapZoom = 15   #  mode1:15   mode2:17
#getType = 'sat'   #sat-hyb-map
#15 zoom
#>>LatLong TL : 32.0400945059217 54.038615226745605
#>>LatLong BR : 31.456196738293727 54.725260734558105
#17 zoom
#>>LatLong TL : 31.82158274738066 54.29609656333923
#>>LatLong BR : 31.675607968788633 54.46775794029236
#------------------

#------ kedenj
#latCenter = 29.42
#longCenter = 52.405
#Resolution = 8000
#area = "Kedenj"
#MapZoom = 18   #  mode1:15   mode2:17
#getType = 'sat'   #sat-hyb-map
#15 zoom
#>>LatLong TL : 32.0400945059217 54.038615226745605
#>>LatLong BR : 31.456196738293727 54.725260734558105
#17 zoom
#>>LatLong TL : 31.82158274738066 54.29609656333923
#>>LatLong BR : 31.675607968788633 54.46775794029236
#------------------

#------ kedenj2
# latCenter = 29.17
# longCenter = 52.5
# Resolution = 16000
# area = "Kedenj"
# MapZoom = 18   #  mode1:15   mode2:17
# getType = 'sat'   #sat-hyb-map



#------ ShahinShar
latCenter = 33.227211
longCenter = 51.262115
Resolution = 96468

area = "ShahinShar"
MapZoom = 17   #  mode1:15   mode2:17
getType = 'sat'   #sat-hyb-map
#15 zoom
#>>LatLong TL : 30.928991496743947 48.64089488983154
#>>LatLong BR : 30.338176282978083 49.32754039764404
#17 zoom
#>>LatLong TL : 30.70785878439814 48.89836549758911
#>>LatLong BR : 30.560154582611865 49.070026874542236
#------------------

####################################################################################
#API parameters
## sia
apiKey = "aTrzS6yVWcHMaimAczjk6IVrX3iobhyc"
## hani
#apiKey = "4XrDOHmLY57IESC0rmP3NGYZLaxbOSXE"

####################################################################################

wSize = 500             #  mode1:1850   mode2:1950
hSize = 500
edgeHalfLen = 30    #Half len of edge in kilometer
wSizeOrg = wSize

XCenter, YCenter = LatLongToPixelXY(latCenter, longCenter, MapZoom)
latCorner_TL , longCorner_TL = PixelXYToLatLong((XCenter - Resolution/2), (YCenter - Resolution/2) , MapZoom)
latCorner_BR , longCorner_BR = PixelXYToLatLong((XCenter + Resolution/2), (YCenter + Resolution/2) , MapZoom)
latCorner_TR , longCorner_TR = PixelXYToLatLong((XCenter + Resolution/2), (YCenter - Resolution/2) , MapZoom)
latCorner_BL , longCorner_BL = PixelXYToLatLong((XCenter - Resolution/2), (YCenter + Resolution/2) , MapZoom)
print ("LatLong FULL TL :", latCorner_TL , longCorner_TL)
print ("LatLong FULL BR :", latCorner_BR , longCorner_BR)
print ("LatLong FULL TR :", latCorner_TR , longCorner_TR)
print ("LatLong FULL BL :", latCorner_BL , longCorner_BL)

lat1 = (latCorner_TL / 180) * math.pi
lon1 = (longCorner_TL / 180) * math.pi
lat2 = (latCorner_TL / 180) * math.pi
lon2 = (longCorner_BR / 180) * math.pi
distkm = math.acos(math.sin(lat1)*math.sin(lat2)+math.cos(lat1)*math.cos(lat2)*math.cos(lon2-lon1))*6371
print("Top Line Distance :", distkm)
lat1 = (latCorner_BR / 180) * math.pi
lon1 = (longCorner_TL / 180) * math.pi
lat2 = (latCorner_BR / 180) * math.pi
lon2 = (longCorner_BR / 180) * math.pi
distkm = math.acos(math.sin(lat1)*math.sin(lat2)+math.cos(lat1)*math.cos(lat2)*math.cos(lon2-lon1))*6371
print("Botton Line Distance :", distkm)

exit()

latlong = [0.1,0.1]
XCorner_Full_TL, YCorner_Full_TL = LatLongToPixelXY(latCorner_TL, longCorner_TL, MapZoom)
XCorner_Full_BR, YCorner_Full_BR = LatLongToPixelXY(latCorner_BR, longCorner_BR, MapZoom)
print ("TL_FULL_pix:", XCorner_Full_TL, YCorner_Full_TL)
print ("BR_FULL_pix:", XCorner_Full_BR, YCorner_Full_BR)

TileNum = 6
TileW = ((XCorner_Full_BR - XCorner_Full_TL) / TileNum)
TileH = ((YCorner_Full_BR - YCorner_Full_TL) / TileNum)
for iTile in range(0, TileNum):
    for jTile in range(0, TileNum):
        XCorner_TL = (int)(XCorner_Full_TL + (iTile * TileW))
        XCorner_BR = (int)(XCorner_Full_TL +((iTile+1) * TileW))
        YCorner_TL = (int)(YCorner_Full_TL + (jTile * TileH))
        YCorner_BR = (int)(YCorner_Full_TL + ((jTile+1) * TileH))
        print("Tile ", iTile, "," , jTile,  "TL_Tilepix:", XCorner_TL, YCorner_TL)
        print("Tile ", iTile, "," , jTile,  "BR_Tilepix:", XCorner_BR, YCorner_BR)

        XImageCap = XCorner_TL
        YImageCap = YCorner_TL
        YImageCap_Row = YImageCap
        yc = 0
        xc = 0
        XcenIm = 0
        YcenIm = 0


        dstImage = Image.new('RGB', ((int)(XCorner_BR - XCorner_TL), (int)(YCorner_BR - YCorner_TL)))

        print ("FinalImage Size:", dstImage.size)

        while (YImageCap <= YCorner_BR):
            while (XImageCap < XCorner_BR):
                try:
                    YImageCap = YImageCap_Row

                    XImageCap_Pr = XImageCap
                    YImageCap_Pr = YImageCap

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

                    # Version4
                    # address = "https://www.mapquestapi.com/staticmap/v4/getplacemap?location=" + str(latlong[0]) + "%2C" + str(
                    #     latlong[1]) + "&size=" + str(wSize) + "%2C" + str(hSize + 24) + "&type=" + getType + "&zoom=" + str(
                    #     MapZoom) + "&imagetype=png&scalebar=false&key=" + apiKey

                    # Version5
                    address = "https://www.mapquestapi.com/staticmap/v5/map?center=" + str(latlong[0]) + "%2C" + str(
                        latlong[1]) + "&size=" + str(wSize) + "%2C" + str(hSize + 24) + "&type=" + getType + "&zoom=" + str(
                        MapZoom) + "&imagetype=png&scalebar=false&key=" + apiKey

                    print(address)
                    name = area + '_' + str(MapZoom) + '_' + getType + '_' + 'Y_' +  str(yc) + '_' + 'X_' +  str(xc) + "_Lat_" + str(latlong[0]) + "_Long_" + str(latlong[1])
                    print(name)

                    # Method1
                    if not(os.path.exists(name + '.png')):
                        print('>>> !!Try Getting File')
                        try:
                            urllib.request.urlretrieve(address, name + '.png')

                        except urllib.request.CalledProcessError as e:
                            print('Error *****************'+e)
                            XImageCap = XImageCap_Pr
                            YImageCap = YImageCap_Pr
                            continue

                        time.sleep(0.5)
                    else:
                        print('>>>>>>>>>>> file exist <<<<<<<<<<')


                    im1 = Image.open(name + '.png')
                    #im1.show(name)
                    #im1.crop(0, 0,  im1.size[0]-1, im1.size[1]-24-1)
                    dstImage.paste(im1, ((int)(XImageCap-wSize-XCorner_TL),  (int)(YImageCap-hSize-YCorner_TL)))

                    #if os.path.exists(name + '.png'):
                    #    os.remove(name + '.png')

                    xc = xc + 1
                except ValueError:
                    print('Error along get :[' + ValueError + ']'+ area + '_' + 'Y_' + str(yc) + '_' + 'X_' + str(xc))

            if( YImageCap == YCorner_BR):
                break

            XImageCap = XCorner_TL
            YImageCap_Row = YImageCap
            yc = yc + 1
            xc = 0
            wSize = wSizeOrg

        dstImage.save(area+ '_'+ getType + '_Tile [' + iTile +'_'+jTile+ ']_'+ str(MapZoom)+ '_X.png')