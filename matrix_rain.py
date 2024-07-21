import curses
import random
import time

def matrix_rain(stdscr):
    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # Clear screen
    stdscr.clear()
    curses.curs_set(0)

    height, width = stdscr.getmaxyx()

    # Initialize drops, each column with a random start position and speed
    drops = [{'pos': random.randint(0, height), 'speed': random.uniform(0.05, 0.3)} for _ in range(width)]

    while True:
        stdscr.clear()
        for i in range(width):
            column = drops[i]
            char = random.choice(['0', '1'])
            
            # Draw character at the current position
            if 0 <= column['pos'] < height:
                stdscr.addstr(column['pos'], i, char, curses.color_pair(1))

            # Move the drop down by incrementing its position
            column['pos'] += 1

            # Reset position if it goes off screen
            if column['pos'] >= height:
                column['pos'] = 0

        stdscr.refresh()

        # Sleep for a short time to control the speed of the rain
        time.sleep(0.05)

def main():
    curses.wrapper(matrix_rain)

if __name__ == "__main__":
    main()
