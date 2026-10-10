import cadquery as cq

# Create a new part with the base disk
# Start with a circle of diameter 100mm on the XY plane
base = cq.Workplane("XY").circle(50).extrude(5)

# Now create the hole - a concentric circle of diameter 50mm on the top surface
# and extrude it downward to cut through the entire thickness
washer = base.faces(">Z").workplane().circle(25).cutThruAll()

result = washer
