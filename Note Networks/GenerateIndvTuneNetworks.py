import TuneToNetwork


if __name__ == "__main__":
    marches4_4 = []
    jigs = []
    reels = []

    f = open("TuneInfo.csv")
    rows = f.readlines()

    # 4_4 marches
    # for r in rows:
    #     if "March,4_4" in r:
    #         marches4_4.append( r[0:r.find("March,4_4")].replace("\"","").strip(","))
    #     elif "March, C" in r:
    #         marches4_4.append( r[0:r.find("March, C")].replace("\"","").strip(","))

    # #Jigs -------------------
    # for r in rows:
    #     if ",Jig," in r:
    #         jigs.append(r[0:r.find(",Jig,")].replace("\"", "").strip(","))

    for r in rows:
        if "Reel,2_2" in r:
            reels.append( r[0:r.find("Reel,2_2")].replace("\"","").strip(","))
        elif "Reel, C_" in r:
            reels.append( r[0:r.find("Reel, C_")].replace("\"","").strip(","))

    f.close()


    allTransFreqs = {} # TODO: this is sloppy

    for tune in reels:
        allTransFreqs = {} # TODO: this is sloppy
        notes = TuneToNetwork.getNotesFromName(tune)
        TuneToNetwork.getTransitionFreqs(notes, allTransFreqs)
        TuneToNetwork.makeEdgeListCSV(allTransFreqs, "Note Networks/Indv Tune Networks/" + tune + ".csv")