import cadquery as cq
import math

# Create the hollow spherical shell
outer_radius = 25  # outer diameter 50mm
inner_radius = 20  # inner diameter 40mm

# Create outer sphere
outer_sphere = cq.Workplane("XY").sphere(outer_radius)

# Create inner sphere
inner_sphere = cq.Workplane("XY").sphere(inner_radius)

# Create hollow shell by cutting inner from outer
shell = outer_sphere.cut(inner_sphere)

# Create a reference plane perpendicular to X-axis, located outside the sphere
# Plane at X = 30 (outside the sphere which goes to 25)
reference_plane = cq.Workplane("YZ").workplane(offset=30)

# Draw a 20x20mm square on this plane, centered on the X-axis (centered on Y-Z plane)
square = reference_plane.rect(20, 20, centered=True).extrude(60, both=True)

# Cut the square through the shell using a through-all extrude
# Create a cutting box that goes through the sphere
cut_tool = cq.Workplane("YZ").workplane(offset=0).rect(20, 20, centered=True).extrude(60, both=True)

# Apply the cut to create the window
result = shell.cut(cut_tool)
