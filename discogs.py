# PYTHON 3.2.2


# Discogs Record Collection GUI V 0.1a

import curses, traceback, string, os, xml.dom.minidom
from xml.dom.minidom import parse

# globals for GUI
hotkey_attr = curses.A_BOLD | curses.A_UNDERLINE
menu_attr = curses.A_NORMAL

EXIT = 0
CONTINUE = 1

MAX_Y = 0
MAX_X = 0

## Data Processing Classes and Functions
class entry(object):
    # Entry Class to get all variables for each entry
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

def get_release_info(dom):
    # get the id in <release id = 'xxxxxxxxx'>
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

def print_entry(releaseId, release):
    # print out the entry in a semi-pretty format
    for item in release:
        if item.return_releaseId() == releaseId:
            return(item.return_artist(), '|', item.return_title(), '|', item.return_year(), '|', \
                  item.return_genre(), '|', item.return_format()) # entry arguments with |'s        

def search_fields(node, fromInput, releaseObjectList):
    # simple search function.  allows for searing for any field, case insensative.
    if (fromInput.lower() in node.return_artist().lower()) == True or \
       (fromInput.lower() in node.return_title().lower()) == True or \
       (fromInput.lower() in node.return_year().lower()) == True or \
       (fromInput.lower() in node.return_genre().lower()) == True or \
       (fromInput.lower() in node.return_format().lower()) == True: # list of fields to check against user input
        return(True)

def sort_items(toSortList):
    # sorts everything by artist, title, year, and format, forward and reverse.  Returns a
    # dictionary of lists with the keys being all the artist, title, etc.
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

def return_matches(userInput, release):
    # returns a list of nodes that match the search query
    searchHits = []
    for item in release:
        if search_fields(item, userInput, release) == True:
            searchHits.append(item)
    return searchHits

# # how i printed things in the test program
# def main():
#     dom = parse('discogs.xml') # parse the document                              
#     release = get_release_info(dom) # get list of all objects with data filled in
#     while True:
#         userInput = input('Search for what?  ') # simple test prompt             
#         if userInput == 'quit':
#             sys.exit()
#         else:
#             searchHits = return_matches(userInput, release)
#         print(searchHits)
#         alphaDict = sort_items(searchHits)
#         sortIt = input('Sort by what? ')
#         print_sorted(sortIt, alphaDict, release)
#
# if __name__ == '__main__':
#     main()

## UI and Data Interaction Functions

def print_sorted(userChoice, alpha, release, MAX_Y, MAX_X):
    # print out the types in whatever order the users asks for
    if userChoice == 'artist up':
        yPos = 4
        for listPoint in alpha['artistUp']:     # print all the hits
            if yPos < MAX_Y-2:
                screen.addnstr(yPos, 3, str(print_entry(listPoint.return_releaseId(), release)), MAX_X-2)
                yPos += 1
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

def show_collection(release):
    searchHits = return_matches("Vinyl", release)
    alphaDict = sort_items(searchHits)
    print_sorted('artist up', alphaDict, release, MAX_Y, MAX_X)

## UI Section Functions

def menus_setup(menus):
    # create the top menu for selecting things
    left = 2
    for menu in menus:
        menu_name = menu[0]
        menu_hotkey = menu_name[0]
        menu_no_hot = menu_name[1:]
        screen.addstr(1, left, menu_hotkey, hotkey_attr)
        screen.addstr(1, left+1, menu_no_hot, menu_attr)
        left = left + len(menu_name)+3
        topbar_key_handler((str.upper(menu_hotkey), menu[1]))
        topbar_key_handler((str.lower(menu_hotkey), menu[1]))
    screen.refresh()

def topbar_key_handler(key_assign=None, key_dict={}):
    # magic I stole from gnosis.cx                                               
    if key_assign:                
        key_dict[ord(key_assign[0])] = key_assign[1]
    else:
        c = screen.getch()
        if c in (curses.KEY_END, ord('!')):
            return 0
        elif c not in key_dict.keys():
            curses.beep()
            return CONTINUE
        else:
            return key_dict[c]()

