import pandas as pd
import altair as alt


def dummy_plot(points=None):
    if points is None:
        points = [(0, 0), (3, 0), (3, 4)]
    data = pd.DataFrame(points, columns=['X', 'Y'])

    print(data)
    chart = alt.Chart(data).mark_line().encode(
        x=alt.X('X', scale=alt.Scale(domain=[-10, 10])),
        y=alt.Y('Y', scale=alt.Scale(domain=[0, 10])),
    ).properties(title="Hello World")

    chart_json = chart.to_json()
    return chart_json

