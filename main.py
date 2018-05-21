from tkinter import *
import random

class Ant:
    location = [0, 0]  # [x, y]
    orientation = 'n'

    def __init__(self, middle, orientation):
        # location is the center of grid
        self.location = [middle, middle]
        self.orientation = orientation
        # initial orientation is random navigational direction (ex: n = north)

    def move(self, movement):
        # movement is left (0) or right (1)
        if self.orientation == 'n':
            if movement:  # move == right == 1
                self.east()  # make player face east
            else:
                self.west()
        elif self.orientation == 's':
            if movement:
                self.west()
            else:
                self.east()
        elif self.orientation == 'e':
            if movement:
                self.south()
            else:
                self.north()
        else:
            if movement:
                self.north()
            else:
                self.south()

    def north(self):
        self.orientation = 'n'
        self.location[1] -= 1

    def south(self):
        self.orientation = 's'
        self.location[1] += 1

    def east(self):
        self.orientation = 'e'
        self.location[0] += 1

    def west(self):
        self.orientation = 'w'
        self.location[0] -= 1


class OurLabel(Label):
    # extension of Label that can be visited by our ant
    visited = False

    def set_background(self):
        # check if visited to change background
        if self.visited:
            self.config(background="white")
        else:
            self.config(background="black")
        self.visited = not self.visited


class Window(Frame):
    def __init__(self, master=None, size=5):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.make_grid(size)
        random_orientation = ['n', 's', 'e', 'w']
        self.ant = Ant((int)(size / 2), random.choice(random_orientation))
        # self.move_loop(size)

    def init_window(self):
        self.master.title("Langton's Ant")
        self.pack(fill=BOTH, expand=1)

    def make_grid(self, size):
        # size is how many labels in one row
        self.label_grid = []
        x = 10
        y = 10
        for i in range(size):
            self.label_grid.append([])
            # each row
            for z in range(size):
                # each col
                our_label = OurLabel(self.master, width=2, height=1,
                                     borderwidth=2, relief="solid")
                our_label.place(x=x, y=y)
                # create and place Label object on board
                self.label_grid[i].append(our_label)
                x += 25
            x = 10
            y += 25

    def move_loop(self, size):
        # we will call all iterations of algorithm here
        pos = self.ant.location
        if pos[0] >= size or pos[1] >= size or pos[0] < 0 or pos[1] < 0:
            # check for ant out of bounds
            self._close()
        curr_label = self.label_grid[pos[1]][pos[0]]
        left_or_right = 0 if curr_label.visited else 1
        # move left (0) if we have already visited
        self.ant.move(left_or_right)
        curr_label.set_background()
        # change background to show if we've visited or not

    def _close(self):
        print("Out of bounds!")
        self.master.destroy()
        quit()

def move_loop(root, app, size, rate):
    app.move_loop(size)
    # wait for next frame
    root.after((int)(1000/rate), move_loop, root, app, size, rate)

if __name__ == '__main__':
    root = Tk()
    size = (int)(sys.argv[1]) if sys.argv[1] else 8
    # width and height of board is second command argument (default: 8)
    rate = (int)(sys.argv[2]) if sys.argv[2] else 5
    # rate that the ant moves on board is third command argument (default: 5 moves / second)
    if size % 2 == 0:
        size -= 1
    if size < 3:
        size = 3
    # grid needs to be at least 9 squares and always odd number of rows/columns
    # this allows us to start directly in the middle of the board
    root.geometry("%dx%d" % (size * 29, size * 29))
    app = Window(root, size)
    root.after(1000, move_loop, root, app, size, rate)
    root.mainloop()
