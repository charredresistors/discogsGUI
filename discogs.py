#! /bin/python3.2
#
# Discogs Record Collection GUI V 0.1a
# now in version control!

import curses, traceback, string, os, xml.dom.minidom
from xml.dom.minidom import parse

# globals for GUI
hotkey_attr = curses.A_BOLD | curses.A_UNDERLINE
menu_attr = curses.A_NORMAL

EXIT = 0
CONTINUE = 1

MAX_Y = None
MAX_X = None

SPLIT_X = None

SEARCHINPUT = ''

INPUTTYPE = 'artist up'

POS = 0
LINESEL = 0
BOTTOMLINE = 0
TOPLINE = 0

MENUSIZE = 0

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

def return_matches(userInput, release, printAll = False):
    # returns a list of nodes that match the search query
    searchHits = []
    for item in release:
        if printAll == False:
            if search_fields(item, userInput, release) == True:
                searchHits.append(item)
        else:
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
#         Alphadict = sort_items(searchHits)
#         sortIt = input('Sort by what? ')
#         print_sorted(sortIt, alphaDict, release)
#
# if __name__ == '__main__':
#     main()

## UI and Data Interaction Functions

def print_entry(releaseId, release, lineNum):
    # print out the entry in the "pad" windows
    global POS
    POS = 0
    for item in release:
        if item.return_releaseId() == releaseId:
            global artistWin, titleWin, yearWin, genreWin, formatWin 
            artistWin.addstr(lineNum, 1, item.return_artist())
            titleWin.addstr(lineNum, 1, item.return_title())
            yearWin.addstr(lineNum, 1, item.return_year())
            genreWin.addstr(lineNum, 1, item.return_genre())
            formatWin.addstr(lineNum, 1, item.return_format())

def print_sorted(userChoice, alpha, release):
    # print out the types in whatever order the users asks for
    global POS
    POS = 0
    if userChoice == 'artist up':
        yPos = 1
        for listPoint in alpha['artistUp']:     # print all the hits
            print_entry(listPoint.return_releaseId(), release, yPos)
            yPos += 1
    elif userChoice == 'artist down':
        yPos = 1
        for listPoint in alpha['artistDown']:     # print all the hits
            print_entry(listPoint.return_releaseId(), release, yPos)
            yPos += 1
    elif userChoice == 'title up':
        yPos = 1
        for listPoint in alpha['titleUp']:     # print all the hits
            print_entry(listPoint.return_releaseId(), release, yPos)
            yPos += 1
    elif userChoice == 'title down':
        yPos = 1
        for listPoint in alpha['titleDown']:     # print all the hits
            print_entry(listPoint.return_releaseId(), release, yPos)
            yPos += 1
    elif userChoice == 'year up':
        yPos = 1
        for listPoint in alpha['yearUp']:     # print all the hits
            print_entry(listPoint.return_releaseId(), release, yPos)
            yPos += 1
    elif userChoice == 'year down':
        yPos = 1
        for listPoint in alpha['yearDown']:     # print all the hits
            print_entry(listPoint.return_releaseId(), release, yPos)
            yPos += 1
    elif userChoice == 'format up':
        yPos = 1
        for listPoint in alpha['formatUp']:     # print all the hits
            print_entry(listPoint.return_releaseId(), release, yPos)
            yPos += 1
    elif userChoice == 'format down':
        yPos = 1
        for listPoint in alpha['formatDown']:     # print all the hits
            print_entry(listPoint.return_releaseId(), release, yPos)
            yPos += 1
    else:
        return CONTINUE

def erase_hits():
    # clear the "pads"
    artistWin.erase()
    titleWin.erase()
    yearWin.erase()
    genreWin.erase()
    formatWin.erase()

