from random import random
from tkinter import Tk, Button, Label, Canvas, Entry, IntVar, Event
from functools import partial
import numpy as np


DARK_THEME = ("black", "grey10", "cadetblue1", "cadetblue2")
LIGHT_THEME = ("white", "grey90", "green", "seagreen")

DEFAULT_TITLE = "Sid Ali's Game of Life"

DEFAULT_TIP = "Click on any cell to turn it on/off."
GLIDERS_TIP = "Try to destroy the gliders by clicking on them !"

DEFAULT_LENGTH = 40
DEFAULT_WIDTH = 50
DEFAULT_CELL_SIZE = 15
DEFAULT_SURVIVAL_RATE = 0.2

DEFAULT_DELAY = 90
DEFAULT_DELAY_STEP = 40
MAX_DELAY = 150
MIN_DELAY = 10


def neighborhood(cell):
    north = ((cell[0] - 1) % width, cell[1])
    south = ((cell[0] + 1) % width, cell[1])
    east = (cell[0], (cell[1] + 1) % length)
    west = (cell[0], (cell[1] - 1) % length)
    northwest = ((cell[0] - 1) % width, (cell[1] - 1) % length)
    northeast = ((cell[0] - 1) % width, (cell[1] + 1) % length)
    southwest = ((cell[0] + 1) % width, (cell[1] - 1) % length)
    southeast = ((cell[0] + 1) % width, (cell[1] + 1) % length)
    return [north, south, east, west, northwest, northeast, southwest, southeast]


def alive_neighbors(grid, cell):
    return sum(grid[neighbor] for neighbor in neighborhood(cell))


def update_grid():
    global grid
    new_grid = np.zeros((width, length))
    for row in range(width):
        for column in range(length):
            neighbors = alive_neighbors(grid, (row, column))
            if grid[row, column] == 1 and neighbors in [2, 3]:
                new_grid[row, column] = 1
            if grid[row, column] == 0 and neighbors == 3:
                new_grid[row, column] = 1
    grid = new_grid


def update_field():
    if night_mode is True:
        theme = DARK_THEME
    else:
        theme = LIGHT_THEME
    field.delete("all")
    for row in range(width):
        for column in range(length):
            field.create_rectangle(
                row * cell_size,
                column * cell_size,
                (row + 1) * cell_size,
                (column + 1) * cell_size,
                fill=theme[0 if grid[row, column] == 0 else 2],
                outline=theme[1 if grid[row, column] == 0 else 3],
                width=1,
                tags=f"cell-{row}-{column}",
            )


def update_game():
    global counter
    counter += 1
    game.title(f"[{counter}] RUNNING - {DEFAULT_TITLE}")
    update_grid()
    update_field()


def apply_changes(length_entry, width_entry, cell_size_entry, survival_rate_entry):
    global length, width, cell_size, survival_rate
    length = int(length_entry.get())
    width = int(width_entry.get())
    cell_size = int(cell_size_entry.get())
    survival_rate = float(survival_rate_entry.get())
    if width > 0 and length > 0 and cell_size > 0 and 0 <= survival_rate <= 1:
        apply_changes_signal.set(1)


def disable_event():
    pass


def clicked(cell, event: Event):
    if night_mode is True:
        theme = DARK_THEME
    else:
        theme = LIGHT_THEME
    field.itemconfig(
        f"cell-{cell[0]}-{cell[1]}",
        fill=theme[0 if grid[cell] == 1 else 2],
        outline=theme[1 if grid[cell] == 1 else 3],
    )
    grid[cell] = 1 - grid[cell]


def randomize():
    for row in range(width):
        for column in range(length):
            grid[row, column] = random() < survival_rate
    update_field()
    change_tip()


