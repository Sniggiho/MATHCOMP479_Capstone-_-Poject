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


def expandTune(tuneString):
    """Given a string representing a tune in BWW format, expands it to be linear (i.e. no repeats, frist/second endings, etc.)"""
    expandedTuneString = ""
    parts = tuneString.split("I!")
    
    for p in parts:

        if p[0:2] == "''" and not "_'" in p: # if there is a repeat but no first/second endings
            expandedTuneString = expandedTuneString + p + p
        elif p[0:2] == "''" and "_'" in p: # if there is a repeat and different first vs. second ending
            endings = re.findall("'[1|2][\s|\S]+?_'", p)
            head = p[0:p.find(endings[0])] # before the split to first vs second ending
            tail = p[p.find(endings[-1]) + len(endings[-1]):] # this is empty if the endings are really endings, and will contain notes if the "endings" are in fact variations inside the part

            if not re.findall("\w_\d",tail): # if there are no notes after the end of the second ending, proceed
                expandedTuneString = expandedTuneString + head

                if len(endings)>1: # if both endings are included in this part
                    for e in endings:
                        if "'1" in e:
                            expandedTuneString = expandedTuneString + e

                    expandedTuneString = expandedTuneString + head

                    for e in endings:
                        if "'2" in e:
                            expandedTuneString = expandedTuneString + e

                else: # if this is a 2 of 4 type situation
                    if re.findall("'\d\d", endings[0]): # if this is a line to be repeated later, we'll just double it now. NOTE: this would be a problem for comparing across tunes, but will be okay to count frequencies
                        expandedTuneString = expandedTuneString + endings[0] + head + endings[0] + endings[0]
                    else: # if this is the line to be not repeated (e.g. being replaced by that of an earlier part on the repeat)
                        expandedTuneString = expandedTuneString + endings[0] + head
            else: # otherwise, the first and second endings  aren't really endings, but in-part variations
                expandedTuneString = expandedTuneString + head + endings[0] + tail + head + endings[1] + tail
        else: # if there are no repeats
            expandedTuneString = expandedTuneString + p
    return expandedTuneString

    

def getNotes(tune):
    """Given a tune string, returns a list of all the notes in that tune"""
    dirtyNotes = re.findall(notesPat, tune)
    notes = []

    for n in dirtyNotes:
        n = n.replace("l","").replace("r","")
        if "'" in n:
            n = re.sub(" '[abcdefg]+", "d",n)  
        notes.append(n)
    return notes

def getNotesFromName(title):
    """Convenience method; given a tune name, returns all of the notes in the expanded tune as a list"""
    return getNotes(expandTune(getTuneString(title)))


def getTransitionFreqs(notes, transFreqs = {}): #TODO: this is sloppy
    """Given a list of cleaned notes corresponding to a tune, counts the frequency of transition between ordered pairs of notes
    in a hashmap with keys = ordered note pair and values = number of occurences"""
    for i in range(len(notes)-1):
        if notes[i]+"," + notes[i+1] in transFreqs.keys():
            transFreqs[notes[i]+","+notes[i+1]] = transFreqs[notes[i]+"," + notes[i+1]] +1
        else:
            transFreqs[notes[i]+","+notes[i+1]] = 1
    return transFreqs
    
def makeEdgeListCSV(transFreqs, filename):
    """Given a hashmap with note pairing frequencies, creates an edge list csv appropriate for use in Gephi"""
    f = open(filename,mode="w")

    for key in transFreqs.keys():
        for i in range(transFreqs[key]):
            f.write(key+"\n")
    f.close()

if __name__ == "__main__":
    marches4_4 = []
    # print(expandTune(getTuneString("Scotland the Brave")))
    jigs = []

    f = open("TuneInfo.csv")
    rows = f.readlines()

    # 4_4 marches
    for r in rows:
        if "March,4_4" in r:
            marches4_4.append( r[0:r.find("March,4_4")].replace("\"","").strip(","))
        elif "March, C" in r:
            marches4_4.append( r[0:r.find("March, C")].replace("\"","").strip(","))

    # Jigs -------------------
    # for r in rows:
    #     if ",Jig," in r:
    #         jigs.append(r[0:r.find(",Jig,")].replace("\"", "").strip(","))
    f.close()

    allTransFreqs = {} # TODO: this is sloppy

    for tune in marches4_4:
        notes = getNotesFromName(tune)
        getTransitionFreqs(notes, allTransFreqs)

        makeEdgeListCSV(allTransFreqs, "Note Networks/All 4_4 Marches.csv")