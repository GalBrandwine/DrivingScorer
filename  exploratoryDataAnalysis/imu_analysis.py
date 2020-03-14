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


def fig_acc_xyz(df_input: pd, given_title: str):
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

    fig.update_layout(title_text=given_title)
    fig.show()


def fig_gyro_xyz(df_input: pd, given_title: str):
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

    fig.update_layout(title_text=given_title)
    fig.show()


def fig_grades(grades, given_title):
    fig = go.Figure(
        data=go.Scatter(x=grades["time"], y=grades["grade"]),
        layout=go.Layout(
            title=go.layout.Title(text=given_title)
        )
    )
    fig.show()


def calculate_std(df: pd, sample_time=-1) -> pd.DataFrame:
    if sample_time > -1:
        temp = df[df['elapsed'] <= sample_time]
        std = temp.std()
        return std
    return df.std()


def grader(df_std_remove: pd, window: int) -> int:
    pass


# windowed: pd.DataFrame = df_std_remove.copy()
#
# min_max_scaler = preprocessing.MinMaxScaler()
# scaled = min_max_scaler.fit_transform(windowed.iloc[:, 1:7])
#
# # windowed.iloc[:, 1:7] = scaled
# # windowed['elapsed'] = df_std_remove['elapsed'] - df_std_remove['elapsed'].iloc[0]  # Fix timing
# # windowed = windowed[windowed['elapsed'] < window]  # Filter
# #
# # # win_size =  [windowed['elapsed'] <= window].count("True")
# # # res = windowed.rolling(len(win_size)).mean()
#
# axe_weight = (100 / 6.0)  # Each weight is 16.6%, the sum of all weights is 100%
# # axes_weights = [axe_weight * 4, axe_weight / 4, axe_weight / 4, axe_weight, axe_weight / 4, axe_weight / 4]
# axes_weights = [axe_weight, axe_weight, axe_weight, axe_weight, axe_weight, axe_weight]
#
# g = windowed.groupby('ax')
# res = windowed.value / g.value.transform("sum") * axes_weights[0]
#
# avarage = windowed.mean()
# # weighted = avarage.iloc[1:7] * axes_weights
#
#
# # scaled = min_max_scaler.fit_transform(windowed.iloc[:, 1:7])
# # df = pd.DataFrame(scaled, columns=['ax', 'ay', 'az', 'gx', 'gy', 'gz'])
#
# res = windowed.iloc[:, 1:7].mean() * axes_weights
# return res.sum()


def calc_window_size(std_removed: pd.DataFrame, window_size_sec: int) -> int:
    """

    :param std_removed:
    :param window_size_sec:
    :return: Number of rows that represent 'window_size_sec'
    """
    df = std_removed.copy()
    df['elapsed'] = df['elapsed'] - df['elapsed'].iloc[0]  # Fix timing
    return df[df['elapsed'] < window_size_sec].shape[0]


def calc_sliding_window_and_fig(std_removed_input):

    grades: pd.DataFrame = pd.DataFrame(columns=["time", "grade"])
    window_size_sec = 1.0
    window_size_rows = calc_window_size(std_removed_input, window_size_sec)
    mean = std_removed_input.rolling(window_size_rows, win_type='triang').mean()

    #
    # for index, row in std_removed.iterrows():
    #     grade = grader(std_removed.iloc[line:], window=window_size)
    #     end_of_window = std_removed.iloc[line]['elapsed']
    #
    #     grades.loc[line, 'time'] = end_of_window + window_size / 2
    #     grades.loc[line, 'grade'] = grade
    #
    #     line = line + 1

    # mean[mean.isna()] = 0

    # using numpy average() method

    axes_weights = pd.DataFrame({'wax': [10], 'way': [10], 'waz': [10], 'wgx': [10], 'wgy': [10], 'wgz': [10]})


    fig_acc_xyz(mean, given_title="IMU data (sliding window mean): acc XYZ")
    fig_gyro_xyz(mean, given_title="IMU data (sliding window mean): gyro XYZ")

    df_norm = mean.iloc[:,:6]
    df_norm -= df_norm.min()  # equivalent to df = df - df.min()
    df_norm /= df_norm.max()  # equivalent to df = df / df.max()

    # df_norm = (mean - mean.mean()) / (mean.max() - mean.min())
    df_norm['elapsed'] = mean['elapsed']

    # g = df_norm.groupby('Date')
    #
    # df_norm.value / g.value.transform("sum") * axes_weights.wt

    fig_acc_xyz(df_norm, given_title="IMU data (sliding window mean normalized): acc XYZ")
    fig_gyro_xyz(df_norm, given_title="IMU data (sliding window mean normalized): gyro XYZ")

    # fig_grades(grades, given_title="IMU grades")


if __name__ == "__main__":
    csv_name = sg.PopupGetFile('Enter the desired record for EDA')
    # reading csv file
    df = pd.read_csv(csv_name)

    df = fix_time_stamp(df)
    fig_acc_xyz(df, given_title="IMU data: acc XYZ")
    fig_gyro_xyz(df, given_title="IMU data: gyro XYZ")

    std_per_axe = calculate_std(df, sample_time=10)
    print(std_per_axe)
    std_removed = df.iloc[:, :7] - std_per_axe[:7]
    std_removed['elapsed'] = df['elapsed']

    fig_acc_xyz(std_removed, given_title="IMU data: acc XYZ (std_removed)")
    fig_gyro_xyz(std_removed, given_title="IMU data: gyro XYZ (std_removed)")

    calc_sliding_window_and_fig(std_removed)
