import math

import PySimpleGUI as sg

# 320 x 240
WINDOWWIDTH = 320
WINDOWHEIGHT = 240

layout = [[sg.Graph(canvas_size=(WINDOWWIDTH, WINDOWHEIGHT), graph_bottom_left=(-105, -105), graph_top_right=(105, 105),
                    background_color='white', key='graph', tooltip='This is a cool graph!')], [sg.Cancel()]]

window = sg.Window('Graph of Sine Function', layout, grab_anywhere=True).Finalize()
window.Maximize()
# window = sg.Window('Window Title', layout, no_titlebar=True, location=(0,0), size=(800,600), keep_on_top=True)
graph = window['graph']

# Draw axis    
graph.DrawLine((-100, 0), (100, 0))
graph.DrawLine((0, -100), (0, 100))

for x in range(-100, 101, 20):
    graph.DrawLine((x, -3), (x, 3))
    if x != 0:
        graph.DrawText(x, (x, -10), color='green')

for y in range(-100, 101, 20):
    graph.DrawLine((-3, y), (3, y))
    if y != 0:
        graph.DrawText(y, (-10, y), color='blue')

    # Draw Graph
for x in range(-100, 100):
    y = math.sin(x / 20) * 50
    graph.DrawCircle((x, y), 1, line_color='red', fill_color='red')

event, values = window.read()
