import cadquery as cq
import math

# Create the Laval Nozzle as an axisymmetric body of revolution

# Parameters
inlet_flange_dia = 60
outlet_flange_dia = 60
flange_thickness = 5
convergent_length = 20
divergent_length = 80
total_length = convergent_length + divergent_length
throat_diameter = 10
throat_radius = throat_diameter / 2
exit_diameter = 40
exit_radius = exit_diameter / 2
inlet_arc_radius = 50
max_outer_diameter = 60
max_outer_radius = max_outer_diameter / 2

# Create a 2D profile that will be revolved around the axis
# The profile is drawn on the XZ plane (X = radial, Z = axial)

# Start building the profile from left to right (inlet to outlet)
profile_points = []

# 1. Inlet flange start (left edge, at outer radius)
profile_points.append((max_outer_radius, 0))

# 2. Inlet flange inner edge
profile_points.append((inlet_flange_dia/2, 0))

# 3. Transition from flange to inlet curved section
# Create smooth inlet with 50mm radius arc
inlet_start_z = flange_thickness
inlet_arc_start_radius = inlet_flange_dia / 2

# The arc connects from inlet_arc_start_radius at z=flange_thickness to throat_radius at z=convergent_length
# Using a circular arc with radius 50mm

# Build the convergent section with arc
convergent_arc = cq.Workplane("XZ").moveTo(inlet_arc_start_radius, inlet_start_z)

# Calculate the center of the inlet arc
# Arc goes from (inlet_arc_start_radius, inlet_start_z) to (throat_radius, convergent_length)
# with radius 50mm
arc_center_x = inlet_arc_start_radius - inlet_arc_radius
arc_center_z = inlet_start_z

# Create inlet curve points
for i in range(21):
    t = i / 20.0
    angle = math.asin((convergent_length - arc_center_z) / inlet_arc_radius)
    theta = -math.pi/2 + angle * t
    x = arc_center_x + inlet_arc_radius * math.cos(theta)
    z = arc_center_z + inlet_arc_radius * math.sin(theta)
    if x > 0:
        profile_points.append((x, z))

# 4. Throat (narrowest section)
profile_points.append((throat_radius, convergent_length))

# 5. Divergent (expansion) section with parabolic shape
# Parabola: opens from throat towards exit
# Vertex at throat: (throat_radius, convergent_length)
# Passes through: (exit_radius, convergent_length + divergent_length)
# Parabola equation: r = a*(z - z_vertex)^2 + r_vertex
# At z = convergent_length + divergent_length: exit_radius = a * divergent_length^2 + throat_radius
# a = (exit_radius - throat_radius) / divergent_length^2

a = (exit_radius - throat_radius) / (divergent_length ** 2)

for i in range(1, 81):
    z_offset = i
    z = convergent_length + z_offset
    r = a * (z_offset ** 2) + throat_radius
    profile_points.append((r, z))

# 6. Exit point
profile_points.append((exit_radius, total_length))

# 7. Outlet flange outer edge
profile_points.append((outlet_flange_dia/2, total_length))

# 8. Outer wall contour (elliptical arc for structural strength)
# Create outer radius arc connecting inlet flange to outlet flange
outer_profile_points = []

# Inlet flange (outer)
outer_profile_points.append((max_outer_radius, 0))
outer_profile_points.append((max_outer_radius, flange_thickness))

# Outer body elliptical profile
for i in range(101):
    t = i / 100.0
    z = flange_thickness + t * total_length
    # Simple elliptical transition from max_outer_radius back to outlet_flange_dia/2
    r = max_outer_radius - (max_outer_radius - outlet_flange_dia/2) * t
    outer_profile_points.append((r, z))

outer_profile_points.append((outlet_flange_dia/2, flange_thickness + total_length))
outer_profile_points.append((outlet_flange_dia/2, total_length + flange_thickness))

# 9. Outlet flange (outer)
outer_profile_points.append((outlet_flange_dia/2, total_length + flange_thickness))
outer_profile_points.append((max_outer_radius, total_length + flange_thickness))
outer_profile_points.append((max_outer_radius, total_length))

# Create the complete profile for revolution
sketch = cq.Workplane("XZ")

# Draw the outer profile
sketch = sketch.moveTo(max_outer_radius, 0)
sketch = sketch.lineTo(inlet_flange_dia/2, 0)
sketch = sketch.lineTo(inlet_flange_dia/2, flange_thickness)

# Inner inlet curve
prev_point = (inlet_flange_dia/2, flange_thickness)
for pt in profile_points[3:-1]:
    sketch = sketch.lineTo(pt[0], pt[1])
    prev_point = pt

# Inner outlet curve
sketch = sketch.lineTo(outlet_flange_dia/2, total_length)
sketch = sketch.lineTo(outlet_flange_dia/2, total_length + flange_thickness)
sketch = sketch.lineTo(max_outer_radius, total_length + flange_thickness)
sketch = sketch.lineTo(max_outer_radius, total_length)
sketch = sketch.lineTo(max_outer_radius, flange_thickness)
sketch = sketch.lineTo(max_outer_radius, 0)
sketch = sketch.close()

# Revolve the sketch around the Z axis to create the 3D nozzle
result = sketch.revolve(360, (0, 0, 0), (0, 0, 1))
