from altair import Chart, X, Y, Axis, Data, DataFormat
import pandas as pd
import numpy as np
from flask import render_template, url_for, flash, redirect, request, make_response, jsonify, abort
from dragon.ui.web import app
from dragon.ui.web.utils import utils, altair_plot, arm
import json

# Loading raw data and clean it



#loading data
total_confirmed, total_death, total_recovered, df_pop = utils.load_data()

(grouped_total_confirmed, grouped_total_recovered,
 grouped_total_death, timeseries_final, country_names) = utils.preprocessed_data(total_confirmed, total_death, total_recovered)

final_df = utils.merge_data(grouped_total_confirmed,
                            grouped_total_recovered, grouped_total_death, df_pop)

#for chart_js map



@app.route("/")
@app.route("/altair")
def plot_altair_global():
    # total confirmed cases globally
    total_all_confirmed = total_confirmed[total_confirmed.columns[-1]].sum()
    total_all_recovered = total_recovered[total_recovered.columns[-1]].sum()
    total_all_deaths = total_death[total_death.columns[-1]].sum()
    #ploting
    plot_global_cases_per_country = altair_plot.altair_global_cases_per_country(final_df)
    plot_global_time_series = altair_plot.altair_global_time_series(
        timeseries_final)
    plot_geo_analysis = altair_plot.altair_geo_analysis(final_df)
    context = {"total_all_confirmed": total_all_confirmed,
               "total_all_recovered": total_all_recovered, "total_all_deaths": total_all_deaths,
               'plot_global_cases_per_country': plot_global_cases_per_country,
               'plot_global_time_series': plot_global_time_series, 'plot_geo_analysis': plot_geo_analysis}
    return render_template('altair.html', context=context)

@app.route("/robot")
def plot_robot_global():
    context = {"dragon_arm": arm.dummy_plot()}
    return render_template('dragon-tank.html', context=context)

@app.route('/background_process_test')
def background_process_test():
    context = {"dragon_arm": arm.dummy_plot([(0, 0), (3, 3), (1, 4)])}
    return render_template('dragon-tank.html', context=context)
