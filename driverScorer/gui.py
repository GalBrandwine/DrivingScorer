# Simple path fixes
import os
import pickle
import sys
from typing import List

import PySimpleGUI as sg
from PySimpleGUI import Button

cwd = os.getcwd()
sys.path.insert(0, cwd)
import driverScorer.driver_scoorer as drvr_scrr

LOGTARGET = "CSV"
# LOGTARGET = "CONSOLE"
driver_scorer = drvr_scrr.DrivingScorer(LOGTARGET, use_case="simulator")


def start_recording(label: str):
    driver_scorer.start(label)


def store_user_average_and_samples_num(users_average_dict_input: dict):
    """
    Store user average to disk.
    :param label:
    :param current_average_and_samples:
    :param users_average_dict_input:
    :return:
    """

    pickle.dump(users_average_dict_input, open("users_average.p", "wb"))


def set_average_and_samples_num(user_accomulating_average_and_scores_num: dict):
    """
    Get average for this user
    :param user_accomulating_average_and_scores_num:
    :return:
    """

    driver_scorer.set_average_and_samples_num(user_accomulating_average_and_scores_num)


# GUI section
sg.theme('DarkAmber')  # Add a touch of color
FONT = ('Helvetica', 20)
SCORESIZING = (20, 3)
LARGEBUTTONSIZE = (8, 3)
SMALLBUTTONSIZE = (16, 2)
WINDOWWIDTH = 500
WINDOWHEIGHT = 320


def handle_start_recording(label, users_average_dict_input):
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

    set_average_and_samples_num(users_average_dict_input[user_name])
    start_recording(user_name)  # Start driving_scorer

    average_score = 6
    while True:
        label, values = window.read(timeout=1)

        warm_up_time_left = driver_scorer.get_warm_up_time_left()
        if warm_up_time_left > 0:
            window['-CURRENT_SCORE-'].update("init {}".format(warm_up_time_left))
            window['-AVERAGE_SCORE-'].update("init {}".format(warm_up_time_left))
        else:
            current_score, average_score_and_samples = driver_scorer.get_scoring()
            window['-CURRENT_SCORE-'].update(current_score)
            window['-AVERAGE_SCORE-'].update(average_score_and_samples[0])
            users_average_dict_input[user_name] = average_score_and_samples

        if label == 'Exit' or label == 'Done' or label is None:
            store_user_average_and_samples_num(users_average_dict_input)
            return


if __name__ == "__main__":

    filepath = cwd + "/users_average.p"
    try:
        # Upon start-up load saved users_average.
        users_average_dict = pickle.load(open(filepath, "rb"))
        print(users_average_dict)
    except FileNotFoundError as err:
        # Create and save
        users_average_dict = {  # Key: driver_name  , Value: [average, num_of_samples]
            "gal": [6.0, 1],
            "rivka": [6.0, 1],
            "other": [6.0, 1]
        }
        pickle.dump(users_average_dict, open(filepath, "wb"))

    # All the stuff inside your window.
    column1 = [
        [sg.Text(size=SMALLBUTTONSIZE), sg.Text('Who drives?', justification='center', font=FONT),
         sg.Text(size=SMALLBUTTONSIZE)],
    ]

    font_colors = ['light sky blue', 'spring green', 'light pink']
    buttons: List[Button] = []
    for user, font_color in zip(users_average_dict.keys(), font_colors):
        buttons.append(
            sg.Button(user.capitalize(), key=user, size=LARGEBUTTONSIZE, button_color=('black', font_color),
                      font=FONT), )

    layout = [
        [sg.Column(column1, justification='center')],
        [sg.Text(size=SMALLBUTTONSIZE)],
        buttons,
    ]

    # Create the Window
    window = sg.Window('DrivingScorer', layout, size=(WINDOWWIDTH, WINDOWHEIGHT))

    # Event Loop to process "events" and get the "values" of the inputs
    event, values = window.read()
    handle_start_recording(event, users_average_dict)

    driver_scorer.stop()
    window.close()
