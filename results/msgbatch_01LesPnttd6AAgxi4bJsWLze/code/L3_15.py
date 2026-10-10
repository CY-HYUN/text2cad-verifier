import cadquery as cq
import math

# Create the main tank cover body
# Inner semi-ellipse with major axis 200mm, minor axis 100mm
major_axis = 200  # diameter direction
minor_axis = 100  # depth direction
wall_thickness = 8

# Create inner semi-ellipse profile
inner_semi_ellipse = cq.Workplane("XY").ellipse(major_axis/2, minor_axis/2).revolve(180, (1, 0, 0))

# Create outer semi-ellipse (offset by wall thickness)
outer_major = (major_axis + 2*wall_thickness) / 2
outer_minor = (minor_axis + wall_thickness) / 2
outer_semi_ellipse = cq.Workplane("XY").ellipse(outer_major, outer_minor).revolve(180, (1, 0, 0))

# Create the cylindrical straight section at the bottom (height 25mm)
cyl_height = 25
inner_cyl_radius = major_axis / 2
outer_cyl_radius = inner_cyl_radius + wall_thickness

# Build the inner cylinder
inner_cylinder = cq.Workplane("XY").circle(inner_cyl_radius).extrude(-cyl_height)

# Build the outer cylinder
outer_cylinder = cq.Workplane("XY").circle(outer_cyl_radius).extrude(-cyl_height)

# Create the hemi-ellipsoid by revolving semi-ellipse
# Position the semi-ellipse properly for revolution around Y axis
inner_ellipsoid_profile = (
    cq.Workplane("XZ")
    .moveTo(major_axis/2, 0)
    .ellipse(major_axis/2, minor_axis/2, rotation=0)
    .revolve(360, (0, 1, 0), (-major_axis/2, 0, 0), (major_axis/2, 0, 0))
)

outer_ellipsoid_profile = (
    cq.Workplane("XZ")
    .moveTo(outer_major, 0)
    .ellipse(outer_major, outer_minor, rotation=0)
    .revolve(360, (0, 1, 0), (-outer_major, 0, 0), (outer_major, 0, 0))
)

# Create the elliptical head (hemi-ellipsoid) + cylinder assembly
# Inner volume
inner_head = cq.Workplane("XY").ellipse(major_axis/2, minor_axis/2).extrude(0, taper=90)
inner_with_cyl = inner_head.union(inner_cylinder)

# Outer volume  
outer_head = cq.Workplane("XY").ellipse(outer_major, outer_minor).extrude(0, taper=90)
outer_with_cyl = outer_head.union(outer_cylinder)

# Create solid wall by subtracting inner from outer
tank_cover = outer_with_cyl.cut(inner_with_cyl)

# Create the flange at the vertex
# Outer diameter 40mm, inner diameter 30mm, height 30mm
flange_outer_radius = 20
flange_inner_radius = 15
flange_height = 30

# Position flange at the top vertex of ellipsoid
flange_outer = cq.Workplane("XY").circle(flange_outer_radius).extrude(flange_height)
flange_hole = cq.Workplane("XY").circle(flange_inner_radius).extrude(flange_height)
flange = flange_outer.cut(flange_hole)

# Combine the main body with the flange
result = tank_cover.union(flange)
