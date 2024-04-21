import networkx
import random

def generateTransFreqMap(file):
    """Given a csv edgelist, creates a map with edges as the keys and frequencies as the notes"""
    freqs = {}

    f = open(file)
    
    for line in f.readlines():
        line = line.strip()
        if line in freqs.keys():
            freqs[line]+=1
        else:
            freqs[line] = 1

    return freqs

def transFreqsToGraph(freqs):
    """Given a map with keys in format note1,note2 and values containing the number of transitions between those notes, creates a networkx edge network representing the graph"""
    G = networkx.DiGraph()
    for notePair in freqs.keys():
        notes = notePair.split(",")
        G.add_edge(notes[0],notes[1],weight = freqs[notePair])

    return G

def weightedGraphFromEdgeList(file):
    """Given a csv edgelist with a weight n edge (a,b) represented by n repeated entries of a,b returns a networkx weighted digraph"""
    return(transFreqsToGraph(generateTransFreqMap(file)))

def getNoteDuration(note):
    """Given a note string in the form N_#, returns an integer value representing the number of 32nd notes in that note"""
    # 32 -> 1
    # 16 -> 2
    # 8 -> 4
    # 4 -> 8
    # 2 -> 16
    # 1 -> 32
    num = note.split("_")[1]
    dur = 0
    if "d" in num:
        num = num[:-1]
        dur += 32/(int(num)*2)
    dur += 32/(int(num))

    return dur

# def randomTuneWalk(G, staringNote = None, measureLen = 32, numMeasures = 16):
#     """Given a weighted digraph G - as well as optionally a starting note, time signature and nummber of 32nds per measure - does a random walk on G to generate a bagpipe tune.
#     Attempts to avoid ties across barlines where possible, adhering to measure level tune logic.
#     """
#     if staringNote == None:
#         currNote = random.choice(list(G.nodes()))
#     else:
#         currNote = staringNote
#     print("currNote initialized as", currNote)
    
#     m = 0 # the number of measures generated so far
#     mSum = getNoteDuration(currNote) # the total duration of notes in the current measure 

#     while m <= numMeasures:

#         neighbors = list(G[currNote].keys()) # all the neighbors of 
#         weights = list
#         pass

def measuredRandomWalk(transFreqs, staringNote = "LA_4",  measureLen = 32, numMeasures = 16):
    """Given a map with keys in format note1,note2 and values containing the number of transitions between those notes 
    does a ranodm walk on those notes to create a tune measure by measure."""
    
    # TODO: some logic to allow a random starting note?

    currNote = staringNote    
    m = 0 # the number of measures generated so far
    mSum = getNoteDuration(currNote) # the total duration of notes in the current measure 
    tune = []
    measure = [currNote]

    while m < numMeasures:
        neighbors = []
        weights = []
        for key in transFreqs.keys():
            if currNote in key.split(",")[0]:
                n = key.split(",")[1]
                if getNoteDuration(n) <= measureLen - mSum: # if the note will fit in what we have left of the measure
                    neighbors.append(key.split(",")[1])
                    weights.append(transFreqs[key])
        if len(neighbors) == 0:
            raise Exception("No legal neighbor")

        currNote  = random.choices(neighbors,weights=weights,k=1)[0]
        measure.append(currNote)

        mSum += getNoteDuration(currNote)
        
        if mSum == measureLen:
            mSum = 0
            m += 1
            tune.append(measure)
            measure = []
    
    return tune




tune = measuredRandomWalk(generateTransFreqMap("Note Networks/All 4_4 Marches.csv"), staringNote="LA_8d", numMeasures=4)
print(tune)