def refresh_hits():
    # refresh the pads based based on the POS global to move up and down
    global artistWin, titleWin, yearWin, genreWin, formatWin
    artistWin.refresh(POS, 0, 3, 1, MAX_Y-1, SPLIT_X+5)
    titleWin.refresh(POS, 0, 3, SPLIT_X+6, MAX_Y-1, 2*SPLIT_X+10)
    yearWin.refresh(POS, 0, 3, 2*SPLIT_X+11, MAX_Y-1, 3*SPLIT_X+6)
    genreWin.refresh(POS, 0, 3, 3*SPLIT_X+7, MAX_Y-1, 4*SPLIT_X+3)
    formatWin.refresh(POS, 0, 3, 4*SPLIT_X+4, MAX_Y-1, MAX_X-1)

def set_select_line():
    # set the selected line based on LINESEL
    global artistWin, titleWin, yearWin, genreWin, formatWin
    artistWin.chgat(LINESEL, 0, curses.A_STANDOUT)
    titleWin.chgat(LINESEL, 0, curses.A_STANDOUT)
    yearWin.chgat(LINESEL, 0, curses.A_STANDOUT)
    genreWin.chgat(LINESEL, 0, curses.A_STANDOUT)
    formatWin.chgat(LINESEL, 0, curses.A_STANDOUT)

def unselect_line():
    # unselect a line based on LINESEL
    global artistWin, titleWin, yearWin, genreWin, formatWin
    artistWin.chgat(LINESEL, 0, curses.A_NORMAL)
    titleWin.chgat(LINESEL, 0, curses.A_NORMAL)
    yearWin.chgat(LINESEL, 0, curses.A_NORMAL)
    genreWin.chgat(LINESEL, 0, curses.A_NORMAL)
    formatWin.chgat(LINESEL, 0, curses.A_NORMAL)


def show_collection(release):
    # do the search and print out hits to the screen
    if SEARCHINPUT == "": # print all hits if there is no search string
        searchHits = return_matches(SEARCHINPUT, release, True)
    else: # search the search string
        searchHits = return_matches(SEARCHINPUT, release)
    alphaDict = sort_items(searchHits)
    erase_hits()
    print_sorted(INPUTTYPE, alphaDict, release)
    refresh_hits()

## UI Section Functions

def menus_setup(menus):
    # create the top menu for selecting things
    global MENUSIZE
    MENUSIZE = 2
    for menu in menus:
        menu_name = menu[0]
        menu_hotkey = menu_name[0]
        menu_no_hot = menu_name[1:]
        screen.addstr(1, MENUSIZE, menu_hotkey, hotkey_attr)
        screen.addstr(1, MENUSIZE+1, menu_no_hot, menu_attr)
        MENUSIZE = MENUSIZE + len(menu_name)+3
        topbar_key_handler((str.upper(menu_hotkey), menu[1]))
        topbar_key_handler((str.lower(menu_hotkey), menu[1]))
    screen.refresh()


def topbar_key_handler(key_assign=None, key_dict={}):
    # magic I stole from gnosis.cx
    global SEARCHINPUT
    global POS, LINESEL
    global TOPLINE, BOTTOMLINE
    global MAX_Y, MAX_X
    if key_assign:                
        key_dict[ord(key_assign[0])] = key_assign[1]
    else:
        screen.addstr(1, MENUSIZE + 1," " * ((MAX_X-2) - MENUSIZE))
#        screen.addstr(1, MAX_X-21, " "*20)
        curserPos =  MAX_X-40
        curserChange = 0
        curserNewPos = curserPos
        curserMin = 0
        screen.move(1, curserNewPos)
        userInput = ''
        SEARCHINPUT = userInput
        show_collection(release)
        screen.refresh()
        TOPLINE = 0
        BOTTOMLINE = MAX_Y-4
        LINESEL = 0
        c = screen.getch()
        while c != 10: # 10 is the enter key
