
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


# ======== full analysis parameters =================

collections = {"ELTeC-fra" : join("..", "corpora", "fra", ""),
               "ELTeC-eng" : join("..", "corpora", "eng", ""),
               "ELTeC-slv" : join("..", "corpora", "slv", ""),
               "ELTeC-deu" : join("..", "corpora", "deu", ""),
               "ELTeC-por" : join("..", "corpora", "por", ""),
               "ELTeC-hun" : join("..", "corpora", "hun", ""),
               "ELTeC-rom" : join("..", "corpora", "rom", "")}

mfws = [10,20,30,40,50,60,70,80,90,100,125,150,175,200,225,250,275,300,325,350,375,400,425,450,475,500,550,600,650,700,750,800,850,900,950,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2200,2400,2600,2800,3000,3200,3400,3600,3800,4000,4200,4400,4600,4800,5000,5500,6000,6500,7000,7500,8000,8500,9000,9500,10000]

#mfws = [10,20,30,40,50,100,150,200,250,300,350,400,450,500,600,700,800,900,1000,1200,1400,1600,1800,2000,2500,3000,3500,4000,4500,5000,6000,7000,8000,9000,10000]

measures = {"cosine-d" : delta.functions.cosine_delta,
            "burrows-d" : delta.functions.burrows,
            "eders-d" : delta.functions.eder}

dendrogram = "save" # "show"|"save"|"none"



# ============ testing parameters ======================

#collections = {"ELTeC-fra" : join("..", "corpora", "fra", ""),
#               "ELTeC-rom" : join("..", "corpora", "rom", "")}
#mfws = [100,500,1000]
#measures = {"cosine-d" : delta.functions.cosine_delta,
#            "burrows-d" : delta.functions.burrows}
#dendrogram = "save" # "show"|"save"|"none"



# ========================
# Functions
# ========================


def load_data(collection): 
    print("load_data")
    data = delta.Corpus(collection, feature_generator=delta.FeatureGenerator(lower_case=True, max_tokens=40000))
    return data


def run_delta(data, mfw, measure, dendrogram, runID): 
    data = data.get_mfw_table(mfw)
    distances = measure(data)
    clusters = delta.Clustering(distances)
    if dendrogram == "show": 
        plt.figure(figsize=(8,12))
        delta.Dendrogram(clusters).show()
    if dendrogram == "save": 
        plt.figure(figsize=(8,12))
        delta.Dendrogram(clusters)
        plt.savefig(join("..", "dendrograms", runID+".png"))
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
    with open(join("..", "evaluation-overview.tsv"), "w", encoding="utf8") as outfile: 
        allresults.to_csv(outfile, sep="\t")
    


# ========================
# Main
# ========================


def main(collections, mfws, measures, dendrogram): 
    allresults = {}
    for key in collections: 
        coll_name = key
        print(coll_name)
        data = load_data(collections[key])
        for mfw in mfws: 
            for label,measure in measures.items(): 
                runID = coll_name +"_"+ str(label) +"_"+ '{:04}'.format(mfw) 
                params = pd.Series([coll_name, str(label), '{:04}'.format(mfw)], ["coll", "measure", "mfw"])
                distances, clusters = run_delta(data, mfw, measure, dendrogram, runID)
                dist_eval = evaluate_distances(distances)
                clust_eval = evaluate_clusters(clusters)
                results = params.append(clust_eval)
                allresults[runID] = results
    save_results(allresults)

main(collections, mfws, measures, dendrogram)
