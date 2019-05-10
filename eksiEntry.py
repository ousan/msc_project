from bs4 import BeautifulSoup
from urllib.request import urlopen
import json

####################Config####################
entryDir="/home/oguzhan/Desktop/entry/"

firstEntryId=1
lastEntryId=100
numberOfRecordedEntryForAFile=10
##############################################

eksiURL="https://eksisozluk.com"
rootUrl="https://eksisozluk.com/entry/"
fileIndex=0
counter=0
for i in range(firstEntryId,lastEntryId):
    try:
        entryURL=rootUrl+str(i)
        response = urlopen(entryURL)
        html = response.read().decode("utf-8")
        if counter >= numberOfRecordedEntryForAFile:
        	counter = 0
        	fileIndex = fileIndex +1
        	print("fileindex: ", fileIndex)

        entryFile=entryDir+str(fileIndex)
        soup = BeautifulSoup(html,'lxml')
        
        entryText=""
        entryID=str(i)
        entryDate=""
        entryTitle=""
        entryTitleURL=""
        entryAuthor=""

        counter = counter + 1
        for content_tag in soup.findAll("div", {"class": "content"}):
            entryText=content_tag.text
            entryText=entryText.replace("\n", "")
            entryText=entryText.replace("\r", "")
            
            #entryText = entryText + "\n"
            
        for entry_date_tag in soup.findAll("a", {"class": "entry-date"}):
            entryDate=entry_date_tag.text

        for entry_author_tag in soup.findAll("a", {"class": "entry-author"}):
            entryAuthor=entry_author_tag.text

        for entry_title_tag in soup.findAll("h1", {"id": "title"}):
            entryTitle=entry_title_tag.text
            entryTitle=entryTitle.replace("\n", "")
            entryTitle=entryTitle.replace("\r", "")

            for link in entry_title_tag.find_all('a'):
                entryTitleURL=eksiURL + link.get('href')
    
        #print(entryID)
        #print(entryDate)
        #print(entryText)
        #print(entryTitle)
        #print(entryTitleURL)
        #print(entryURL)
        #print(entryAuthor)
        
        entryJSON={'id' : entryID , 'date' : entryDate, 'title' : entryTitle, 'author' : entryAuthor, 'text' : entryText, 'titleURL' : entryTitleURL, 'entryURL' : entryURL}
        #print(entryJSON)

        with open(entryFile, 'a') as outfile:  
            json.dump(entryJSON, outfile,indent=4, ensure_ascii=False)
            outfile.write("\n")
        
    except :
        pass