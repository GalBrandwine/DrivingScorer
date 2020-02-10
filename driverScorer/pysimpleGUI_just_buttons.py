import PySimpleGUI as sg

sg.theme('DarkAmber')  # Add a touch of color
LARGEBUTTONSIZE = (24, 12)
# All the stuff inside your window.
layout = [[sg.Text('Who drives?',justification='center')],
            [sg.Button('Gal', key="gal", size=LARGEBUTTONSIZE),
            sg.Button('Rivka', key='rivka',size=LARGEBUTTONSIZE),
            sg.Button('Other', key='other',size=LARGEBUTTONSIZE)]
          ]

# Create the Window
window = sg.Window('DrivingScorer', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Cancel', 'Exit'):  # if user closes window or clicks cancel
        break
    print('You entered ', values[0])

window.close()
