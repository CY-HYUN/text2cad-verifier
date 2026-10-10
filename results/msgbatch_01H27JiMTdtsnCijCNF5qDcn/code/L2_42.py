import cadquery as cq

# L profile extruded 60 wide, centered on z=0
pts = [(0,0),(100,0),(100,10),(10,10),(10,100),(0,100)]
L = cq.Workplane("XY").polyline(pts).close().extrude(30, both=True)

# holes through plates
h1 = cq.Workplane("XZ").center(50, 0).circle(10).extrude(-20)  # along +Y through horizontal plate
h2 = cq.Workplane("YZ").center(50, 0).circle(10).extrude(20)   # along +X through vertical plate
L = L.cut(h1).cut(h2)

# triangular rib, 10 thick, centered on mid plane
rib = (cq.Workplane("XY")
       .polyline([(10,10),(60,10),(10,60)]).close()
       .extrude(5, both=True))

result = L.union(rib)
