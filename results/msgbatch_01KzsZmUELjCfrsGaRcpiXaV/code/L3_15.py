import cadquery as cq
import math

# Parameters
major_axis = 200  # diameter direction
minor_axis = 100  # depth direction
wall_thickness = 8
cyl_height = 25

# Create inner semi-ellipsoid using a 2D profile revolved
# Create a sketch of half ellipse in XZ plane, then revolve around Z axis
inner_radius_major = major_axis / 2
inner_radius_minor = minor_axis / 2

# Create outer dimensions
outer_radius_major = inner_radius_major + wall_thickness
outer_radius_minor = inner_radius_minor + wall_thickness

# Build the inner elliptical head using extrude with taper
inner_head = (
    cq.Workplane("XY")
    .ellipse(inner_radius_major, inner_radius_minor)
    .extrude(inner_radius_minor, taper=90)
)

# Build the outer elliptical head
outer_head = (
    cq.Workplane("XY")
    .ellipse(outer_radius_major, outer_radius_minor)
    .extrude(outer_radius_minor, taper=90)
)

# Create inner cylinder at bottom
inner_cylinder = (
    cq.Workplane("XY")
    .circle(inner_radius_major)
    .extrude(-cyl_height)
)

# Create outer cylinder at bottom
outer_cylinder = (
    cq.Workplane("XY")
    .circle(outer_radius_major)
    .extrude(-cyl_height)
)

# Combine inner volumes
inner_volume = inner_head.union(inner_cylinder)

# Combine outer volumes
outer_volume = outer_head.union(outer_cylinder)

# Create the tank cover wall by subtracting inner from outer
tank_cover = outer_volume.cut(inner_volume)

# Create the flange at the vertex (top of the ellipsoid)
flange_outer_radius = 20  # outer diameter 40mm
flange_inner_radius = 15  # inner diameter 30mm
flange_height = 30

# Build flange as a disk with hole, positioned at top
flange_solid = (
    cq.Workplane("XY")
    .circle(flange_outer_radius)
    .extrude(flange_height)
)

flange_hole = (
    cq.Workplane("XY")
    .circle(flange_inner_radius)
    .extrude(flange_height)
)

flange = flange_solid.cut(flange_hole)

# Combine tank cover with flange
result = tank_cover.union(flange)
