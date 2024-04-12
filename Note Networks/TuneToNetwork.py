# Functions for turning a BWW file into an edgelist CSV, 
# Nodes are notes of a specific duration (e.g. Low A 16th quaiver), and there is an edge from note 1 to note 2 if note 2 follows note 1 in the tune
# Rhys O'Higgins, 4/24

import codecs
import re

notesPat = "L?[ABCDEFG][lr]?_\d\d?(?: 'l?[abcdefg])?" # for regex

def getTuneString(title):
    """Given a tune name, gets the contents of that tune and returns it as a bww format string"""
    f = codecs.open("UniqueTunes/"+title+".txt",encoding='utf-8')
    tune = f.read()
    f.close()

    startIdx = tune.find("&amp")
    tune = tune[startIdx:]

    return tune

def getNotes(tune):
    """Given a tune string, returns a list of all the notes in that tune
    TODO: update this to deal with repeats, dumb endings, etc.
    """
    dirtyNotes = re.findall(notesPat, tune)
    notes = []

    for n in dirtyNotes:
        n = n.replace("l","").replace("r","")
        if "'" in n:
            n = re.sub(" '[abcdefg]+", "d",n)  
        notes.append(n)
    return notes

def getTransitionFreqs(notes):
    """Given a list of cleaned notes corresponding to a tune, counts the frequency of transition between ordered pairs of notes
    in a hashmap with keys = ordered note pair and values = number of occurences"""
    transFreqs = {}
    for i in range(len(notes)-1):
        if notes[i]+"," + notes[i+1] in transFreqs.keys():
            transFreqs[notes[i]+","+notes[i+1]] = transFreqs[notes[i]+"," + notes[i+1]] +1
        else:
            transFreqs[notes[i]+","+notes[i+1]] = 1
    return transFreqs
    
def makeEdgeListCSV(transFreqs, filename):
    f = open(filename,mode="w")

    for key in transFreqs.keys():
        for i in range(transFreqs[key]):
            f.write(key+"\n")
    f.close()


tuneString = getTuneString("Scotland The Brave")
freqs = getTransitionFreqs(getNotes(tuneString))
print(freqs)
makeEdgeListCSV(freqs, "STBEdgeList.csv")

