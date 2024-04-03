# Creates a table holding information about each tune from the assorted BWW files
# Rhys O'Higgins, 4/24
import os
import csv
import codecs


idioms = ["March", "Strathspey", "Reel", "Hornpipe", "Jig", "Waltz", "Air", "Slow Air", "Polka"]
timeSigs = ["4_4", "2_4", "2_2", "3_4", "6_8", "12_8", "9_8", "5_4"," C ", "C_"]

tuneNames = os.listdir("UniqueTunes")
tunes = [None]*len(tuneNames) # this will hold all of the info about each tune (one row per tune)

# for each tune we want:
# name, idiom, time signature, number of parts, number of lines
fields = ["Name", "Idiom", "Time Sig", "Num Parts", "Num Lines"]

for i in range(len(tuneNames)): # go through each tune

    # get the tune as a string
    f = codecs.open("UniqueTunes/"+tuneNames[i],encoding='utf-8')
    tuneStr = f.read()
    f.close()

    # find the idiom
    tuneIdiom = "NA"
    for idiom in idioms:
        if idiom in tuneStr: # potiential issue in tunes with two listed! Taking the second, however, should avoid titles (which is good)
            tuneIdiom = idiom

    # find the time sig
    tuneSig = "NA"
    for sig in timeSigs:
        if sig in tuneStr: # same potential issue as above
            tuneSig = sig
    
    numParts = tuneStr.count("I!")
    numLines = tuneStr.count("&amp")

    tunes[i] = [tuneNames[i][:-4], tuneIdiom, tuneSig, numParts, numLines]


with open('TuneInfo.csv', 'w', newline="") as f:
     
    # using csv.writer method from CSV package
    write = csv.writer(f)
    
    write.writerow(fields)
    write.writerows(tunes)





