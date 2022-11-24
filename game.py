from tkinter import *
from tkinter import messagebox
import time


tk = Tk()
app_running = True

size_canvas_x = 600
size_canvas_y = 600
s_x = s_y = 10 # size of the game board
step_x = size_canvas_x // s_x # step by the horizontal
step_y = size_canvas_y // s_y # step by the vertical
size_canvas_x = step_x * s_x
size_canvas_y = step_y * s_y



def on_closing():
    global app_running
    if messagebox.askokcancel("Exit the Game", "Do you want to exit the Game?"):
        app_running = False
        tk.destroy()

tk.protocol("WM_DELETE_WINDOW", on_closing)
tk.title("Lode game")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=size_canvas_x, height=size_canvas_y, bd=0, highlightthickness=0)
canvas.create_rectangle(0, 0, size_canvas_x, size_canvas_y, fill="white")
canvas.pack()
tk.update()


def draw_table():
    for i in range(0, s_x + 1):
        canvas.create_line(step_x * i, 0, step_x * i, size_canvas_y)
    for i in range(0, s_y + 1):
        canvas.create_line(0, step_y * i, size_canvas_x,  step_y * i)
        




draw_table()


while app_running:
    if app_running:
        tk.update_idletasks()
        tk.update()
    time.sleep(0.005)