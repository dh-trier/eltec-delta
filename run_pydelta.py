
"""
Run pyzeta on ELTeC collections. 
Requires pandas to be v. 0.25.3 (!)
"""



# ========================
# Imports
# ========================

import delta
import pandas as pd 
from os.path import join
import matplotlib.pyplot as plt

print(pd.__version__)

# ========================
# Parameters
# ========================


collections = {"ELTeC-fra" : join("corpora", "fra", ""),
               "ELTeC-eng" : join("corpora", "eng", ""),
               "ELTeC-slv" : join("corpora", "slv", ""),
               "ELTeC-deu" : join("corpora", "deu", ""),
               "ELTeC-rom" : join("corpora", "rom", ""),
               "ELTeC-por" : join("corpora", "por", ""),
               "ELTeC-hun" : join("corpora", "hun", ""),
               "ELTeC-slv" : join("corpora", "slv", "")}


mfws = [10,20,30,40,50,100,150,200,250,300,350,400,450,500,600,700,800,900,1000,1200,1400,1600,1800,2000,2500,3000,3500,4000,4500,5000]

measures = {"cosine-d" : delta.functions.cosine_delta,
            "burrows-d" : delta.functions.burrows,
            "eders-d" : delta.functions.eder}


# ========================
# Functions
# ========================


def load_data(collection): 
    print("load_data")
    data = delta.Corpus(collection, feature_generator=delta.FeatureGenerator(lower_case=True, max_tokens=40000))
    return data


def run_delta(data, mfw, measure): 
    data = data.get_mfw_table(mfw)
    distances = measure(data)
    clusters = delta.Clustering(distances)
    #plt.figure(figsize=(8,12))
    #delta.Dendrogram(clusters).show()
    return distances, clusters


def evaluate_distances(distances): 
    dist_eval = distances.evaluate()
    #print(dist_eval)
    return dist_eval


def evaluate_clusters(clusters): 
    clusters = clusters.fclustering()
    #print(clusters.describe())
    clust_eval = clusters.evaluate()   
    #print(clust_eval)    
    return clust_eval


def save_results(allresults): 
    allresults = pd.DataFrame(allresults).T
    print(allresults.head())
    with open("delta-results.tsv", "w", encoding="utf8") as outfile: 
        allresults.to_csv(outfile, sep="\t")
    


# ========================
# Main
# ========================


def main(collections, mfws, measures): 
    allresults = {}
    for key in collections: 
        coll_name = key
        print(coll_name)
        data = load_data(collections[key])
        for mfw in mfws: 
            for label,measure in measures.items(): 
                params = pd.Series([coll_name, str(label), '{:04}'.format(mfw)], ["coll", "measure", "mfw"])
                distances, clusters = run_delta(data, mfw, measure)
                dist_eval = evaluate_distances(distances)
                clust_eval = evaluate_clusters(clusters)
                results = params.append(clust_eval)
                runID = coll_name +"_"+ str(label) +"_"+ '{:04}'.format(mfw) 
                allresults[runID] = results
    save_results(allresults)

main(collections, mfws, measures)
