from pathlib import Path
filepath = Path(__file__).parent / "input.txt"

sources = {}
maps = {} #key is src, value is mappings data
order = []
possibilities = set()

def followMaps(maps, s):
    for map in maps:
        des, src, range = map
        if s >= src and s < src + range:
            return s - src + des #special map rule found, return value
    return s

def backwardsMap(maps, answer):
    for map in maps:
        des, src, range = map
        if answer >= src and answer < src + range:
            return answer + src - des
    return answer


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
                src, des = line.split("-to-")
            else:
                sources["seed"] = list(map(int, line.split(':')[1].split()))
        else: #normal mapping data
            rowMap = list(map(int, line.split()))
            data.append(rowMap)
            possibilities.add(rowMap[1])
    #add final section's data
    des = des.split()[0]
    order.append(src)
    order.append(des)
    sources[src] = []
    sources[des] = []
    maps[src] = data

#generate possible minimums that should be checked
toCheck = {}
for level in reversed(order):
    if level == "location": continue
    toCheck[level] = []
    map = maps[level]
    if level != "humidity":
        for check in toCheck[order[order.index(level) + 1]]:
            toCheck[level].append(backwardsMap(map, check))
    for rule in map:
        toCheck[level].append(rule[1])
possibilities = toCheck["seed"]

#generate seeds from seed range and possibilities
tempSeed = []
for i in range(0, len(sources["seed"]), 2):
    start = sources["seed"][i]
    end = start + sources["seed"][i + 1]
    tempSeed.append(start)
    for possibility in possibilities: #definitely should be using the possibilities, that was the whole point
        if possibility in range(start, end):
            tempSeed.append(possibility)
#    for j in range(start, end):
#        if j == start or j in possibilities:
#            tempSeed.append(j)
sources["seed"] = tempSeed

for source in sources:
    if source == "location": break #done
    sourceData = sources[source]
    for s in sourceData:
        sources[order[order.index(source) + 1]].append(followMaps(maps[source], s))

print("Lowest location: " + str(min(sources["location"]))) #answer 46294175