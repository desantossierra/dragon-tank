import streamlit as st
from dragon.ui.apps.app import App
import pandas as pd
import numpy as np
import altair as alt
from dragon.utils.math import circumferences_intersection


class Robot(App):

    def run(self):
        col1, col2, col3 = st.columns([0.2, 0.6, 0.2])
        with col1:
            st.image('resources/brazo-robotico.png', width=90)
        with col3:
            x = st.slider('X', -15., 15., 7.)
            y = st.slider('Y', 0., 15., 7.)
        with col2:               # To display brand log

            points = circumferences_intersection((0, 0), 6.6, (x, y), 13.5)

            df = pd.DataFrame(
                [(0, 0, 0), (1, *points[0]), (2, x, y)],
                columns=['i', 'x', 'y'])

            print(df, [(0, 0), points[0], (x, y)])
            c = alt.Chart(df).mark_line().encode(
                x = alt.X('x', scale=alt.Scale(domain=[-15, 15])),
                y = alt.Y('y', scale=alt.Scale(domain=[0, 15])
                          ))

            st.altair_chart(c, use_container_width=True)
