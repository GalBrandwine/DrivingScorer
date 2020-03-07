import numpy as np
import pandas as pd

csv_name = "06_03_2020_13_53_08_moved_slowly_that_fast_in_z_axe.csv"
csv_name = "06_03_2020_17_30_06_holding_still.csv"
# reading csv file
df = pd.read_csv(csv_name)

df['timestamp'] = pd.to_datetime(df['timestamp'],
                                 format='%H:%M:%S.%f')  # Change timestamp format to something pd understand
# print(data.dtypes)


df['timestamp'] = df['timestamp'] - df['timestamp'].iloc[0]  # Change from timestamp to time-passed-from-beginning
df['elapsed'] = df['timestamp'] / np.timedelta64(1, 's')  # Change from milisec to seconds

# fig = px.scatter(df, x='elapsed', y='ax'
#                  )
from plotly.subplots import make_subplots
import plotly.graph_objects as go

fig = make_subplots(rows=3, cols=1,
                    shared_xaxes=True,

                    subplot_titles=("aX", "aY", "aZ"))

fig.add_trace(
    go.Scatter(x=df['elapsed'], y=df['ax'], name="ax"),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(x=df['elapsed'], y=df['ay'],name="ay"),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(x=df['elapsed'], y=df['az'], name="az"),
    row=3, col=1
)

# Update xaxis properties
fig.update_xaxes(title_text="Elapsed time [sec]",row=3, col=1)

#
# # Update yaxis properties
# fig.update_yaxes(title_text="yaxis 1 title", row=1, col=1)
# fig.update_yaxes(title_text="yaxis 2 title", range=[40, 80], row=1, col=2)
# fig.update_yaxes(title_text="yaxis 3 title", showgrid=False, row=2, col=1)
# fig.update_yaxes(title_text="yaxis 4 title", row=2, col=2)

fig.update_layout(title_text="IMU data")
fig.show()

# fig.data[0].update(mode='markers+lines')
# fig.update_traces(marker=dict(size=12,
#                               line=dict(width=2,
#                                         color='DarkSlateGrey')),
#                   selector=dict(mode='markers+lines'))
#
# fig2 = px.scatter(df, x="elapsed", y="ay",color='ay')
# fig2.update_traces(marker=dict(size=12,
#                               line=dict(width=2,
#                                         color='Peach')),
#                   selector=dict(mode='markers+lines'))
#
# fig3 = px.scatter(df, x="elapsed", y="az",color='az')
# fig3.data[0].update(mode='markers+lines')
#
# fig.add_trace(fig2.data[0])
# fig.add_trace(fig3.data[0])

# fig.show()
