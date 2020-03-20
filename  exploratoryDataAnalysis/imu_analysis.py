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


def fig_grades(grades, given_title, sensor_data=None):
    fig = go.Figure(
        data=go.Scatter(x=grades['time'], y=grades['raw_diff_abs'], name="raw_diff_abs"),
        layout=go.Layout(
            title=go.layout.Title(text=given_title)
        )
    )

    if sensor_data is not None:
        fig.add_trace(
            go.Scatter(x=sensor_data['elapsed'], y=sensor_data['ax'], name="ax"),
        )

        fig.add_trace(
            go.Scatter(x=sensor_data['elapsed'], y=sensor_data['ay'], name="ay"),
        )

        fig.add_trace(
            go.Scatter(x=sensor_data['elapsed'], y=sensor_data['az'], name="az"),
        )
        fig.add_trace(
            go.Scatter(x=sensor_data['elapsed'], y=sensor_data['gx'], name="gx"),
        )

        fig.add_trace(
            go.Scatter(x=sensor_data['elapsed'], y=sensor_data['gy'], name="gy"),
        )

        fig.add_trace(
            go.Scatter(x=sensor_data['elapsed'], y=sensor_data['gz'], name="gz"),
        )
    fig.show()


def calculate_std(df: pd, sample_time=-1) -> pd.DataFrame:
    if sample_time > -1:  # Remove STD of a specific record time ( useful if having a sensor "warm-up" time)
        temp = df[df['elapsed'] <= sample_time]
        std = temp.std()
        return std
    return df.std()  # Remove STD from all sampled data.


def calc_window_size(std_removed: pd.DataFrame, window_size_sec: float) -> int:
    """

    :param std_removed:
    :param window_size_sec:
    :return: Number of rows that represent 'window_size_sec'
    """

    df = std_removed.copy()
    df = df.fillna(0)
    df['elapsed'] = df['elapsed'] - df['elapsed'].iloc[0]  # Fix timing
    return df[df['elapsed'] < window_size_sec].shape[0]


def normalize_data(un_normalized_data) -> pd.DataFrame:
    df = un_normalized_data.copy()
    df = df.iloc[:, 1:7]
    df -= df.min()  # equivalent to df = df - df.min()
    df /= df.max()  # equivalent to df = df / df.max()
    df['elapsed'] = un_normalized_data['elapsed']  # Keep original data
    return df


def calc_mean_using_sliding_window(std_removed_input, window_size_sec_input: float = 1.0) -> pd.DataFrame:
    window_size = window_size_sec_input
    window_size_rows = calc_window_size(std_removed_input, window_size)
    mean = std_removed_input.rolling(window_size_rows, win_type='triang').mean()
    return mean
    # axes_weights = pd.DataFrame({'wax': [10], 'way': [10], 'waz': [10], 'wgx': [10], 'wgy': [10], 'wgz': [10]})


def prepare_fig_df1_and_df2_gyro(df1, df2, df1_trace_title, df2_trace_title, given_title) -> go.Figure:
    fig = make_subplots(rows=3, cols=1,
                        shared_xaxes=True,

                        subplot_titles=("gX", "gY", "gZ"))
    # GX
    # fig.add_trace(
    #     go.Scatter(x=df1['elapsed'], y=df1['gx'], name="gx {}".format(df1_trace_title)),
    #     row=1, col=1
    # )

    fig.add_trace(
        go.Scatter(x=df2['elapsed'], y=df2['gx'], name="gx {}".format(df2_trace_title)),
        row=1, col=1
    )

    # GY
    fig.add_trace(
        go.Scatter(x=df1['elapsed'], y=df1['gy'], name="gy {}".format(df1_trace_title)),
        row=2, col=1
    )

    # fig.add_trace(
    #     go.Scatter(x=df2['elapsed'], y=df2['ay'], name="ay {}".format(df2_trace_title)),
    #     row=2, col=1
    # )

    # GZ
    fig.add_trace(
        go.Scatter(x=df1['elapsed'], y=df1['gz'], name="gz {}".format(df1_trace_title)),
        row=3, col=1
    )

    # fig.add_trace(
    #     go.Scatter(x=df2['elapsed'], y=df2['gz'], name="gz {}".format(df2_trace_title)),
    #     row=3, col=1
    # )
    return fig


