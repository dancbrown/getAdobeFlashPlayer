# getAdobeFlashPlayer.py
# Version 0.9
# By Dan Brown

import os, sys, requests, bs4, time
from datetime import date

# -----------------
# GLOBAL VARIABLES:
# -----------------

downloadURLs = []
soup = []
versionCurrent = []

# ----------
# FUNCTIONS:
# ----------

# writeOutToLog function to:
# write application messages to a log file with datestamp
def writeOutToLog(message):
    versionFile = open('getAdobeFlashPlayer.log', 'a')
    versionFile.write(str(date.today()) + ', ' + message + '\n')
    versionFile.close()


# getWebpage function to:
# get a webpage and parse it
def getWebpage(URL):
    webpage = requests.get(URL)
    webpage.raise_for_status()
    global soup
    soup = bs4.BeautifulSoup(webpage.text, "html.parser")


# ---------------------------------------
# Check: Adobe Flash Player About webpage
# ---------------------------------------

# Use getWebpage function to:
# Get and parse the Adobe Flash Player About webpage:
getWebpage('http://www.adobe.com/software/flash/about/')


# Extract all table cells
elems = soup.select('td')


# Using a for loop:
#   - Convert list elements from HTML to string data type
#   - Remove unwanted HTML characters from the string
for i in range(len(elems)):
    listElement = str(elems[i])
    if ('Internet Explorer - ActiveX') in listElement:
        #print(listElement[4:-5] + ', ' + str(elems[i+1])[4:-5])
        versionCurrent.append(listElement[4:-5] + ', ' + str(elems[i+1])[4:-5])
    if ('Firefox, Mozilla - NPAPI') in listElement:
        #print(listElement[4:-5] + ', ' + str(elems[i+1])[4:-5])
        versionCurrent.append(listElement[4:-5] + ', ' + str(elems[i+1])[4:-5])


# If it does not exist, create FlashPlayerVersion.txt
versionFile = open('FlashPlayerVersion.txt', 'a')
versionFile.write('')
versionFile.close()


# Open FlashPlayerVersion.txt
versionFile = open('FlashPlayerVersion.txt')
versionFileContent = versionFile.read()
versionFile.close()


# Test version...
test = versionCurrent[0] + '\n' + versionCurrent[1]

if str(versionFileContent) != test:
    print('New Adobe Flash Player version found:')
    print(test)
    print('Downloading Adobe Flash Player...')
    writeOutToLog('New Adobe Flash Player version found:')
    writeOutToLog(versionCurrent[0])
    writeOutToLog(versionCurrent[1])
    writeOutToLog('Downloading Adobe Flash Player...')
    # Record details of the latest version of Flash Player
    versionFile = open('FlashPlayerVersion.txt', 'w')
    versionFile.write(test)
    versionFile.close()
    # Continue... to download
else:
    print('Adobe Flash Player is up-to-date.')
    writeOutToLog('Adobe Flash Player is up-to-date.')
    sys.exit()

# -----------------------------------------------------
# Download from Adobe Flash Player Distribution webpage 
# -----------------------------------------------------

# Use getWebpage function to:
# Get and parse Adobe Flash Player Distribution webpage:
getWebpage('Enter Adobe\'s Flash Player Distribution URL here!')


# Extract all links within lists within table cells:
elems = soup.select('td li a')
# Extract all URLs for the MSI installers:
for i in range(len(elems)):
    listElement = str(elems[i])
    if ('.msi') in listElement:
        elems[i] = listElement[9:-28]
        downloadURLs.append(elems[i])


# Download Adobe Flash Player msi files:
for i in range (2):
#for i in range (len(downloadURLs)):
    print('Downloading file: ' + (downloadURLs[i])[72:])
    writeOutToLog('Downloading file: ' + (downloadURLs[i])[72:]) 
    downloadFile = requests.get(downloadURLs[i])
    downloadFile.raise_for_status()
    playFile = open((downloadURLs[i])[72:], 'wb')
    for chunk in downloadFile.iter_content(100000):
        playFile.write(chunk)
    playFile.close()


print('Downloads complete!')
writeOutToLog('Downloads complete!')
sys.exit()

# ---
# END
# ---
