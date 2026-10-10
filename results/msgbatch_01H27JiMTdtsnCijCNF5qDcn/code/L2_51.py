import cadquery as cq

# T-shaped profile: top bar 60x20, stem 20 wide x 40 long
pts = [
    (-30, 0), (30, 0), (30, 20), (-30, 20), (-30, 0)
]
bar = cq.Workplane("XY").rect(60, 20, centered=(True, False)).extrude(20)
stem = (cq.Workplane("XY").workplane()
        .center(0, -20).rect(20, 40).extrude(20))
block = bar.union(stem).clean()

# Fillet all edges with 8 mm radius
block = block.edges().fillet(8)

# Holes, 5 mm dia, at centers of the three flat ends
# Along X through the bar's two ends
hole_x = (cq.Workplane("YZ").workplane(offset=-40)
          .center(10, 10).circle(2.5).extrude(80))
# Along Y through the stem's bottom end
hole_y = (cq.Workplane("XZ").workplane(offset=-30)
          .center(0, 10).circle(2.5).extrude(70))
# XZ normal is -Y: offset=-30 -> y=30, extrude goes toward -Y by 70 -> y=-40

result = block.cut(hole_x).cut(hole_y)
