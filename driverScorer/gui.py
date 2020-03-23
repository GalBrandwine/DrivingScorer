# Simple path fixes
import os
import pickle
import sys

import PySimpleGUI as sg

# print("matplotlib sersion: {}".format(matplotlib.__version__))

cwd = os.getcwd()
sys.path.insert(0, cwd)
import driverScorer.driver_scoorer as drvr_scrr

LOGTARGET = "CSV"
# LOGTARGET = "CONSOLE"
driver_scorer = drvr_scrr.DrivingScorer(LOGTARGET, use_case="simulator")

users_average_dict = {
    "gal": 6.0,
    "rivka": 6.0,
    "other": 6.0
}


def start_recording(label: str):
    driver_scorer.start(label)


def store_user_average(label: str, current_average: float):
    """
    Store user average to disk.
    :param label:
    :return:
    """
    users_average_dict[label] = current_average
    pickle.dump(users_average_dict, open("users_average.p", "wb"))


def set_average(label):
    """
    Get average for this user
    :param label: str
    :return:
    """

    driver_scorer.set_average(users_average_dict[label])
    pass


font_colors = ['light sky blue', 'spring green', 'light pink']

# GUI section
sg.theme('DarkAmber')  # Add a touch of color
FONT = ('Helvetica', 20)
SCORESIZING = (20, 3)
LARGEBUTTONSIZE = (8, 3)
SMALLBUTTONSIZE = (16, 2)
WINDOWWIDTH = 500
WINDOWHEIGHT = 320

# All the stuff inside your window.
column1 = [
    [sg.Text(size=SMALLBUTTONSIZE), sg.Text('Who drives?', justification='center', font=FONT),
     sg.Text(size=SMALLBUTTONSIZE)],
]

buttons = []
for user, font_color in zip(users_average_dict.keys(), font_colors):
    buttons.append(
        sg.Button(user.capitalize(), key=user, size=LARGEBUTTONSIZE, button_color=('black', font_color), font=FONT), )

layout = [
    [sg.Column(column1, justification='center')],
    [sg.Text(size=SMALLBUTTONSIZE)],
    buttons,
]

# Create the Window
window = sg.Window('DrivingScorer', layout, size=(WINDOWWIDTH, WINDOWHEIGHT))


def handle_start_recording(label):
    global window
    recording_window = [
        [sg.Text(size=SMALLBUTTONSIZE)],
        [sg.Text('CURRENT SCORE: ', size=SCORESIZING, font=FONT),
         sg.Text('Warming_up..', key='-CURRENT_SCORE-', size=SCORESIZING, font=FONT)],
        [sg.Text('AVERAGE SCORE: ', size=SCORESIZING, font=FONT),
         sg.Text('Warming_up..', key='-AVERAGE_SCORE-', size=SCORESIZING, font=FONT)],
        [sg.Cancel("Done", font=FONT)],
        [sg.Text(size=SMALLBUTTONSIZE)]
    ]

    window.close()

    window = sg.Window('Recording data, higher is better.', recording_window, size=(WINDOWWIDTH, WINDOWHEIGHT))
    # window.Finalize()  # needed to access the canvas element prior to reading the window

    user_name = label
    set_average(user_name)
    start_recording(user_name)  # Start driving_scorer

    average_score = 6
    while True:
        label, values = window.read(timeout=1)

        warm_up_time_left = driver_scorer.get_warm_up_time_left()
        if warm_up_time_left > 0:
            window['-CURRENT_SCORE-'].update("init {}".format(warm_up_time_left))
            window['-AVERAGE_SCORE-'].update("init {}".format(warm_up_time_left))
        else:
            current_score, average_score = driver_scorer.get_scoring()
            window['-CURRENT_SCORE-'].update(current_score)
            window['-AVERAGE_SCORE-'].update(average_score)

        if label == 'Exit' or label == 'Done' or label is None:
            store_user_average(user_name, average_score)
            return


if __name__ == "__main__":

    filepath = cwd + "/users_average.p"
    try:
        # Upon start-up load saved users_average.
        users_average_dict = pickle.load(open(filepath, "rb"))
        print(users_average_dict)
    except FileNotFoundError as err:
        # Create and save
        pickle.dump(users_average_dict, open(filepath, "wb"))

    # Event Loop to process "events" and get the "values" of the inputs
    event, values = window.read()
    handle_start_recording(event)

    driver_scorer.stop()
    window.close()
