"""

import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

st.title('Hello World')

data = pd.DataFrame([(0, 0), (3, 0), (3, 4)], columns=['X', 'Y'])

chart = alt.Chart(data).mark_line().encode(
    x=alt.X('X', scale=alt.Scale(domain=[-10, 10])),
    y=alt.Y('Y', scale=alt.Scale(domain=[0, 10])),
).properties(title="Hello World")
st.altair_chart(chart, use_container_width=False)


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

"""
from dragon.ui.web import app


if __name__ == '__main__':
    app.run(debug=True)