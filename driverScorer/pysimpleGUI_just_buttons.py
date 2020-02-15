import PySimpleGUI as sg

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
        [sg.Slider(range=(0x1000, 0x10000), orientation='h', size=(34, 20))],
        [sg.Ok(), sg.Cancel()]
    ]

    window.close()
    window = sg.Window('Recording', recording_window, size=(WINDOWWIDTH, WINDOWHEIGHT))
    start_recording(event)


# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Cancel', 'Exit'):  # if user closes window or clicks cancel
        driver_scorer.stop()
        break

    handle_start_recording(event)

window.close()
