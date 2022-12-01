import csv

birds_ratios={}

birds_habitats={}


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
    "Lakes and Ponds":0.5,
    "Marshes":0,
    "Forests":1,
    "Rivers and Streams":0.5,
    "Open Woodlands": 0,
    "Grasslands":0,
    "Shorelines":0.5,
    "Oceans":0
}

def normalize_score(a): #Function to return score to compare against habitats
    if a>=1.5:
        return 1
    if a<1.5 and a>=0.5:
        return 0.5
    return 0
    
total=0
for bird in birds_habitats:
    total+=abs(habitats[birds_habitats[bird]]-normalize_score(birds_ratios[bird]))

print((1-(total/len(birds_habitats)))*100)
