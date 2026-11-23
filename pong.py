import curses
import time

def pong(paddle_y, end_y, stdscr):
    size = 5
    for x in range(size):
        row = paddle_y + x
        if 0 <= row < end_y:
            stdscr.addstr(row, 0, "@")

def en_pong(en_paddle_y, end_x, end_y, stdscr):
    size = 5
    for x in range(size):
        row = en_paddle_y - x
        if 0 <= row < end_x:
            stdscr.addstr(row, end_x - 1, "@")

def ball(ball_direction_x, ball_direction_y, ball_x, ball_y, paddle_y, end_x, end_y, stdscr):
    size = 5

    if ball_x == 0 and paddle_y <= ball_y <= paddle_y + size - 1:
        ball_direction_x = 1
        return ball_direction_x,ball_direction_y, ball_x + 2

    elif ball_x == 0:
        stdscr.addstr(0, 0, "YOU LOSE")
        stdscr.refresh()
        curses.napms(2000)

    elif ball_x == end_x - 1:
        ball_direction_x = -1
        return ball_direction_x, ball_direction_y, ball_x - 2

    elif ball_y == 0:
        ball_direction_y = 1
        return ball_direction_x,ball_direction_y,ball_x

    elif ball_y == end_y:
        ball_direction_y = -1
        return ball_direction_x,ball_direction_y,ball_x

    else:
        return ball_direction_x,ball_direction_y, ball_x + ball_direction_x


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)

    h, w = stdscr.getmaxyx()
    end_x = w - 1  # last col is a border
    end_y = h - 1  # last row is a border

    # state
    paddle_y = end_y // 2
    ball_direction_x = -1
    ball_direction_y = -1
    ball_x = end_x // 2
    ball_y = end_y // 2

    while True:
        ch = stdscr.getch()

        if ch == ord('q'):
            break
        elif ch == ord('w'):
            paddle_y = max(paddle_y - 1, 0)     #the top of the screen is y 0 so paddle -1 makes it move up
        elif ch == ord('s'):
            paddle_y = min(paddle_y + 1, end_y - 5) #the botome of the screen is end_y -5 because the top @ is the true thing
        curses.flushinp()

        ball_direction_x,ball_direction_y, ball_x = ball(ball_direction_x, ball_direction_y, ball_x, ball_y, paddle_y, end_x, end_y, stdscr)
        # draw
        ball_y = ball_y + ball_direction_y
        stdscr.erase()
        pong(paddle_y, end_y, stdscr)
        en_paddle_y = max(ball_y, 5) #if ball_y < end_y / 2 else max(ball_y)
        en_pong(en_paddle_y, end_x, end_y, stdscr)
        stdscr.addstr(ball_y, ball_x, '@', curses.color_pair(1))
        stdscr.refresh()

        curses.napms(50)  # ~20 FPS is also game speed...


curses.wrapper(main)
