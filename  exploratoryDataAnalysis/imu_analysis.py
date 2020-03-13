import PySimpleGUI as sg
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def fix_time_stamp(df_input: pd) -> pd:
    df_input['timestamp'] = pd.to_datetime(df_input['timestamp'],
                                           format='%H:%M:%S.%f')  # Change timestamp format to something pd understand

    df_input['timestamp'] = df_input['timestamp'] - df_input['timestamp'].iloc[
        0]  # Change from timestamp to time-passed-from-beginning
    return add_elapsed_col(df_input)


def add_elapsed_col(df_input: pd) -> pd:
    df_input['elapsed'] = df_input['timestamp'] / np.timedelta64(1, 's')  # Change from milisec to seconds
    return df_input


def fig_acc_xyz(df_input: pd):
    fig = make_subplots(rows=3, cols=1,
                        shared_xaxes=True,

                        subplot_titles=("aX", "aY", "aZ"))

    fig.add_trace(
        go.Scatter(x=df_input['elapsed'], y=df_input['ax'], name="ax"),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=df_input['elapsed'], y=df_input['ay'], name="ay"),
        row=2, col=1
    )

    fig.add_trace(
        go.Scatter(x=df_input['elapsed'], y=df_input['az'], name="az"),
        row=3, col=1
    )

    # Update xaxis properties
    fig.update_xaxes(title_text="Elapsed time [sec]", row=3, col=1)

    #
    # # Update yaxis properties
    # fig.update_yaxes(title_text="yaxis 1 title", row=1, col=1)
    # fig.update_yaxes(title_text="yaxis 2 title", range=[40, 80], row=1, col=2)
    # fig.update_yaxes(title_text="yaxis 3 title", showgrid=False, row=2, col=1)
    # fig.update_yaxes(title_text="yaxis 4 title", row=2, col=2)

    fig.update_layout(title_text="IMU data")
    fig.show()


def fig_gyro_xyz(df_input: pd):
    fig = make_subplots(rows=3, cols=1,
                        shared_xaxes=True,

                        subplot_titles=("gX", "gY", "gZ"))

    fig.add_trace(
        go.Scatter(x=df_input['elapsed'], y=df_input['gx'], name="gx"),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=df_input['elapsed'], y=df_input['gy'], name="gy"),
        row=2, col=1
    )

    fig.add_trace(
        go.Scatter(x=df_input['elapsed'], y=df_input['gz'], name="gz"),
        row=3, col=1
    )

    # Update xaxis properties
    fig.update_xaxes(title_text="Elapsed time [sec]", row=3, col=1)

    fig.update_layout(title_text="IMU data")
    fig.show()


if __name__ == "__main__":
    csv_name = sg.PopupGetFile('Enter the desired record for EDA')
    # reading csv file
    df = pd.read_csv(csv_name)

    df = fix_time_stamp(df)
    fig_acc_xyz(df)
    fig_gyro_xyz(df)
