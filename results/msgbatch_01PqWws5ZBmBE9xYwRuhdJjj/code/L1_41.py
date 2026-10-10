import cadquery as cq
import math

# Create a new workplane with default XY plane as base
result = cq.Workplane("XY")

# Draw a circle (diameter 100.0 mm) and extrude it by 10.0 mm to form the disc
disc = result.circle(50.0).extrude(10.0)

# Select the top surface for adding holes
top_surface = disc.faces(">Z").workplane()

# Create a hole at a specific position on the distribution circle
# Distribution circle radius: 35.0 mm
# Hole diameter: 10.0 mm (radius 5.0 mm)
# First hole positioned at angle 0 degrees
distribution_radius = 35.0
hole_radius = 5.0

# Calculate the position of the first hole
hole_x = distribution_radius * math.cos(0)
hole_y = distribution_radius * math.sin(0)

# Move to the hole position and create the hole
hole = top_surface.moveTo(hole_x, hole_y).circle(hole_radius).cutThruAll()

# Create a pattern of 4 holes equally spaced around the Z-axis
# with 360 degrees total angle (90 degrees apart)
result = hole.polarArray(radius=distribution_radius, count=4, angle=360)

