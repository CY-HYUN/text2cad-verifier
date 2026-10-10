import cadquery as cq

# L-shaped profile extruded 60 wide, centered on z=0
pts = [(0,0),(100,0),(100,10),(10,10),(10,100),(0,100)]
L = cq.Workplane("XY").polyline(pts).close().extrude(30, both=True)

# Triangular rib on the mid-plane, 10 thick
rib = (cq.Workplane("XY").polyline([(10,10),(60,10),(10,60)]).close()
       .extrude(5, both=True))

body = L.union(rib)

# Holes dia 20 at centers of each plate
h1 = cq.Workplane("XZ").center(55,0).circle(10).extrude(-10)
h2 = cq.Workplane("YZ").center(55,0).circle(10).extrude(10)

result = body.cut(h1).cut(h2)
