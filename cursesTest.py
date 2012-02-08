# PYTHON 3.2.2

# simple curses program
import curses, traceback, string, os

# a few globals for easyness sake
hotkey_attr = curses.A_BOLD | curses.A_UNDERLINE
menu_attr = curses.A_NORMAL

EXIT = 0
CONTINUE = 1
SET_MENU = None

def menus_setup(menus):
    # create the top menu for selecting things
    left = 2
    for menu in menus:
        menu_name=menu[0]
        menu_hotkey = menu_name[0]
        menu_no_hot = menu_name[1:]
        screen.addstr(1, left, menu_hotkey, hotkey_attr)
        screen.addstr(1, left+1, menu_no_hot, menu_attr)
        left = left + len(menu_name)+3
        topbar_key_handler((str.upper(menu_hotkey),menu[1]))
        topbar_key_handler((str.lower(menu_hotkey),menu[1]))
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

def rm_col(max_y, max_x):
    # erase old right box edge when window gets resized
    screen.addstr(10,10,str(max_x))
    for yPos in range(1, max_y-1):
        screen.delch(yPos, max_x-1)

def rm_row(max_y, max_x):
    # erase old bottom box edge when window gets resized
    screen.addstr(10,10,str(max_y))
    screen.move(max_y-1, 1)
    screen.deleteln()
    # for xPos in range(1, max_x-1):
    #     screen.delch(max_y-1, xPos)

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
        else:
            curses.beep()
    return CONTINUE


def main(stdscr, max_y, max_x):
    # set up screen for standard terminal size
    global screen
    screen = stdscr.subwin(max_y,max_x,0,0)
    screen.box()
    screen.hline(2, 1, curses.ACS_HLINE, max_x-2)
    screen.addstr(30, 10, str(max_y))
    screen.addstr(31, 10, str(max_x))
    screen.refresh()

    # define menus
    file_menu = ("File", file_func) 
    exit_menu = ("Exit", exit_func) # EXIT

    # add topbar menu
    menus_setup((file_menu, exit_menu))

    #topbar menu loop
    while topbar_key_handler():
        screen.move(1,1)
        new_y, new_x = stdscr.getmaxyx()
        if (new_y, new_x) != (max_y, max_x):
            if new_x > max_x:
                rm_col(max_y, max_x)
            if new_y > max_y:
                rm_row(max_y, max_x)
        max_y, max_x = new_y, new_x
        curses.resizeterm(max_y, max_x)
        screen.box()
        screen.hline(2, 1, curses.ACS_HLINE, max_x-2)
        screen.refresh()

if __name__=='__main__':
    try:
        # initialize curese
        stdscr=curses.initscr()
        max_y, max_x = stdscr.getmaxyx()
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
        main(stdscr, max_y, max_x)
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




