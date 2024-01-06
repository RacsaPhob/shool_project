from shapely.geometry import  Polygon
from shapely.affinity import  rotate

tri = Polygon([(0,0),(2,0),(1,1)])
tri = rotate(tri,180,origin=(1,0),use_radians=False)
print(list(tri.exterior.coords))
