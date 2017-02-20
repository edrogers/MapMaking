#!/usr/bin/python

import pandas as pd
from PIL import Image
import os

def convertLatToPixelY(lat):
    my=(520.0-195.0)/(36.999-45.0)
    by=195.0-45.0*my
    return lat*my+by

def convertLngToPixelX(lng):
    mx=(1046.0-490.0)/(111.05-94.618)
    bx=490.0+111.05*mx
    return lng*mx+bx

listOfStates=["ia", "ks", "in", "mo", "nd", "mn", "wi", "mi", "il", "oh", "ne", "sd"]

dictOfCSVsByState = {}
for state in listOfStates:
    rootdir = "/home/ed/Work/DataRole/us/{}".format(state)
    for root, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith(".csv"):
                if state not in dictOfCSVsByState:
                    dictOfCSVsByState[state]=[os.path.join(root, file)]
                else:
                    dictOfCSVsByState[state].extend([os.path.join(root, file)])
    # print state
    # print dictOfCSVsByState[state]
    
startingMap="/home/ed/Work/DataRole/2000px-USA_location_map.svg.png"
# outputMap="/home/ed/Work/DataRole/01_AllLocations.png"
# outputMap="/home/ed/Work/DataRole/02_LocationsWithMoreThanLatLng.png"
# outputMap="/home/ed/Work/DataRole/03_LocationsWithStreetAddress.png"
# outputMap="/home/ed/Work/DataRole/04_LocationsWithStreetAddressTop400.png"
outputMap="/home/ed/Work/DataRole/04_LocationsWithStreetAddressTop400Darker.png"

outMapImg=Image.open(outputMap)
myMapX,myMapY=outMapImg.size

for state in listOfStates:
    for csv in dictOfCSVsByState[state]:
        df = pd.read_csv(csv)
        myXvalues= [ int(convertLngToPixelX(lng)) for lng in df["LON"].values.tolist() ]
        myYvalues= [ int(convertLatToPixelY(lat)) for lat in df["LAT"].values.tolist() ]
        rowsToCheck=400
        if df.count < 400:
            rowsToCheck=df.count
        if rowsToCheck == 0:
            continue
        hasNonLatLngValues = (df.iloc[0:rowsToCheck,2:4].isnull()==False).all(axis=1).values.tolist()
        myXYtuples=zip(myXvalues,myYvalues)
        for i, xyTuple in enumerate(myXYtuples):
            if i == rowsToCheck:
                break
            if xyTuple[0] < 0 or xyTuple[0] > myMapX or xyTuple[1] < 0 or xyTuple[1] > myMapY:
                print xyTuple
            elif hasNonLatLngValues[i] :
                thisColor=list(outMapImg.getpixel(xyTuple))
                # thisColor[0]-=1
                # thisColor[1]-=1
                # thisColor[2]+=1
                thisColor[0]=0
                thisColor[1]=0
                thisColor[2]=255
                outMapImg.putpixel(xyTuple,tuple(thisColor))
outMapImg.save(outputMap)

quit()
