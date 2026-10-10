import cadquery as cq

# Create the first beam (100mm long, 20mm wide)
beam1 = cq.Workplane("XY").rect(100.0, 20.0).extrude(20.0)

# Create the second beam (20mm long, 100mm wide) on the same plane
beam2 = cq.Workplane("XY").rect(20.0, 100.0).extrude(20.0)

# Fuse the two beams to create the cross structure
result = beam1.union(beam2)
