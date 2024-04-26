import networkx as nx
import RandomWalk

def transFreqsToGraph(freqs):
    """Given a map with keys in format note1,note2 and values containing the number of transitions between those notes, creates a networkx edge network representing the graph"""
    G = nx.DiGraph()
    for notePair in freqs.keys():
        notes = notePair.split(",")
        G.add_edge(notes[0],notes[1],weight = freqs[notePair])

    return G

def weightedGraphFromEdgeList(file):
    """Given a csv edgelist with a weight n edge (a,b) represented by n repeated entries of a,b returns a networkx weighted digraph"""
    return(transFreqsToGraph(RandomWalk.generateTransFreqMap(file)))

def getEditdistance(tune1,tune2):
    """Given the titles of two tunes, returns the edit distance between the note-transition graphs of those tunes
    NOTE: this is too slow to use in practice
    """
    g1 = weightedGraphFromEdgeList("Note Networks/Indv Tune Networks/" + tune1 + ".csv")
    g2 = weightedGraphFromEdgeList("Note Networks/Indv Tune Networks/" + tune2 + ".csv")
    for v in nx.optimize_graph_edit_distance(g1,g2):
        print(v)

def getTuneNetworkStats(tune):
    """Given a tune title, returns a list containing various statistics about the graph:

        - clustering coefficient
        - strongly connected?
        - diameter
        - avg path len
    """
    g = weightedGraphFromEdgeList("Note Networks/Indv Tune Networks/" + tune + ".csv")
    clustCoef = nx.average_clustering(g, weight='weight')
    connected = nx.is_strongly_connected(g)
    diameter = -1
    avgPathLen = -1
    if connected:
        diameter = nx.diameter(g)
        avgPathLen = nx.average_shortest_path_length(g)
    return (clustCoef,connected, diameter, avgPathLen)


if __name__ == "__main__":

    # gather the names of all 4_4 marches, jigs, and reels
    f = open("TuneInfo.csv")
    rows = f.readlines()

    tuneNames = []

    # 4_4 marches
    for r in rows:
        if "March,4_4" in r:
            tuneNames.append( r[0:r.find("March,4_4")].replace("\"","").strip(","))
        elif "March, C" in r:
            tuneNames.append( r[0:r.find("March, C")].replace("\"","").strip(","))

    #Jigs -------------------
    for r in rows:
        if ",Jig," in r:
            tuneNames.append(r[0:r.find(",Jig,")].replace("\"", "").strip(","))

    for r in rows:
        if "Reel,2_2" in r:
            tuneNames.append( r[0:r.find("Reel,2_2")].replace("\"","").strip(","))
        elif "Reel, C_" in r:
            tuneNames.append( r[0:r.find("Reel, C_")].replace("\"","").strip(","))

    f.close()

    # get stats for each one

    f = open("Note Networks/Tune Stats.csv", mode="w")
    f.write("name,clustcoef,connected,diameter,avgpathlen\n")
    for t in tuneNames:
        stats = "\"" +  t + "\""
        for s in getTuneNetworkStats(t):
            stats  = stats + "," + str(s)

        f.write(stats + "\n")
    f.close()