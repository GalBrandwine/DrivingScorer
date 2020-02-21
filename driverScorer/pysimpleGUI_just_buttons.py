import tkinter as Tk

import PySimpleGUI as sg
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
from matplotlib.figure import Figure

import driverScorer.driver_scoorer as drvr_scrr

LOGTARGET = "CSV"
# LOGTARGET = "CONSOLE"
driver_scorer = drvr_scrr.DrivingScorer(LOGTARGET, is_mock=True)


def start_recording(label: str):
    driver_scorer.start(label)


# GUI section
sg.theme('DarkAmber')  # Add a touch of color
LARGEBUTTONSIZE = (16, 6)
SMALLBUTTONSIZE = (16, 2)
WINDOWWIDTH = 500
WINDOWHEIGHT = 320

fig = Figure(figsize=(10, 6), dpi=45)

ax = fig.add_subplot(111)
ax.set_xlabel("X axis")
ax.set_ylabel("Y axis")
ax.grid()

# All the stuff inside your window.
column1 = [
    [sg.Text(size=SMALLBUTTONSIZE), sg.Text('Who drives?', justification='center'), sg.Text(size=SMALLBUTTONSIZE)],
]
layout = [
    [sg.Column(column1, justification='center')],
    [sg.Text(size=SMALLBUTTONSIZE)],
    [sg.Button('Gal', key="gal", size=LARGEBUTTONSIZE, button_color=('black', 'light sky blue')),
     sg.Button('Rivka', key='rivka', size=LARGEBUTTONSIZE, button_color=('black', 'spring green')),
     sg.Button('Other', key='other', size=LARGEBUTTONSIZE, button_color=('black', 'light pink'))]
]

# Create the Window
window = sg.Window('DrivingScorer', layout, size=(WINDOWWIDTH, WINDOWHEIGHT))


def handle_start_recording(event):
    global window
    recording_window = [
        [sg.Canvas(size=(WINDOWWIDTH - 20, WINDOWHEIGHT - 40), key='canvas')],
        [sg.Cancel()]
    ]

    window.close()

    window = sg.Window('Recording', recording_window, size=(WINDOWWIDTH, WINDOWHEIGHT))
    window.Finalize()  # needed to access the canvas element prior to reading the window

    start_recording(event)

    canvas_elem = window['canvas']

    graph = FigureCanvasTkAgg(fig, master=canvas_elem.TKCanvas)
    canvas = canvas_elem.TKCanvas
    begin_index = 0

    while (True):
        event, values = window.read(timeout=1)
        if event == 'Exit' or event == 'Cancel' or event is None:
            return


        ax.cla()
        ax.grid()
        current_score_arr = driver_scorer.get_score_arr()

        if len(current_score_arr) is 0:
            print("stop here")

        ax.plot(range(len(current_score_arr)), current_score_arr, color='purple')
        graph.draw()
        figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds
        figure_w, figure_h = int(figure_w), int(figure_h)
        photo = Tk.PhotoImage(master=canvas, width=figure_w, height=figure_h)

        canvas.create_image(WINDOWWIDTH / 2, WINDOWHEIGHT / 2, image=photo)

        figure_canvas_agg = FigureCanvasAgg(fig)
        figure_canvas_agg.draw()

        tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)


# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Cancel', 'Exit'):  # if user closes window or clicks cancel
        break

    handle_start_recording(event)

driver_scorer.stop()
window.close()