#            screen.addstr(2,15,str(c)) use to tell what number = what key
            # resize screen on the fly
            new_y, new_x = check_screen_size()
            if (new_y, new_x) != (MAX_Y, MAX_X):
                MAX_Y, MAX_X = new_y, new_x
                change_screen_size()
                screen.addstr(1, MENUSIZE + 1," " * ((MAX_X-2) - MENUSIZE))
                BOTTOMLINE = TOPLINE + MAX_Y-4
                if LINESEL > BOTTOMLINE: # see if the line select went off screen during resize
                    unselect_line()
                    LINESEL = BOTTOMLINE 
            curserPos =  MAX_X-40
            curserNewPos = curserPos + curserChange
            screen.move(1, curserNewPos)
            screen.addstr(1, curserPos, userInput)
            set_select_line()
            refresh_hits()
            screen.refresh()
            if c == curses.KEY_DOWN and (artistWin.instr(LINESEL + 1, 1, \
                                         1).decode("utf-8") != ' '):
                # key down and push down selection so long as next line is not empty
                unselect_line()
                LINESEL += 1
                set_select_line()
                refresh_hits()
                screen.move(1, curserNewPos)
                if LINESEL > BOTTOMLINE: # move the screen down if beyond screen
                    TOPLINE += 1
                    BOTTOMLINE += 1
                    POS += 1
                    refresh_hits()
                c = screen.getch()
            elif c == curses.KEY_UP and POS >= 0: # key up and move selection
                if LINESEL == 0: # is the line at the very top?  do nothing
                    screen.move(1, curserNewPos)
                else:  # move up the selection
                    unselect_line()
                    LINESEL -= 1
                    set_select_line()
                    refresh_hits()
                if LINESEL < TOPLINE and POS > 0: #is the line greater than the top?
                    TOPLINE -= 1                  # but not at the very top? 
                    BOTTOMLINE -= 1               # move screen up
                    POS -= 1
                    refresh_hits()
                c = screen.getch()
            # pretty sure i dont need any of the below
            # elif c == curses.KEY_UP and POS == 0: # key up until very top
            #     unselect_line()
            #     LINESEL -= 1
            #     set_select_line()
            #     refresh_hits()
            #     screen.move(1, curserNewPos)
            #     if LINESEL == TOPLINE:
            #         TOPLINE -= 1
            #         BOTTOMLINE -= 1
            #     c = screen.getch()
            # elif c == curses.KEY_UP and POS == 0: # key up until top
            #     refresh_hits()        
            #     screen.move(1, curserNewPos)
            #     c = screen.getch()
            elif c == curses.KEY_NPAGE and (artistWin.instr(MAX_Y-5 + POS, 1, \
                                            1).decode("utf-8") != ' '):
                # page down until there are no more hits
                unselect_line()
                POS += MAX_Y-5 # MAX_Y-5 is how much each screen moves
                LINESEL += MAX_Y-5
                TOPLINE += MAX_Y-5
                BOTTOMLINE += MAX_Y-5
                set_select_line()
                refresh_hits()
                screen.move(1, curserNewPos)
                c = screen.getch()
            elif c == curses.KEY_PPAGE and POS > 0: # page up
                unselect_line()
                POS -= MAX_Y-5
                LINESEL -= MAX_Y-5
                TOPLINE -= MAX_Y-5
                BOTTOMLINE -= MAX_Y-5
                if LINESEL < 0: # if pageup moves beyond top, reset to top of screen values
                    POS = 0 
                    LINESEL = 0
                    TOPLINE = 0
                    BOTTOMLINE = MAX_Y-4
                set_select_line()
                refresh_hits()
                screen.move(1, curserNewPos)
                c = screen.getch()
            # pretty sure I dont need this as well
            # elif c == curses.KEY_PPAGE and POS <= 0: # keep the page up from going too far
            #     refresh_hits()        
            #     screen.move(1, curserNewPos)
            #     c = screen.getch()
            elif c == 127: # 127 is backspace
                if curserChange > curserMin:
                    userInput = userInput[:-1]
                    curserChange -= 1
                    curserNewPos = curserPos + curserChange 
                    screen.move(1, curserNewPos)
                    screen.addch(' ') # del character
                    screen.refresh()
                    screen.move(1, curserNewPos)
                    SEARCHINPUT = userInput
                    show_collection(release)
                    c = screen.getch()
                elif curserChange == curserMin: 
                    userInput = ''
                    c = screen.getch()
            elif c == 6:
                return key_dict[ord('f')]() # ctrl + f = file menu
            elif c == 5: # ctrl + e = bring up exit window
                exMenu = curses.newwin(8, 15, 10, 15)
                exMenu.box()
                exMenu.addstr(3, 5, 'Exit??')
                exMenu.addstr(4, 5, 'y OR n')
                exMenu.refresh()
                d = exMenu.getch()
                if d == ord('y'):
                    return key_dict[ord('e')]() # ctrl + f = file menu
                elif d == ord('n'):
                    exMenu.erase()
                    refresh_hits()
                    c = screen.getch()
                else:
                    d = exMenu.getch()
            elif c < 257: # get the key from the keyboard for search
                userInput += chr(c)
                screen.addstr(1, curserPos, userInput)
                screen.refresh()
                curserChange += 1
                curserNewPos = curserPos + curserChange
                screen.move(1, curserNewPos)
                SEARCHINPUT = userInput
                show_collection(release)
                LINESEL = 0
                POS = 0
                TOPLINE = 0
                BOTTOMLINE = MAX_Y-4
                refresh_hits()
                c = screen.getch()
            else:
                c = screen.getch()
        screen.refresh()
        return CONTINUE

