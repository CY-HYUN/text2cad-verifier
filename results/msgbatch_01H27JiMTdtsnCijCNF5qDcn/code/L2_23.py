import cadquery as cq

# Plane 1: z=0, Plane 2: z=20, Plane 3: z=50
base = cq.Workplane("XY").rect(50, 50).extrude(20)

transition = (
    cq.Workplane("XY").workplane(offset=20)
    .rect(50, 50)
    .workplane(offset=30)
    .circle(15)
    .loft(combine=True)
)

top = cq.Workplane("XY").workplane(offset=50).circle(15).extrude(20)

solid = base.union(transition).union(top)

# Shell: remove top and bottom faces, 2 mm wall thickness (inward)
result = solid.faces(">Z or <Z").shell(-2)