def prepare_fig_df1_and_df2_acc(df1, df2, df1_trace_title, df2_trace_title, given_title) -> go.Figure:
    fig = make_subplots(rows=3, cols=1,
                        shared_xaxes=True,

                        subplot_titles=("aX", "aY", "aZ"))
    # AX
    fig.add_trace(
        go.Scatter(x=df1['elapsed'], y=df1['ax'], name="ax {}".format(df1_trace_title)),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=df2['elapsed'], y=df2['ax'], name="ax {}".format(df2_trace_title)),
        row=1, col=1
    )

    # AY
    fig.add_trace(
        go.Scatter(x=df1['elapsed'], y=df1['ay'], name="ay {}".format(df1_trace_title)),
        row=2, col=1
    )

    fig.add_trace(
        go.Scatter(x=df2['elapsed'], y=df2['ay'], name="ay {}".format(df2_trace_title)),
        row=2, col=1
    )

    # AZ
    fig.add_trace(
        go.Scatter(x=df1['elapsed'], y=df1['az'], name="az {}".format(df1_trace_title)),
        row=3, col=1
    )

    fig.add_trace(
        go.Scatter(x=df2['elapsed'], y=df2['az'], name="az {}".format(df2_trace_title)),
        row=3, col=1
    )
    return fig


def fig_df1_and_df2(df1, df2, sensor: str, df1_trace_title, df2_trace_title, given_title):
    if sensor == "acc":
        fig = prepare_fig_df1_and_df2_acc(df1, df2, df1_trace_title, df2_trace_title, given_title)

    if sensor == "gyro":
        fig = prepare_fig_df1_and_df2_gyro(df1, df2, df1_trace_title, df2_trace_title, given_title)

    # # Update xaxis properties
    fig.update_xaxes(title_text="Elapsed time [sec]", row=3, col=1)
    fig.update_layout(title_text=given_title)
    fig.show()


def remove_std(df: pd.DataFrame, calculated_std) -> pd.DataFrame:
    std_removed = df.copy()
    std_removed = std_removed.iloc[:, :7] - calculated_std[:7]  # Remove std from sensor data only
    return std_removed


def calc_grades(mean_normalized_data: pd.DataFrame) -> pd.DataFrame:
    """

    :param mean_normalized_data:
    :return:
    """
    # window_size_sec = 0.2
    # window_size_rows = calc_window_size(mean_normalized_data, window_size_sec)

    to_be_graded = mean_normalized_data.copy()

    grades: pd.DataFrame = pd.DataFrame(
        columns=["time", "data_sum", "data_sum_diff_abs", "raw_diff_abs"])
    grades["time"] = to_be_graded["elapsed"]

    # mean = to_be_graded.rolling(window_size_rows, win_type='triang').mean()
    mean_normalized2 = to_be_graded.copy()
    mean_normalized2.iloc[:, :6] = mean_normalized2.iloc[:, :6].diff(periods=10).abs()
    grades["raw_diff_abs"] = mean_normalized2.transpose().iloc[1:6, :].sum()  # .diff(periods=10).abs()

    # Relating as if each axe has same weight.
    grades["data_sum"] = to_be_graded.transpose().iloc[1:6,
                         :].sum()  # Data in each axe is in range [0,1]
    # grades["grade"] = grades["grade"]  # Make data be in range [0,5]
    grades["data_sum_diff_abs"] = 1 - grades["data_sum"].diff(periods=10).abs()
    return grades


def calc_grades_1(mean_normalized_data: pd.DataFrame) -> pd.DataFrame:
    """
    Calc diff of a row with n row ahead.

    For small n: a high resolution diff will be calculated, noticing only aggressive changes in data.
    For large n: a low resolution diff will be calculated, allowing the slope to be gentle, and yet be noticed.

    This way, slow changes will be noticed
    :param mean_normalized_data:
    :return: pd.DataFrame
    """

    to_be_graded = mean_normalized_data.copy()

    grades: pd.DataFrame = pd.DataFrame(columns=["time", "raw_diff_abs","derivative"])
    grades["time"] = to_be_graded["elapsed"]

    to_be_graded.iloc[:, :6] = to_be_graded.iloc[:, :6].diff(periods=10).abs()
    grades["raw_diff_abs"] = 1 - to_be_graded.transpose().iloc[1:6,
                                 :].sum()  # Max value is 1, from there it gett smaller as data diff grows
    grades["derivative"] = grades["raw_diff_abs"].diff() / grades["time"].diff()
    return grades


