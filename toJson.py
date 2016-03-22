import source
import json
import numpy


# Serializer to Serialize numpy objects
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)


dataInp = source.newline
# Store Corners in listCorners by removing the duplicates using set
uniqueCorners = set()
for [x1, y1, x2, y2] in dataInp:
    uniqueCorners.add((x1, y1))
    uniqueCorners.add((x2, y2))
listCorners = list(uniqueCorners)
# make a sub-dict of corners
corners = {}
for c in range(len(listCorners)):
    coors = {"x": listCorners[c][1], "y": listCorners[c][0]}
    corners[c] = coors
# Store Walls in list having corner info in sub-dictionaries
walls = []
for [x1, y1, x2, y2] in dataInp:
    corner1 = listCorners.index((x1, y1))
    corner2 = listCorners.index((x2, y2))
    wall = {"corner1": corner1, "corner2": corner2}
    walls.append(wall)
# Get data in required JSON file format
data = {"floorplan": {"corners": corners, "walls": walls}}
print(data)
# JSON file output
with open('floorplan.json', 'w') as outfile:
    json.dump(data, outfile, cls=MyEncoder)
