import codecs


def getTuneString(title):
    """Given a tune name, gets the contents of that tune and returns it as a bww format string"""
    f = codecs.open("UniqueTunes/"+title+".txt",encoding='utf-8')
    tune = f.read()
    f.close()

    startIdx = tune.find("&amp")

    tune = tune[startIdx:]

    return tune


def tuneToVector(tune, resolution=32):
    """Takes in a tune as a string, and outputs a string of integers representing that tune (embellishments are ignored)"""
    measures = tune.split("!")
    print(measures)
    
tuneToVector(getTuneString("Scotland The Brave"))