if __name__ == "__main__":
    csv_name = sg.PopupGetFile('Enter the desired record for EDA')
    # reading csv file
    df = pd.read_csv(csv_name)

    df = fix_time_stamp(df)
    # fig_acc_xyz(df, given_title="IMU raw data: acc XYZ")
    # fig_gyro_xyz(df, given_title="IMU raw data: gyro XYZ")

    std_per_axe = calculate_std(df, sample_time=10)
    print(std_per_axe)
    std_removed = remove_std(df, std_per_axe)

    std_removed['elapsed'] = df['elapsed']
    fig_df1_and_df2(df, std_removed, sensor="acc", df1_trace_title="raw data", df2_trace_title="std_removed",
                    given_title="IMU data, raw vs std_removed")

    # fig_acc_xyz(std_removed, given_title="IMU data: acc XYZ (std_removed)")
    # fig_gyro_xyz(std_removed, given_title="IMU data: gyro XYZ (std_removed)")

    # window_size_sec = 1.0
    # mean = calc_mean_using_sliding_window(std_removed, window_size_sec)
    # fig_sensor = "acc"
    # fig_df1_and_df2(std_removed, mean, sensor=fig_sensor, df1_trace_title="std_removed", df2_trace_title="mean",
    #                 given_title="IMU {} XYZ data, std_removed and mean. sliding_window size {} [sec]".format(
    #                     fig_sensor, window_size_sec))
    # fig_sensor = "gyro"
    # fig_df1_and_df2(std_removed, mean, sensor=fig_sensor, df1_trace_title="std_removed", df2_trace_title="mean",
    #                 given_title="IMU {} XYZ data, std_removed and mean. sliding_window size {} [sec]".format(
    #                     fig_sensor, window_size_sec))

    window_size_sec = 0.2
    # mean = calc_mean_using_sliding_window(std_removed, window_size_sec)
    # fig_sensor = "acc"
    # fig_df1_and_df2(std_removed, mean, sensor=fig_sensor, df1_trace_title="std_removed", df2_trace_title="mean",
    #                 given_title="IMU {} XYZ data, std_removed and mean. sliding_window size {} [sec]".format(
    #                     fig_sensor, window_size_sec))
    # fig_sensor = "gyro"
    # fig_df1_and_df2(std_removed, mean, sensor=fig_sensor, df1_trace_title="std_removed", df2_trace_title="mean",
    #                 given_title="IMU {} XYZ data, std_removed and mean. sliding_window size {} [sec]".format(
    #                     fig_sensor, window_size_sec))

    # fig_acc_xyz(mean, given_title="IMU data (sliding window mean): acc XYZ")
    # fig_gyro_xyz(mean, given_title="IMU data (sliding window mean): gyro XYZ")

    std_removed_normalized = normalize_data(std_removed)
    mean_normalized = calc_mean_using_sliding_window(std_removed_normalized, window_size_sec)
    fig_sensor = "acc"
    fig_df1_and_df2(std_removed_normalized, mean_normalized,
                    sensor=fig_sensor,
                    df1_trace_title="std_removed_normalized",
                    df2_trace_title="mean_normalized",
                    given_title="IMU {} XYZ data, mean_normalized and std_removed_normalized. sliding_window size {} [sec]".format(
                        fig_sensor, window_size_sec))

    mean_normalized2 = mean_normalized.copy()
    mean_normalized2.iloc[:, :6] = mean_normalized2.iloc[:, :6].diff(periods=10).abs()
    fig_df1_and_df2(mean_normalized2, mean_normalized,
                    sensor=fig_sensor,
                    df1_trace_title="mean_normalized2",
                    df2_trace_title="mean_normalized",
                    given_title="IMU {} XYZ data, mean_normalized and std_removed_normalized.".format(
                        fig_sensor))

    grades = calc_grades_1(mean_normalized)
    # average_grade = grades["data_sum"].mean()
    avarage_grade = grades["raw_diff_abs"].mean()
    fig_grades(grades, "grades [average grade: {}]".format(avarage_grade), sensor_data=mean_normalized)
    # fig_acc_xyz(std_removed_normalized, given_title="IMU std_removed_normalized data: acc XYZ")
    # fig_gyro_xyz(std_removed_normalized, given_title="IMU std_removed_normalized data: gyro XYZ")
    # fig_acc_xyz(mean_normalized, given_title="IMU data (sliding window mean normalized): acc XYZ")
    # fig_gyro_xyz(mean_normalized, given_title="IMU data (sliding window mean normalized): gyro XYZ")
