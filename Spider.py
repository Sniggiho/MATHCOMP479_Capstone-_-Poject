# Scraper for gathering .bww data from Bagpipe Tunes website and putting it in text files. 
# For Network Science capstone project
# Rhys O'Higgins, 3/24

import requests
from bs4 import BeautifulSoup
import codecs



alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0-9"]
alphabet2 = ["M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0-9"]

for letter in alphabet2:

    r = requests.get("https://bagpipetunes.intertechnics.com/alpha_results.php?d=" + letter)
    soup = BeautifulSoup(r.content, 'html.parser')

    links = soup.find_all("a") # Find all elements with the tag <a>
    links = links[5:-1] # Get rid of navigation links, so we're just left with links to tunes


    for link in links:
        if link.get("href")[-3:] == "bww": # we just want .bww files

            r2 = requests.get("https://bagpipetunes.intertechnics.com/" + link.get("href"))
            soup2 = BeautifulSoup(r2.content, 'html.parser')
            tuneAsText = soup2.prettify()

            f = codecs.open("Tunes/" + link.string.replace("/","").replace("?","") + ".txt", "w",encoding='utf-8' )
            f.write(tuneAsText)
            f.close()