# all from original code.  last line returns based on key using the key
# dicts.  useful for autosetting up of menus which isn't used right now
# but could be useful for future changes if new menues need to be added.
        # if len(userInput) == 0:
        #     return CONTINUE
        # elif ord(userInput[0]) not in key_dict.keys() or len(userInput) > 1:
        #     SEARCHINPUT = userInput
        #     show_collection(release)
        #     return CONTINUE
        # elif ord(userInput[0]) in (curses.KEY_END, ord('!')) and \
        #         len(userInput) == 1:
        #     return 0
        # else:
        #     return key_dict[ord(userInput[0])]()


def rm_col(MAX_Y, MAX_X):
    # erase old right box edge when window gets resized
    for yPos in range(1, 3):
        screen.delch(yPos, MAX_X-1)

def rm_row(MAX_Y, MAX_X):
    # erase old bottom box edge when window gets resized
    screen.deleteln()

def exit_func():
    # exit function
    return EXIT

def check_screen_size():
    # check the size of the screen to see if it's changed
    new_y, new_x = stdscr.getmaxyx()
    if (new_y, new_x) != (MAX_Y, MAX_X):
        if new_x > MAX_X:
            rm_col(MAX_Y, MAX_X)
        if new_y > MAX_Y:
            rm_row(MAX_Y, MAX_X)
    return new_y, new_x

def change_screen_size():
    # quite literal
    global SPLIT_X
    SPLIT_X = int(MAX_X/5)
    curses.resizeterm(MAX_Y, MAX_X)
    screen.box()
    screen.hline(2, 1, curses.ACS_HLINE, MAX_X-2)
    screen.refresh()
    refresh_hits()

