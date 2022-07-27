


import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

import os
import numpy as np
from numbers import Number
from math import atan2, degrees, radians

def circumferences_intersection(p0: (Number, Number), r0: Number, p1: (Number, Number), r1: Number) -> list:
    """
    It calculates the intersection of two circumferences given their center and radius.
    Args:
        - `p0`: first circle center
        - `r0`: first circle radius
        - `p1`: second circle center
        - `r1`: second circle radius
    Returns:
        intersection points in case of intersecting circumferences. None in any other case.
    """

    (x0, y0) = p0
    (x1, y1) = p1

    d = np.sqrt((x1-x0)**2 + (y1-y0)**2)

    if d > r0 + r1:      # non intersecting
        return None
    if d <= abs(r0-r1):  # One circle within other
        return None

    a = (r0**2-r1**2+d**2)/(2*d)
    h = np.sqrt(r0**2-a**2)
    x2 = x0+a*(x1-x0)/d
    y2 = y0+a*(y1-y0)/d
    x3 = x2+h*(y1-y0)/d
    y3 = y2-h*(x1-x0)/d

    x4 = x2-h*(y1-y0)/d
    y4 = y2+h*(x1-x0)/d

    return [(round(x3, 5), round(y3, 5)),
            (round(x4, 5), round(y4, 5))]


st.title('Hello World')

x = st.slider('X: ', -10.0, 10.0, 5.)
y = st.slider('Y: ', 0., 10.0, 5.)

pm = circumferences_intersection((0, 0), 7, (x, y), 3)

data = pd.DataFrame([(0, 0), pm[0], (x, y)], columns=['X', 'Y'])
brush = alt.selection_single()  # selection of type "single"

chart = alt.Chart(data).mark_line().encode(
    x=alt.X('X', scale=alt.Scale(domain=[-10, 10])),
    y=alt.Y('Y', scale=alt.Scale(domain=[0, 10])),
).properties(title="Hello World").add_selection(
    brush
)
st.altair_chart(chart, use_container_width=False)


import altair as alt
from vega_datasets import data

source = data.seattle_weather()
brush = alt.selection(type='interval', encodings=['x'])

bars = alt.Chart().mark_bar().encode(
    x='month(date):O',
    y='mean(precipitation):Q',
    opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.7)),
).add_selection(
    brush
)

line = alt.Chart().mark_rule(color='firebrick').encode(
    y='mean(precipitation):Q',
    size=alt.SizeValue(3)
).transform_filter(
    brush
)

c = alt.layer(bars, line, data=source)

st.altair_chart(c, use_container_width=False)


"""
import streamlit as st
import plotly.express as px
import pandas as pd
from streamlit_plotly_events import plotly_events

x = [1, 2, 3, 4, 5]
y = [6, 7, 2, 4, 5]

df=[]
df= pd.DataFrame(df)
df['year']= x
df['lifeExp']= y

fig = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada')

selected_points = plotly_events(fig)
a=selected_points[0]

a= pd.DataFrame.from_dict(a,orient='index')
a


from dragon.ui.web import app


if __name__ == '__main__':
    app.run(debug=True)
"""