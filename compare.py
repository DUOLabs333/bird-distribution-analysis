import csv

locations=[]

birds_habitats={}

#[[0.89, 1.03], 63.90041493775933]
#[[1,1],76] {'Scrub': 0, 'Towns': 0, 'Lakes and Ponds': 0, 'Marshes': 0, 'Forests': 1, 'Rivers and Streams': 0, 'Open Woodlands': 0, 'Grasslands': 0, 'Shorelines': 0, 'Oceans': 0}

with open("analysis_results.csv") as f:
    reader=csv.reader(f)
    next(reader)
    for row in reader:
        locations.append(row)

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
    
import itertools
maximum=[[],0]
for k in itertools.product([0,1,2],repeat=len(habitats)):
    correct=0
    total=0
    habitats=dict(zip(habitats.keys(),k))
    for location in locations:
        forest_birds=0
        open_birds=0
        for bird in eval(location[1]):
            if bird not in birds_habitats:
                continue
            total+=1
            habitat=habitats[birds_habitats[bird]]
            if habitat==0:
                open_birds+=1
            elif habitat==1:
                forest_birds+=1
            else:
                open_birds+=1
                forest_birds+=1
                
            if int(location[2])==int(forest_birds>open_birds):
                correct+=1
    if (correct/total>maximum[1]):
        maximum=[k,correct/total]
        print(maximum)

print((correct/total)*100)
