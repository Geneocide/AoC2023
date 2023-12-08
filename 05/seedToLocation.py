from pathlib import Path
filepath = Path(__file__).parent / "input.txt"

sources = {}
maps = {} #key is src, value is mappings data
order = []

def followMaps(maps, s):
    for map in maps:
        des, src, range = map
        if s >= src and s < src + range:
            return s - src + des #special map rule found, return value
    return s 

with open(filepath, "r") as file:
    src = None
    data = []
    for line in file:
        line = line.strip()
        if len(line) == 0: continue
        if ':' in line: # then header
            if '-' in line: # then not seeds
                if src != None:
                    maps[src] = data #add completed mapping data to mappings dict
                    order.append(src)
                    if src != "seed":
                        sources[src] = [] #add empty space for during traversal of maps
                    data = []
                src,des = line.split("-to-")
            else:
                sources["seed"] = list(map(int, line.split(':')[1].split()))
        else: #normal mapping data
            data.append(list(map(int, line.split())))
    #add final section's data
    des = des.split()[0]
    order.append(src)
    order.append(des)
    sources[src] = []
    sources[des] = []
    maps[src] = data

for source in sources:
    if source == "location": break #done
    sourceData = sources[source]
    for s in sourceData:
        sources[order[order.index(source) + 1]].append(followMaps(maps[source], s))

print("Lowest location: " + str(min(sources["location"]))) #answer 484023871