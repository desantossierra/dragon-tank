import streamlit as st
from dragon.ui.old_apps.app import App
import pandas as pd
import numpy as np
import altair as alt
from dragon.utils.math import circumferences_intersection_safe
from dragon.ui.style.palette import DragonTail


class Robot(App):

    def run(self):
        col1, col2, col3 = st.columns([0.2, 0.4, 0.4])
        with col1:
            st.image('resources/brazo-robotico.png', width=300)
        with col3:
            x = st.slider('X', -15., 15., 7.)
            y = st.slider('Y', 0., 15., 7.)
        with col2:               # To display brand log

            self.plot_dragon_arm(x, y)

    def plot_dragon_arm(self, x, y):
        points = circumferences_intersection_safe((0, 0), 6.6, (x, y), 13.5)
        base = None
        max_radius = 20
        step_radius = 5
        for radius in range(step_radius, max_radius + 1, step_radius):
            cx = np.arange(-radius, radius, 0.01)
            cy = np.sqrt(radius ** 2 - cx ** 2)
            cir = pd.DataFrame.from_dict({'x': cx, 'y': cy})

            cir = alt.Chart(cir).mark_line().encode(
                x=alt.X('x', scale=alt.Scale(domain=[-max_radius, max_radius])),
                y=alt.Y('y', scale=alt.Scale(domain=[0, max_radius]), axis=None),
                color=alt.value(DragonTail.radius_grid)
            )

            base = cir if base is None else base + cir

        touched_point = False
        if points is not None and len(points) > 0:
            df = pd.DataFrame(
                [('FIRST', 0, 0), ('FIRST', *points[0]), ('SECOND', *points[0]), ('SECOND', x, y)],
                columns=['part', 'x', 'y'])
            arm = alt.Chart(df).encode(
                x=alt.X('x', scale=alt.Scale(domain=[-15, 15])),
                y=alt.Y('y', scale=alt.Scale(domain=[0, 15]), axis=None),
                color=alt.Color('part', legend=None),
                strokeWidth=alt.value(15)
            )
            base = base + arm.mark_line() + arm.mark_circle(size=250)
            touched_point = True


        obj = pd.DataFrame([(x, y)], columns=['x','y'])
        selection = alt.Chart(obj).mark_square(size=200).encode(
            x=alt.X('x', scale=alt.Scale(domain=[-15, 15])),
            y=alt.Y('y', scale=alt.Scale(domain=[0, 15]), axis=None),
            color=alt.value(DragonTail.touched_point if touched_point else DragonTail.untouched_point)
        )
        base = base + selection
        base = base.configure_axis(
            grid=False,
        ).configure_view(
            strokeWidth=0,
            strokeOpacity=0
        )
        st.altair_chart(base, use_container_width=True)

