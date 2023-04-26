import argparse
from pathlib import Path
import shapefile

parser = argparse.ArgumentParser(description = "Simple Python Script to remove duplicates from Terrain Builder Object Files")
parser.add_argument("roads", type=str, help="Path of the Objects File")
parser.add_argument("ID", type=int, help="Road Type")
parser.add_argument("-o", "--output", type=str, default="output", help="Name of the output file")
args = parser.parse_args()

road_path = Path(args.roads)
assert road_path.exists(), f"Object Files {args.roads} do not exist"

f = open(road_path, "r")
points = eval(f.read())
f.close()

w = shapefile.Writer(args.output, shapeType=3)
w.field('ID', 'N')
w.field('ORDER', 'N')

lines = []
out = []
temp = []
order = 0

lines.append(points[0][4])
for i in points:
    if i[4] not in lines:
        w.line([temp])
        w.record(args.ID,0)
        order += 1
        temp = []
        lines.append(i[4])
    temp.append([float(i[1][0])+200000,float(i[1][1])])

w.line([temp])
w.record(args.ID,order)
w.close()
