
"""
Visualize pydelta results.
"""



# ========================
# Imports
# ========================

import pandas as pd 
from os.path import join
import pygal


# ========================
# Parameters
# ========================


resultsfile = "delta-results.tsv"
indicator = "Adjusted Rand Index"




# ========================
# Functions
# ========================


def load_data(resultsfile): 
    with open(resultsfile, "r", encoding="utf8") as infile: 
        data = pd.read_csv(infile, sep="\t")
        #print(data.head())
        plots = list(set(data.loc[:,"coll"]))
        #print(plots)
        return data, plots


def group_data(data, plot): 
    grouped = data.groupby(["coll"])
    grouped = grouped.get_group(plot)
    grouped = grouped.groupby(["measure"])
    return grouped


def prepare_data(grouped, indicator): 
    allscores = {}
    for measure, scores in grouped: 
        #print(measure)
        mfws = list(grouped.get_group(measure).loc[:,"mfw"])
        scores = list(grouped.get_group(measure).loc[:,indicator])
        #print(mfws)
        #print(scores)
        allscores[measure] = scores
        #print(prepared)
    return mfws, allscores


def visualize(mfws, allscores, plot, indicator): 
    plotname = "results_"+str(plot)+".svg"
    chart = pygal.Line(range=(0.3,1.0), x_label_rotation=-60)
    chart.legend_at_bottom = True
    chart.legend_at_bottom_columns = 3
    chart.x_labels = mfws
    chart.title = str(plot)+" ("+str(indicator)+")"
    for key,vizdata in allscores.items(): 
        #print(key, vizdata)
        chart.add(key, vizdata, stroke_style={'width': 3})
    chart.render_to_file(plotname)
        



# ========================
# Main
# ========================


def main(resultsfile, indicator): 
    data, plots = load_data(resultsfile)
    for plot in plots: 
        print(plot)
        grouped = group_data(data, plot)
        mfws, allscores = prepare_data(grouped, indicator)
        visualize(mfws, allscores, plot, indicator)
    
    


main(resultsfile, indicator)
