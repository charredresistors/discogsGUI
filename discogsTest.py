# the start of my python Discogs GUI
import sys
import xml.dom.minidom
from xml.dom.minidom import parse

# entry class to get all variables for each entry
class entry(object):
    def __init__(self, releaseId, artist, title, year, genre, formatType):
        self.releaseId = releaseId
        self.artist = artist
        self.title = title
        self.year = str(year)
        self.genre = genre
        self.formatType = formatType
    def __repr__(self):
        return repr((self.releaseId, self.artist, self.title, self.year, \
                     self.genre, self.formatType))
    def return_releaseId(self):
        return self.releaseId
    def return_artist(self):
        return self.artist
    def return_title(self):
        return self.title
    def return_year(self):
        return self.year
    def return_genre(self):
        return self.genre
    def return_format(self):
        return self.formatType

# get the id in <release id = 'xxxxxxxxx'>
def get_release_info(dom):
    final = []
    for ele in dom.getElementsByTagName('release'):
        releaseId = ele.getAttribute('id') # very first attribute in xml
        artist = get_artist(ele)
        title = get_title(ele)
        year = get_year(ele)
        genre = get_genre(ele)
        formatType = get_format(ele)
        final.append(entry(releaseId, artist, title, year, genre, formatType)) # make the list
    return final

# Funtions to populate each new release object.  releaseId is
# is for each release.  <release id ="xxxxxxxx"> in the xml.

def get_artist(node):
    for child in node.getElementsByTagName('name'):
        if child.parentNode.localName == 'artist':
            return(child.firstChild.nodeValue)
def get_title(node):
    for child in node.getElementsByTagName('title'):
        if child.parentNode.localName == 'release':
            return(child.firstChild.nodeValue)
def get_year(node):
    for child in node.getElementsByTagName('released'):
        if child.parentNode.localName == 'release':
            return(child.firstChild.nodeValue)
def get_genre(node):
    for child in node.getElementsByTagName('genre'):
        if child.parentNode.localName == 'genres':
            return(child.firstChild.nodeValue)
def get_format(node):
    for child in node.getElementsByTagName('format'):
        return child.getAttribute('name')

# print out the entry in a semi-pretty format
def print_entry(releaseId, release):
    for item in release:
        if item.return_releaseId() == releaseId:
            print(item.return_artist(), '|', item.return_title(), '|', item.return_year(), '|', \
                  item.return_genre(), '|', item.return_format()) # entry arguments with |'s

# simple search function.  allows for searing for any field, case insensative.
# also strips the (*) from many artits entires.  must match exactly otherwise.

def search_fields(node, fromInput, releaseObjectList):
    if (fromInput.lower() in node.return_artist().lower()) == True or \
       (fromInput.lower() in node.return_title().lower()) == True or \
       (fromInput.lower() in node.return_year().lower()) == True or \
       (fromInput.lower() in node.return_genre().lower()) == True or \
       (fromInput.lower() in node.return_format().lower()) == True: # list of fields to check against user input
        return(True)

# sorts everything by artist, title, year, and format, forward and reverse.  Returns a 
# dictionary of lists with the keys being all the artist, title, etc.

def sort_items(toSortList): 
    artistUp = sorted(toSortList, key=lambda x: x.artist)
    artistDown = sorted(toSortList, key=lambda x: x.artist, reverse = True)
    titleUp = sorted(toSortList, key=lambda x: x.title)
    titleDown = sorted(toSortList, key=lambda x: x.title, reverse = True)
    yearUp = sorted(toSortList, key=lambda x: x.year)
    yearDown = sorted(toSortList, key=lambda x: x.year, reverse = True)
    formatUp = sorted(toSortList, key=lambda x: x.formatType)
    formatDown = sorted(toSortList, key=lambda x: x.formatType, reverse = True)
    return ({'artistUp':artistUp, 'artistDown':artistDown, 'titleUp':titleUp, \
             'titleDown':titleDown, 'yearUp':yearUp, 'yearDown':yearDown, \
             'formatUp':formatUp, 'formatDown':formatDown})

# returns a list of nodes that match the search query

def return_matches(userInput, release):
    searchHits = []
    for item in release:
        if search_fields(item, userInput, release) == True:
            searchHits.append(item)
    return searchHits

# print out the types in whatever order the users asks for

def print_sorted(userChoice, alpha, release):
    if userChoice == 'artist up':      
        for listPoint in alpha['artistUp']:     # print all the hits
            print_entry(listPoint.return_releaseId(), release)
    elif userChoice == 'artist down':     
        for listPoint in alpha['artistDown']:     # print all the hits
            print_entry(listPoint.return_releaseId(), release)
    elif userChoice == 'title up':
        for listPoint in alpha['titleUp']:     # print all the hits
            print_entry(listPoint.return_releaseId(), release)
    elif userChoice == 'title down':          
        for listPoint in alpha['titleDown']:     # print all the hits
            print_entry(listPoint.return_releaseId(), release)
    elif userChoice == 'year up':
        for listPoint in alpha['yearUp']:     # print all the hits
            print_entry(listPoint.return_releaseId(), release)
    elif userChoice == 'year down':
        for listPoint in alpha['yearDown']:     # print all the hits
            print_entry(listPoint.return_releaseId(), release)
    elif userChoice == 'format up':
        for listPoint in alpha['formatUp']:     # print all the hits
            print_entry(listPoint.return_releaseId(), release)
    elif userChoice == 'format down':
        for listPoint in alpha['formatDown']:     # print all the hits
            print_entry(listPoint.return_releaseId(), release)
    else:
        print('bad type')


# main loop (currently for testing to see if everything works)
def main():
    dom = parse('discogs.xml') # parse the document
    release = get_release_info(dom) # get list of all objects with data filled in
    while True:
        userInput = input('Search for what?  ') # simple test prompt
        if userInput == 'quit':
            sys.exit()
        else:
            searchHits = return_matches(userInput, release)
        print(searchHits)
        alphaDict = sort_items(searchHits)
        sortIt = input('Sort by what? ')
        print_sorted(sortIt, alphaDict, release)

if __name__ == '__main__':
    main()



