import cadquery as cq
import math

# Create the four datum planes at different X positions
# Plane1 at X=0
plane1_circle = cq.Workplane("XY").circle(15/2).face()

# Plane2 at X=50 - ellipse with major axis 25mm, minor axis 20mm
plane2_ellipse = cq.Workplane("XY").ellipse(25/2, 20/2).face()

# Plane3 at X=100 - ellipse with major axis 22mm, minor axis 18mm
plane3_ellipse = cq.Workplane("XY").ellipse(22/2, 18/2).face()

# Plane4 at X=150 - circle with 20mm diameter
plane4_circle = cq.Workplane("XY").circle(20/2).face()

# Create guide spline curve with control points P0(0,0), P1(30,20), P2(100,25), P3(150,5)
# We'll create this as a 3D curve in the XZ plane (Y=0)
guide_points = [(0, 0, 0), (30, 0, 20), (100, 0, 25), (150, 0, 5)]

# Create sections at each X position
# Section 1: Circle at X=0 (15mm diameter)
section1 = cq.Workplane("YZ").transformed(offset=(0, 0, 0)).circle(15/2)

# Section 2: Ellipse at X=50 (major 25mm, minor 20mm)
section2 = cq.Workplane("YZ").transformed(offset=(50, 0, 0)).ellipse(25/2, 20/2)

# Section 3: Ellipse at X=100 (major 22mm, minor 18mm)
section3 = cq.Workplane("YZ").transformed(offset=(100, 0, 0)).ellipse(22/2, 18/2)

# Section 4: Circle at X=150 (20mm diameter)
section4 = cq.Workplane("YZ").transformed(offset=(150, 0, 0)).circle(20/2)

# Build the lofted solid using multi-section lofting
# We create wire frames for each section
wire1 = cq.Workplane("YZ").transformed(offset=(0, 0, 0)).circle(15/2).val().Edges()[0]
wire2 = cq.Workplane("YZ").transformed(offset=(50, 0, 0)).ellipse(25/2, 20/2).val().Edges()[0]
wire3 = cq.Workplane("YZ").transformed(offset=(100, 0, 0)).ellipse(22/2, 18/2).val().Edges()[0]
wire4 = cq.Workplane("YZ").transformed(offset=(150, 0, 0)).circle(20/2).val().Edges()[0]

# Create a lofted surface through the sections
lofted = cq.Workplane("XY").loft([wire1, wire2, wire3, wire4], ruled=False)

# Convert to solid by creating faces between sections
base = cq.Workplane("YZ").circle(15/2).extrude(0.01)
for i, section in enumerate([section1, section2, section3, section4]):
    pass

# Alternative approach: Create a simple loft by building intermediate shapes
# Create approximate lofted solid
profiles = []

# Profile at X=0: circle
prof1 = cq.Workplane("YZ").transformed(offset=(0, 0, 0)).circle(15/2)
profiles.append(prof1.val().Edges()[0])

# Profile at X=50: ellipse
prof2 = cq.Workplane("YZ").transformed(offset=(50, 0, 0)).ellipse(25/2, 20/2)
profiles.append(prof2.val().Edges()[0])

# Profile at X=100: ellipse
prof3 = cq.Workplane("YZ").transformed(offset=(100, 0, 0)).ellipse(22/2, 18/2)
profiles.append(prof3.val().Edges()[0])

# Profile at X=150: circle
prof4 = cq.Workplane("YZ").transformed(offset=(150, 0, 0)).circle(20/2)
profiles.append(prof4.val().Edges()[0])

# Create lofted solid
lofted_solid = cq.Workplane("XY").loft(profiles, ruled=False)

# Apply shell operation: remove the two end faces and set wall thickness to 1.5mm
result = lofted_solid.val().shell(1.5)

# Create final workplane object
result = cq.Workplane("XY").add(result)
