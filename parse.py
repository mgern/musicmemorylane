import sys
import bisect
from bisect import *

def find_index(a, f):
    x = min(a, key=lambda x:abs(x-f))
    return x
    

#print(str(sys.argv)) #test
if len(sys.argv) == 3:
    
    lastfmfile = open(sys.argv[1], encoding="UTF-8")
    mapsfile = open(sys.argv[2], encoding="UTF-8")
    
    lastfmcsv = lastfmfile.readlines()
    mapscsv = mapsfile.readlines()
    lastfmfile.close()
    mapsfile.close()
    #per scrobble file, find the closest location data (nearest)
    #skip first lines
    lastfmcsv = lastfmcsv[1:]
    mapscsv = set(mapscsv[1:])

    
    
    
    #sort ascending
    lastfmcsv = sorted(lastfmcsv, key=lambda i:i[1:])
    mapscsv = sorted(mapscsv, key=lambda i:i[1:])

    #just timestamps
    maptimestamps = []
    for x in mapscsv:
        maptimestamps.append(int(x.split(",")[0]))
    #find highest and lowest timestamp in both files
    #print(lastfmcsv[0].split(",")[0])

    lfmlowesttimestamp = int(lastfmcsv[0].split(",")[0])
    lfmhighesttimestamp = int(lastfmcsv[-1].split(",")[0])
    mapslowesttimestamp = int(mapscsv[0].split(",")[0])
    mapshighesttimestamp = int(mapscsv[-1].split(",")[0])

    print(mapslowesttimestamp, mapshighesttimestamp, sep=" ")
    print(lfmlowesttimestamp, lfmhighesttimestamp, sep=" ")

    for x in lastfmcsv:
        lfmsplitline = x.split(",")
        #print(splitline)
        #get timestamp for this line
        lfmtimestamp = int(lfmsplitline[0])

        #check if this one is even in the range of the maps file
        if lfmtimestamp < mapslowesttimestamp:
            continue

        #match this timestamp with closest maps timestamp for lat long
        #accept timestamps within range -10 min and + 3hr
        timeceiling = int(lfmtimestamp) + 60000  #3hrs -> seconds
        timefloor = int(lfmtimestamp) - 10000

        #look for timestamp in mapscsv within timeceiling and timefloor
        

        index = find_index(maptimestamps, lfmtimestamp)
        difference = index - lfmtimestamp
        #print("searching... ", lfmtimestamp, " match: ", index, "diff ", difference)
        
        if abs(difference) <= 60000:
            #if timefloor <= maptimestamps[index] <= timeceiling:
            index = maptimestamps.index(index)
            printtuple = mapscsv[index]
            if int(printtuple[0]) <= timeceiling:
                print(printtuple, lfmsplitline[1], lfmsplitline[3], lfmsplitline[7], sep=",")
                continue
    
else:
    print("usage: python parse.py <last fm scrobbles.csv> <maps.csv>")
input("Enter to close")