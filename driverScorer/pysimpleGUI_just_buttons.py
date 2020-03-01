# Simple path fixes
import os
import sys

import PySimpleGUI as sg
import matplotlib

print("matplotlib sersion: {}".format(matplotlib.__version__))
cwd = os.getcwd()
sys.path.insert(0, cwd)
import driverScorer.driver_scoorer as drvr_scrr

LOGTARGET = "CSV"
# LOGTARGET = "CONSOLE"
driver_scorer = drvr_scrr.DrivingScorer(LOGTARGET, is_mock=False)


def start_recording(label: str):
    driver_scorer.start(label)


# GUI section
sg.theme('DarkAmber')  # Add a touch of color
FONT = ('Helvetica', 20)
SCORESIZING = (20, 3)
LARGEBUTTONSIZE = (8, 3)
SMALLBUTTONSIZE = (16, 2)
WINDOWWIDTH = 500
WINDOWHEIGHT = 320

# plt.style.use('ggplot')  # matplotlib visual style setting
# fig, axs = plt.subplots(1, 1, figsize=(4, 3.5))
# cmap = plt.cm.Set1

# prepping for visualization
# mpu6050_str = ['accel-x', 'accel-y', 'accel-z', 'gyro-x', 'gyro-y', 'gyro-z']
# AK8963_str = ['mag-x', 'mag-y', 'mag-z']

# fig = Figure(figsize=(10, 6), dpi=45)
# ax = fig.add_subplot(111)
# ax.set_xlabel("Time")
# ax.set_ylabel("Grade")
# ax.grid()

# All the stuff inside your window.
column1 = [
    [sg.Text(size=SMALLBUTTONSIZE), sg.Text('Who drives?', justification='center', font=FONT),
     sg.Text(size=SMALLBUTTONSIZE)],
]
layout = [
    [sg.Column(column1, justification='center')],
    [sg.Text(size=SMALLBUTTONSIZE)],
    [sg.Button('Gal', key="gal", size=LARGEBUTTONSIZE, button_color=('black', 'light sky blue'), font=FONT),
     sg.Button('Rivka', key='rivka', size=LARGEBUTTONSIZE, button_color=('black', 'spring green'), font=FONT),
     sg.Button('Other', key='other', size=LARGEBUTTONSIZE, button_color=('black', 'light pink'), font=FONT)]
]

# Create the Window
window = sg.Window('DrivingScorer', layout, size=(WINDOWWIDTH, WINDOWHEIGHT))


def handle_start_recording(event):
    global window
    recording_window = [
        # [sg.Canvas(size=(WINDOWWIDTH - 20, WINDOWHEIGHT - 40), key='canvas')],
        [sg.Text(size=SMALLBUTTONSIZE)],
        [sg.Text('CURRENT SCORE: ', size=SCORESIZING, font=FONT),
         sg.Text('before', key='-CURRENT_SCORE-', size=SCORESIZING, font=FONT)],
        [sg.Text('AVERAGE SCORE: ', size=SCORESIZING, font=FONT),
         sg.Text('before', key='-AVERAGE_SCORE-', size=SCORESIZING, font=FONT)],
        [sg.Cancel(font=FONT)],
        [sg.Text(size=SMALLBUTTONSIZE)]
    ]

    window.close()

    window = sg.Window('Recording data, higher is better.', recording_window, size=(WINDOWWIDTH, WINDOWHEIGHT))
    window.Finalize()  # needed to access the canvas element prior to reading the window

    start_recording(event)  # Start driving_scorer

    # canvas_elem = window['canvas']
    # graph = FigureCanvasTkAgg(fig, master=canvas_elem.TKCanvas)
    # canvas = canvas_elem.TKCanvas

    while True:
        event, values = window.read(timeout=1)

        if event == 'Exit' or event == 'Cancel' or event is None:
            return
        #
        # axs.cla()
        # axs.grid()
        #
        # a1].cla()
        # a1].grid()

        current_score_arr, t_vec = driver_scorer.get_raw_data()

        # axs.plot(t_vec, current_score_arr[:, 0], label=mpu6050_str[0], color=cmap(0))
        # axs.plot(t_vec, current_score_arr[:, 1], label=mpu6050_str[1], color=cmap(1))
        # axs.plot(t_vec, current_score_arr[:, 2], label=mpu6050_str[2], color=cmap(2))
        # axs.legend(bbox_to_anchor=(1.12, 0.9))
        # axs.set_ylabel('Acceleration [g]', fontsize=10)

        # axs[1].plot(t_vec, current_score_arr[:, 3], label=mpu6050_str[3], color=cmap(3))
        # axs[1].plot(t_vec, current_score_arr[:, 4], label=mpu6050_str[4], color=cmap(4))
        # axs[1].plot(t_vec, current_score_arr[:, 5], label=mpu6050_str[5], color=cmap(5))
        # axs[1].legend(bbox_to_anchor=(1.12, 0.9))
        # axs[1].set_ylabel('Angular Vel. [dps]', fontsize=10)

        # fig.align_ylabels(axs)
        #
        # graph.draw()
        # figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds
        # figure_w, figure_h = int(figure_w), int(figure_h)
        # photo = Tk.PhotoImage(master=canvas, width=figure_w, height=figure_h)
        #
        # canvas.create_image(WINDOWWIDTH / 2, WINDOWHEIGHT / 2, image=photo)
        #
        # figure_canvas_agg = FigureCanvasAgg(fig)
        # figure_canvas_agg.draw()
        #
        # tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)

        current_score, average_score = driver_scorer.get_scoring()
        window['-CURRENT_SCORE-'].update(current_score)
        window['-AVERAGE_SCORE-'].update(average_score)


# Event Loop to process "events" and get the "values" of the inputs
event, values = window.read()
handle_start_recording(event)

driver_scorer.stop()
window.close()
