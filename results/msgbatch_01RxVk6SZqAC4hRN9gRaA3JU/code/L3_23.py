import cadquery as cq

# Base block: 200 x 100 x 80, centered in XY, z from 0 to 80
L, W, H = 200.0, 100.0, 80.0
block = cq.Workplane("XY").rect(L, W).extrude(H)

# Countersunk bolt holes at the four top corners
corner_pts = [(-90, -40), (90, -40), (-90, 40), (90, 40)]
block = (
    block.faces(">Z").workplane(centerOption="CenterOfBoundBox")
    .pushPoints(corner_pts)
    .cskHole(9.0, 18.0, 90.0)
)

# Internal longitudinal main oil passages (along X) at y = +/-20, z = 40
main_passages = (
    cq.Workplane("YZ", origin=(-L / 2, 0, 0))
    .pushPoints([(-20, 40), (20, 40)])
    .circle(8.0)
    .extrude(180.0)
)
block = block.cut(main_passages)

# Three front oil inlets, dia 20, at center height, drilled from y = -50 toward +Y
inlets = (
    cq.Workplane("XZ", origin=(0, -W / 2, 0))
    .pushPoints([(-50, 40), (0, 40), (50, 40)])
    .circle(10.0)
    .extrude(-75.0)  # XZ normal is -Y, so negative extrude goes +Y
)
block = block.cut(inlets)

# Two rows of five dia-10 top holes, cut down to the main passages (z = 40)
top_pts = [(x, y) for y in (-20, 20) for x in (-70, -35, 0, 35, 70)]
top_holes = (
    cq.Workplane("XY", origin=(0, 0, 40))
    .pushPoints(top_pts)
    .circle(5.0)
    .extrude(40.0)
)
block = block.cut(top_holes)

# Lightening grooves: two oval pockets on the bottom face
bottom_slots = (
    cq.Workplane("XY")
    .pushPoints([(-50, 0), (50, 0)])
    .slot2D(60.0, 20.0)
    .extrude(20.0)
)
block = block.cut(bottom_slots)

# Lightening grooves: two oval pockets on the back side face (y = +50)
side_slots = (
    cq.Workplane("XZ", origin=(0, W / 2, 0))
    .pushPoints([(-50, 40), (50, 40)])
    .slot2D(60.0, 20.0)
    .extrude(15.0)  # goes -Y from y=50 to y=35
)
block = block.cut(side_slots)

result = block