def file_func():
    # file menu for exiting, exiting, etc.
    global INPUTTYPE
    fMenu = curses.newwin(6,20,2,1)
    fMenu.box()
    fMenu.addstr(1,2, "W", hotkey_attr)
    fMenu.addstr(1,3, "rite Something", menu_attr)
    fMenu.addstr(2,2, "C", hotkey_attr)
    fMenu.addstr(2,3, "lear", menu_attr)
    fMenu.addstr(3,2, "T", hotkey_attr)
    fMenu.addstr(3,3, "ype", menu_attr)
    fMenu.refresh()
    set_menu = True
    while set_menu == True:
        c = fMenu.getch()
        if c in (ord('W'), ord('w')): # useless
            screen.addstr(10,10, "Well Hot Damn")
            screen.move(1,23)
            fMenu.erase()
            screen.refresh()
            set_menu = False
        elif c in (ord('C'), ord('c')): # useless
            erase_hits()
            screen.move(1,23)
            fMenu.erase()
            set_menu = False
        elif c in (ord('T'), ord('t')): # file menu, only important one right now
            fMenu.addstr(3, 7, "->", menu_attr)
            fMenu.refresh()
            typeMenu = curses.newwin(10, 18, 4, 10)
            typeMenu.box()
            typeMenu.addstr(1, 2, "1", hotkey_attr)
            typeMenu.addstr(1, 3, " Artist Up", menu_attr)
            typeMenu.addstr(2, 2, "2", hotkey_attr)
            typeMenu.addstr(2, 3, " Artist Down", menu_attr)
            typeMenu.addstr(3, 2, "3", hotkey_attr)
            typeMenu.addstr(3, 3, " Title Up", menu_attr)
            typeMenu.addstr(4, 2, "4", hotkey_attr)
            typeMenu.addstr(4, 3, " Title Down", menu_attr)
            typeMenu.addstr(5, 2, "5", hotkey_attr)
            typeMenu.addstr(5, 3, " Year Up", menu_attr)
            typeMenu.addstr(6, 2, "6", hotkey_attr)
            typeMenu.addstr(6, 3, " Year Down")
            typeMenu.addstr(7, 2, "7", hotkey_attr)
            typeMenu.addstr(7, 3, " Format Up", menu_attr)
            typeMenu.addstr(8, 2, "8", hotkey_attr)
            typeMenu.addstr(8, 3, " Format Down", menu_attr)
            t = typeMenu.getch()
            # sort submenu options.  sets INPUTTYPE to change hits on the screen to 
            # desired order.  specifically changes print_sorted() to match the new
            # input
            if t == ord('1'):
                INPUTTYPE = 'artist up'
                show_collection(release)
            elif t ==ord('2'):
                INPUTTYPE = 'artist down'
                show_collection(release)
            elif t == ord('3'):
                INPUTTYPE = 'title up'
                show_collection(release)
            elif t == ord('4'):
                INPUTTYPE = 'title down'
                show_collection(release)
            elif t == ord('5'):
                INPUTTYPE = 'year up'
                show_collection(release)
            elif t == ord('6'):
                INPUTTYPE = 'year down'
                show_collection(release)
            elif t == ord('7'):
                INPUTTYPE = 'format up'
                show_collection(release)
            elif t == ord('8'):
                INPUTTYPE = 'format down'
                show_collection(release)
            typeMenu.erase()
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
    screen = stdscr.subwin(3,MAX_X,0,0)
    screen.keypad(1)
    screen.box()
    screen.hline(2, 1, curses.ACS_HLINE, MAX_X-2)
    screen.refresh()

    # define menus
    file_menu = ("File", file_func)
    exit_menu = ("Exit", exit_func) # EXIT

    # add topbar menu
    menus_setup((file_menu, exit_menu))

    # set up field windows (soon to be) according to user preferences
    global SPLIT_X
    SPLIT_X = int(MAX_X/5)
    global artistWin, titleWin, yearWin, genreWin, formatWin

    # Set up XML
    dom = parse('discogs.xml') # parse the document                              
    global release 
    release = get_release_info(dom) # get list of all objects with data filled in

    # set up subwindow "pads"
    artistWin = curses.newpad(len(release) + 256, 256)
    titleWin = curses.newpad(len(release) + 256, 256)
    yearWin = curses.newpad(len(release) + 256, 256)
    genreWin = curses.newpad(len(release) + 256, 256)
    formatWin = curses.newpad(len(release) + 256, 256)

    #topbar menu loop
    while topbar_key_handler():
        new_y, new_x = check_screen_size()
        MAX_Y, MAX_X = new_y, new_x
        change_screen_size()

if __name__=='__main__':
    try:
        # initialize curses
        stdscr=curses.initscr()
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
        screen.keypad(0)
        stdscr.keypad(0)
        curses.echo() ; curses.nocbreak()
        curses.endwin()
    except:
        # in event of an error, restore the terminal
        # to a sane state
        screen.keypad(0)
        stdscr.keypad(0)
        curses.echo() ; curses.nocbreak()
        curses.endwin()
        traceback.print_exc()  # print the exception