def rm_col(MAX_Y, MAX_X):
    # erase old right box edge when window gets resized
    screen.addstr(10,10,str(MAX_X))
    for yPos in range(1, MAX_Y-1):
        screen.delch(yPos, MAX_X-1)

def rm_row(MAX_Y, MAX_X):
    # erase old bottom box edge when window gets resized
    screen.addstr(10,10,str(MAX_Y))
    screen.move(MAX_Y-1, 1)
    screen.deleteln()

def exit_func():
    # exit function
    return EXIT

def file_func():
    # file menu for exiting, exiting, etc.
    fMenu = curses.newwin(6,20,2,1)
    fMenu.box()
    fMenu.addstr(1,2, "W", hotkey_attr)
    fMenu.addstr(1,3, "rite Something", menu_attr)
    fMenu.addstr(2,2, "C", hotkey_attr)
    fMenu.addstr(2,3, "lear", menu_attr)
    fMenu.addstr(3,2, "S", hotkey_attr)
    fMenu.addstr(3,3, "how Collection", menu_attr)
    fMenu.refresh()
    set_menu = True
    while set_menu == True:
        c = fMenu.getch()
        if c in (ord('W'), ord('w')):
            screen.addstr(10,10, "Well Hot Damn")
            screen.move(1,23)
            fMenu.erase()
            screen.refresh()
            set_menu = False
        elif c in (ord('C'), ord('c')):
            screen.addstr(10,10, "             ")
            screen.move(1,23)
            fMenu.erase()
            screen.refresh()
            set_menu = False
        elif c in (ord('S'), ord('s')):
            show_collection(release)
            fMenu.erase()
            screen.refresh()
            set_menu = False
        else:
            curses.beep()
    return CONTINUE

def main(stdscr):
    # set up screen for standard terminal size
    global screen
    global MAX_Y
    global MAX_X
    screen = stdscr.subwin(MAX_Y,MAX_X,0,0)
    screen.box()
    screen.hline(2, 1, curses.ACS_HLINE, MAX_X-2)
    screen.addstr(30, 10, str(MAX_Y))
    screen.addstr(31, 10, str(MAX_X))
    screen.refresh()

    # define menus
    file_menu = ("File", file_func)
    exit_menu = ("Exit", exit_func) # EXIT

    # add topbar menu
    menus_setup((file_menu, exit_menu))

    # set up XML
    dom = parse('discogs.xml') # parse the document                              
    global release 
    release = get_release_info(dom) # get list of all objects with data filled in

    #topbar menu loop
    while topbar_key_handler():
        screen.move(1,1)
        new_y, new_x = stdscr.getmaxyx()
        if (new_y, new_x) != (MAX_Y, MAX_X):
            if new_x > MAX_X:
                rm_col(MAX_Y, MAX_X)
            if new_y > MAX_Y:
                rm_row(MAX_Y, MAX_X)
        MAX_Y, MAX_X = new_y, new_x
        curses.resizeterm(MAX_Y, MAX_X)
        screen.box()
        screen.hline(2, 1, curses.ACS_HLINE, MAX_X-2)
        screen.refresh()

if __name__=='__main__':
    try:
        # initialize curses
        stdscr=curses.initscr()
        global MAX_Y
        global MAX_X
        MAX_Y, MAX_X = stdscr.getmaxyx()
        # turn of fechoing of keys, and enter cbreak mode,                                                           
        # where no buffering is performed on keyboard                                                                
        # input
        curses.noecho() ; curses.cbreak()

        # make the cursor invisible
        curses.curs_set(0)


        # in keypad mode, escape sequences for special keys
        # (like the cursor keys) will be interpreted and
        # a special value like curses.KEY_LEFT will be
        # returned
        stdscr.keypad(1)
        main(stdscr)
        # set everything back to normal for clean exit
        stdscr.keypad(0)
        curses.echo() ; curses.nocbreak()
        curses.endwin()
    except:
        # in event of an error, restore the terminal
        # to a sane state
        stdscr.keypad(0)
        curses.echo() ; curses.nocbreak()
        curses.endwin()
        traceback.print_exc()  # print the exception



