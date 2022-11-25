from tkinter import *
from tkinter import messagebox
import time
import random


tk = Tk()
app_running = True

size_canvas_x = 600
size_canvas_y = 600
s_x = s_y = 10 # size of the game board
step_x = size_canvas_x // s_x # step by the horizontal
step_y = size_canvas_y // s_y # step by the vertical
size_canvas_x = step_x * s_x
size_canvas_y = step_y * s_y

menu_x = 250

ships = 10 # max count of ships
ship_len1 = 1 # the length for the 1th type of ships
ship_len2 = 2 # the length for the 2th type of ships
ship_len3 = 3 # the length for the 3th type of ships
ship_len4 = 4 # the length for the 4th type of ships

enemy_ships = [[0 for i in range(s_x+1)] for i in range(s_y+1)]




def on_closing():
    global app_running
    if messagebox.askokcancel("Exit the Game", "Do you want to exit the Game?"):
        app_running = False
        tk.destroy()


tk.protocol("WM_DELETE_WINDOW", on_closing)
tk.title("Lode game")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=size_canvas_x+menu_x, height=size_canvas_y, bg='#292929', bd=0, highlightthickness=0)
canvas.create_rectangle(0, 0, size_canvas_x, size_canvas_y, fill="#3D3D3D")
canvas.pack()
tk.update()


def draw_table():
    for i in range(0, s_x + 1):
        canvas.create_line(step_x * i, 0, step_x * i, size_canvas_y)
    for i in range(0, s_y + 1):
        canvas.create_line(0, step_y * i, size_canvas_x,  step_y * i)
        

draw_table()


def button_generate_ships():
    pass

def button_generate_map():
    pass


b0 = Button(tk, bg='#7C7CFC', text="Generate locations for ships", command = button_generate_ships)
b0.place(x = size_canvas_x+20, y = 30)

b1 = Button(tk, bg='#9090EE', text="Generate the map again!", command = button_generate_map)
b1.place(x = size_canvas_x+20, y = 70)


def add_to_all(event):
    _type = 0 # for LMB
    if event.num == 3:
        _type = 1 # for RMB
    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()
    ip_x = mouse_x // step_x
    ip_y = mouse_y // step_y
    print (ip_x, ip_y, "_type:", _type)
    


canvas.bind_all("<Button-1>", add_to_all) # left button of mouse (LMB)
canvas.bind_all("<Button-3>", add_to_all) # right button of mouse (RMB)


def generate_ships():
    global enemy_ships
    ships_list = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
    sum_1_all_ships = sum(ships_list)
    sum_1_enemy = 0;
    
    
    
    
    #while sum_1_enemy != sum_1_all_ships:
    #    pass


generate_ships()


while app_running:
    if app_running:
        tk.update_idletasks()
        tk.update()
    time.sleep(0.005)
