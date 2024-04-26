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

def getEditdistance(path1,path2, timelimit = -1):
    """Given paths to edgelist csv files for two networks, returns the edit distance between the note-transition graphs of those tunes
    NOTE: this is too slow to use in practice for comparison between many networks. I highly reccomend using the time limit
    """
    g1 = weightedGraphFromEdgeList(path1)
    g2 = weightedGraphFromEdgeList(path2)
    print(g1, g2)
    if timelimit > 0:
        return nx.graph_edit_distance(g1,g2,timeout=timelimit)
    else:
        return nx.graph_edit_distance(g1,g2)

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
    diameter = "NA"
    avgPathLen = "NA"
    if connected:
        diameter = nx.diameter(g)
        avgPathLen = nx.average_shortest_path_length(g)
    return (clustCoef,connected, diameter, avgPathLen)

def getIdiomStats(pathToEdgeListCsv):
    """Same as above, but for a given idiom. This one takes a file path to the csv edgelist of the graph.
    TODO: should refactor this and the above method into one"""
    g = weightedGraphFromEdgeList(pathToEdgeListCsv)
    clustCoef = nx.average_clustering(g, weight='weight')
    connected = nx.is_strongly_connected(g)
    diameter = "NA"
    avgPathLen = "NA"
    if connected:
        diameter = nx.diameter(g)
        avgPathLen = nx.average_shortest_path_length(g)
    return (clustCoef,connected, diameter, avgPathLen)

def makeStatCsvs():
    """Creates csv files with statistics on tune and idiom networks.
    NOTE: highly brittle/specialized. Honestly shouldn't really be a method, but I wanted the code out of main. Use with caution."""
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

    # get stats for full idiom graphs
    f = open("Note Networks/Idiom Stats.csv", mode="w")
    f.write("idiom,clustcoef,connected,diameter,avgpathlen\n")
    for i in ["4_4 Marches", "Jigs", "Reels"]:
        stats = i
        for s in getIdiomStats("Note Networks/All " + i + ".csv"):
            stats  = stats + "," + str(s)
        f.write(stats + "\n")
    f.close()


if __name__ == "__main__":
    timelim = 400 # this is in seconds
    print(getEditdistance("Note Networks/All 4_4 Marches.csv", "Note Networks/All Jigs.csv",timelim))
    print(getEditdistance("Note Networks/All 4_4 Marches.csv", "Note Networks/All Reels.csv",timelim))
    print(getEditdistance("Note Networks/All Reels.csv", "Note Networks/All Jigs.csv",timelim))

