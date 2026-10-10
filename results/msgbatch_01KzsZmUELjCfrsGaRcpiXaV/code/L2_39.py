import cadquery as cq
import math

# Create the base wedge shape using a solid approach
# Bottom surface: 60x40mm, rear height: 40mm, front height: 10mm

# Create base box
base = cq.Workplane("XY").box(60, 40, 10, centered=False)

# Create the sloped portion
# We'll create a second box and position it to form the slope
slope = cq.Workplane("XY").box(60, 40, 30, centered=False)
slope = slope.translate((0, 0, 10))

# Cut the slope to create the wedge effect
# Create a cutting plane that removes material from front to back
cutting_wedge = cq.Workplane("XY").sketch().polygon([
    (0, 0), (60, 0), (60, 40), (0, 40)
]).finalize().extrude(30)
cutting_wedge = cutting_wedge.translate((0, 0, 10))

# Combine base with sloped section
wedge = base.union(slope)

# Now cut to create the wedge (slope from z=10 at y=0 to z=40 at y=40)
# Create a box that we'll use to cut
upper_cut = cq.Workplane("XY").box(60, 40, 30, centered=False)
upper_cut = upper_cut.translate((0, 0, 10))

# Create cutting geometry - a rectangular solid that slopes
# Cut away the lower front portion
front_cut = cq.Workplane("XY").box(60, 40, 30, centered=False).translate((0, 0, 10))
wedge = base.union(
    cq.Workplane("XY").polyline([(0, 0), (60, 0), (60, 40), (0, 40)]).close().workplane(offset=10).polyline([(0, 0), (60, 0), (60, 40), (0, 40)]).close().loft(ruled=True)
)

# Simpler solid approach: create wedge directly
vertices = [
    (0, 0, 0), (60, 0, 0), (60, 40, 0), (0, 40, 0),  # bottom face
    (0, 0, 10), (60, 0, 10), (60, 40, 40), (0, 40, 40)  # top face
]

# Build using a sweep/loft approach
bottom_face = cq.Workplane("XY").sketch().polygon([(0, 0), (60, 0), (60, 40), (0, 40)]).finalize()
top_face = cq.Workplane("XY", origin=(0, 0, 10)).sketch().polygon([(0, 0), (60, 0), (60, 40), (0, 40)]).finalize()

# Create wedge by combining two boxes and cutting
box1 = cq.Workplane("XY").box(60, 40, 10, centered=False)
box2 = cq.Workplane("XY").box(60, 40, 30, centered=False).translate((0, 0, 10))

# Cut a triangular wedge from box2
cut_solid = cq.Workplane("XY").box(60, 40, 30, centered=False).translate((0, 0, 10))
# Remove front portion: create a sloped cut
wedge = box1.union(box2)

# Create the slope by cutting - remove a triangular prism from the front
cutter = cq.Workplane("XZ").sketch().polygon([(0, 10), (40, 40), (0, 40)]).finalize().extrude(60)
wedge = wedge.cut(cutter)

# Add the rectangular slot on the beveled surface (30mm x 15mm x 10mm deep)
slot_box = cq.Workplane("XY").box(30, 15, 10, centered=True)
slot_center = (30, 20, 25)
slot_box = slot_box.translate(slot_center)

wedge = wedge.cut(slot_box)

# Add the through-hole (8mm diameter) at the center of the slot
hole = cq.Workplane("XY").circle(4).extrude(50, both=True)
hole = hole.translate((30, 20, 0))

wedge = wedge.cut(hole)

result = wedge
