import networkx
import RandomWalk

def transFreqsToGraph(freqs):
    """Given a map with keys in format note1,note2 and values containing the number of transitions between those notes, creates a networkx edge network representing the graph"""
    G = networkx.DiGraph()
    for notePair in freqs.keys():
        notes = notePair.split(",")
        G.add_edge(notes[0],notes[1],weight = freqs[notePair])

    return G

def weightedGraphFromEdgeList(file):
    """Given a csv edgelist with a weight n edge (a,b) represented by n repeated entries of a,b returns a networkx weighted digraph"""
    return(transFreqsToGraph(RandomWalk.generateTransFreqMap(file)))

# generate some statics using networks of the tunes