def gliders():
    global gliders_is_clicked, grid
    gliders_is_clicked = True
    grid = np.zeros((width, length))
    reset_grid()
    for row in range(max(1, width // 10)):
        for column in range(max(1, length // 10)):
            grid[1 + 10 * row, 1 + 10 * column] = 1
            grid[2 + 10 * row, 2 + 10 * column] = 1
            grid[2 + 10 * row, 3 + 10 * column] = 1
            grid[3 + 10 * row, 2 + 10 * column] = 1
            grid[1 + 10 * row, 3 + 10 * column] = 1
    update_field()
    change_tip()
    gliders_is_clicked = False


def switch_theme():
    global night_mode
    night_mode = not night_mode
    if night_mode is False:
        switch_theme_button.configure(text="Night mode")
    else:
        switch_theme_button.configure(text="Day mode")
    update_field()


def start():
    global game_started
    game_started = True
    update_game()
    game.after_id = game.after(round(delay), start)
    start_button.config(state="disabled")
    stop_button.config(state="normal")


def stop():
    game.after_cancel(game.after_id)
    start_button.config(state="normal")
    stop_button.config(state="disabled")
    game.title(f"[{counter}] ON HOLD - {DEFAULT_TITLE}")


def reset_grid():
    global grid, counter
    counter = 0
    grid = np.zeros((width, length))
    update_field()
    if game_started:
        stop()
    game.title(f"READY - {DEFAULT_TITLE}")
    change_tip()


def faster_pace():
    global delay
    delay = max(MIN_DELAY, delay - DEFAULT_DELAY_STEP)
    slower_pace_button.config(state="normal")
    if delay == MIN_DELAY:
        faster_pace_button.config(state="disabled")
    else:
        faster_pace_button.config(state="normal")


def slower_pace():
    global delay
    delay = min(MAX_DELAY, delay + DEFAULT_DELAY_STEP)
    faster_pace_button.config(state="normal")
    if delay == MAX_DELAY:
        slower_pace_button.config(state="disabled")
    else:
        slower_pace_button.config(state="normal")


def reset_speed():
    global delay
    delay = DEFAULT_DELAY
    slower_pace_button.config(state="normal")
    faster_pace_button.config(state="normal")


def change_tip():
    if gliders_is_clicked:
        tip_label.config(text=GLIDERS_TIP)
    else:
        tip_label.config(text=DEFAULT_TIP)










length = DEFAULT_LENGTH
width = DEFAULT_WIDTH
cell_size = DEFAULT_CELL_SIZE
survival_rate = DEFAULT_SURVIVAL_RATE
delay = DEFAULT_DELAY


counter = 0
game_started = False
night_mode = True
gliders_is_clicked = False


game = Tk()


game.title(DEFAULT_TITLE)
game.eval(f"tk::PlaceWindow . center")
game.protocol("WM_DELETE_WINDOW", disable_event)


game.resizable(False, False)


valid_values_label = Label(game, text="Please enter valid values.")
valid_values_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

length_label = Label(game, text="Length")
length_label.grid(row=1, column=0, padx=5, pady=5)

width_label = Label(game, text="Width")
width_label.grid(row=2, column=0, padx=5, pady=5)

cell_size_label = Label(game, text="Cell size")
cell_size_label.grid(row=3, column=0, padx=5, pady=5)

survival_rate_label = Label(game, text="Survival rate")
survival_rate_label.grid(row=4, column=0, padx=5, pady=5)


length_entry = Entry(game)
length_entry.grid(row=1, column=1, padx=5, pady=5)
length_entry.insert(0, str(length))

width_entry = Entry(game)
width_entry.grid(row=2, column=1, padx=5, pady=5)
width_entry.insert(0, str(width))

cell_size_entry = Entry(game)
cell_size_entry.grid(row=3, column=1, padx=5, pady=5)
cell_size_entry.insert(0, str(cell_size))

survival_rate_entry = Entry(game)
survival_rate_entry.grid(row=4, column=1, padx=5, pady=5)
survival_rate_entry.insert(0, str(survival_rate))


apply_changes_signal = IntVar()
apply_changes_button = Button(game, text="Apply changes", command=partial(apply_changes, length_entry, width_entry, cell_size_entry, survival_rate_entry))
apply_changes_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
apply_changes_button.wait_variable(apply_changes_signal)


apply_changes_button.destroy()


length_entry.destroy()
width_entry.destroy()
cell_size_entry.destroy()
survival_rate_entry.destroy()


valid_values_label.grid_forget()
length_label.grid_forget()
width_label.grid_forget()
cell_size_label.grid_forget()
survival_rate_label.grid_forget()


grid = np.zeros((width, length))
new_grid = np.zeros((width, length))


field = Canvas(game, height=(cell_size) * length + 1, width=(cell_size) * width + 1, borderwidth=0, highlightthickness=0)
field.grid(row=0, column=0, columnspan=3, padx=1, pady=1)


for row in range(width):
    for column in range(length):
        field.tag_bind(f"cell-{row}-{column}", "<Button-1>", partial(clicked, (row, column)))


randomize_button = Button(game, text="Randomize", command=randomize)
randomize_button.grid(row=1, column=0, padx=1, pady=1)
randomize_button.config(width=8)

gliders_button = Button(game, text="Gliders", command=gliders)
gliders_button.grid(row=2, column=0, padx=1, pady=1)
gliders_button.config(width=8)

switch_theme_button = Button(game, text="Day mode", command=switch_theme)
switch_theme_button.grid(row=3, column=0, padx=1, pady=1)
switch_theme_button.config(width=8)

start_button = Button(game, text="Start", command=start)
start_button.grid(row=1, column=1, padx=1, pady=1)
start_button.config(width=20)

stop_button = Button(game, text="Stop", command=stop)
stop_button.grid(row=2, column=1, padx=1, pady=1)
stop_button.config(width=20)
stop_button.config(state="disabled")

reset_grid_button = Button(game, text="Reset grid", command=reset_grid)
reset_grid_button.grid(row=3, column=1, padx=1, pady=1)
reset_grid_button.config(width=20)

faster_pace_button = Button(game, text="Faster pace", command=faster_pace)
faster_pace_button.grid(row=1, column=2, padx=1, pady=1)
faster_pace_button.config(width=8)

slower_pace_button = Button(game, text="Slower pace", command=slower_pace)
slower_pace_button.grid(row=2, column=2, padx=1, pady=1)
slower_pace_button.config(width=8)

reset_speed_button = Button(game, text="Reset speed", command=reset_speed)
reset_speed_button.grid(row=3, column=2, padx=1, pady=1)
reset_speed_button.config(width=8)


tip_label = Label(game, text=DEFAULT_TIP)
tip_label.grid(row=4, column=0, columnspan=3, padx=0, pady=0)


game.title(f"READY - {DEFAULT_TITLE}")
game.eval(f"tk::PlaceWindow . center")
game.protocol("WM_DELETE_WINDOW", quit)


randomize()

game.mainloop()




