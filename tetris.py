import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP
import copy
from random import randint

HEIGTH = 21
WIDTH = 12
def new_block():
    block = [[4, 1], tetblock[randint(0,5)]]
    return block

def draw_block(stdscr, block):
    for i in range(0, 4):
        for j in range(0, 4):
            if block[1][i*4 + j] != '.':
                stdscr.addch(block[0][1] + i, block[0][0] + j, block[1][i*4 + j])

def rotate(block):
    newblock = [block[0], ['.' for i in range(0, 16)]]
    for i in range(0, 4):
        for j in range(0, 4):
            newblock[1][i*4 + j] = block[1][12 - j*4 + i]
    return newblock

def draw_field(stdscr, field):
    for i in range(0, HEIGTH-1):
        for j in range(0, WIDTH):
            if field[i*WIDTH + j] != '.':
                stdscr.addch(i, j, field[i*WIDTH + j])


def is_possible_move(block, field):  
    for i in range(0, 4):
        for j in range(0, 4):
            if block[1][i*4 + j] != '.':
                if field[(block[0][1]+i)*WIDTH + block[0][0]+j] != '.':
                    return False
    
    return True

def block_to_field(field, block):
    for i in range(0, 4):
        for j in range(0, 4):
            if block[1][i*4 + j] != '.':
                field[(block[0][1]+i)*WIDTH + block[0][0]+j] = block[1][i*4 + j]

def check_full_line(field, score):
    for i in range(2, HEIGTH-2):
        line = 1
        for j in range(1, WIDTH):
            if field[i*(WIDTH)+j] == '.':
                line = 0
                continue
        if line == 1:
            for k in range(i, 2, - 1):
                for l in range(1, WIDTH):
                    if l%WIDTH != 0 and l%WIDTH != WIDTH-1:
                        field[(k)*(WIDTH)+l] = field[(k-1)*(WIDTH)+l]
            score = score + 100
    return score


def main(stdscr):
    stdscr = curses.newwin(HEIGTH, WIDTH, 1, 20)
    stdscr.keypad(True)
    curses.noecho()
    curses.curs_set(0)
    #stdscr.border(0)
    stdscr.nodelay(1)

    block = new_block()
    for i in range(0, HEIGTH-1):
        for j in range(0, WIDTH):
            if j == 0 or j == WIDTH-1 or i == HEIGTH-2:
                field[i*WIDTH + j] = 'x'
    
    draw_block(stdscr, block)
    score = 0
    key = 0
    #stdscr.addch(10, 5, '#')
    while key != 27:
        stdscr.addstr(0, 4, str(score))
        key = 0
        prevkey = key
        event = stdscr.getch() 
        key = key if event == -1 else event
        if key not in [KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_UP, 27]:
            key = 0
        stdscr.clear()
        prevblock = copy.deepcopy(block)

        if key == KEY_LEFT:
            block[0][0] -= 1    
        if key == KEY_RIGHT:
            block[0][0] += 1
        if key == KEY_DOWN:
            block[0][1] += 1
        if key == KEY_UP:
            block = rotate(block)
 
        
        if is_possible_move(block, field):
            draw_block(stdscr, block)
        else:
            if key == KEY_DOWN:
                block_to_field(field, prevblock)
                score = check_full_line(field, score)
                block = new_block()
            else:
                block = copy.deepcopy(prevblock)
            
            draw_block(stdscr, block)
        check_full_line(field, score)
        draw_field(stdscr, field)
        
        




tetblock = []
tetblock.append([   '.', '.', 'A', '.',
                    '.', '.', 'A', '.',
                    '.', '.', 'A', '.',
                    '.', '.', 'A', '.'])

tetblock.append([   '.', '.', 'B', '.',
                    '.', 'B', 'B', '.',
                    '.', 'B', '.', '.',
                    '.', '.', '.', '.'])

tetblock.append([   '.', 'C', '.', '.',
                    '.', 'C', 'C', '.',
                    '.', '.', 'C', '.',
                    '.', '.', '.', '.'])

tetblock.append([   '.', '.', '.', '.',
                    '.', '.', 'D', '.',
                    '.', '.', 'D', '.',
                    '.', 'D', 'D', '.'])

tetblock.append([   '.', '.', '.', '.',
                    '.', 'E', '.', '.',
                    '.', 'E', '.', '.',
                    '.', 'E', 'E', '.'])

tetblock.append([   '.', '.', '.', '.',
                    '.', 'F', 'F', '.',
                    '.', 'F', 'F', '.',
                    '.', '.', '.', '.'])


field = ['.' for i in range(0, (HEIGTH-1)*WIDTH)]

curses.wrapper(main)