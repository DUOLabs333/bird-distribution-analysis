import csv

birds_ratios={}

birds_habitats={}

#[[0.89, 1.03], 63.90041493775933]
#[[1,1],76] {'Scrub': 0, 'Towns': 0, 'Lakes and Ponds': 0, 'Marshes': 0, 'Forests': 1, 'Rivers and Streams': 0, 'Open Woodlands': 0, 'Grasslands': 0, 'Shorelines': 0, 'Oceans': 0}

with open("analysis_results.csv") as f:
    reader=csv.reader(f)
    next(reader)
    for row in reader:
        birds_ratios[row[0]]=float(row[1])

with open("preferred_habitats.csv") as f:
    reader=csv.reader(f)
    next(reader)
    for row in reader:
        birds_habitats[row[0]]=row[1]

habitats={
    "Scrub":0,
    "Towns":0,
    "Lakes and Ponds":0,
    "Marshes":0,
    "Forests":1,
    "Rivers and Streams":0,
    "Open Woodlands": 0,
    "Grasslands":0,
    "Shorelines":0,
    "Oceans":0
}

def normalize_score(a): #Function to return score to compare against habitats
    if a>=1:
        return 1
    if a<1 and a>=1:
        return 2
    return 0
    
total=0
for bird in birds_habitats:
    total+=int(habitats[birds_habitats[bird]]==normalize_score(birds_ratios[bird]))

print(total/len(birds_habitats)*100)
