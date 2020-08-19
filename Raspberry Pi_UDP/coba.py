import curses
import time

def main(screen):
    refresh_rate = 1
    screen.nodelay(1)
    a = 0
    # Infinite loop. Displays information and updates it 
    # every (refresh_rate) # of seconds
 
    while True:
	a += 1
	print(a)
        # Escape infinite loop
        if screen.getch() == ord('q'):
            break

        # Wait before going through the loop again
        time.sleep(refresh_rate)

if __name__ == "__main__":
    curses.wrapper(main)