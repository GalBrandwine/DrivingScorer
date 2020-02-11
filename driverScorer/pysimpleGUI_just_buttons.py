import PySimpleGUI as sg

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
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Cancel', 'Exit'):  # if user closes window or clicks cancel
        break
    if event == "rivka":
        print(event)
    if event == "gal":
        print(event)
    if event == "other":
        print(event)

    # Update the "output" text element to be the value of "input" element
    # window['-OUTPUT-'].update(values['-IN-'])

window.close()
