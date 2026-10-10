import cadquery as cq
import math

# Create the base rectangle on the XY plane
base = cq.Workplane("XY").rect(100, 50).extrude(5.0)

# Create fins using a simpler approach with loft/sweep
# Create 5 fins with sine wave paths along the Y-axis

fins_model = base

for fin_idx in range(5):
    # Y position for this fin
    fin_y = -20 + fin_idx * 10.0
    
    # Create the sine curve profile at the top of the base
    curve_points = []
    for i in range(101):
        x = -50 + i * 100.0 / 100
        y_offset = 2 * math.sin(0.2 * math.pi * (i / 100.0 * 100))
        y = fin_y + y_offset
        z = 5.0
        curve_points.append((x, y, z))
    
    # Create top edge points (extended in Z direction by 30mm)
    top_points = []
    for i in range(101):
        x = -50 + i * 100.0 / 100
        y_offset = 2 * math.sin(0.2 * math.pi * (i / 100.0 * 100))
        y = fin_y + y_offset
        z = 35.0  # 5.0 + 30.0
        top_points.append((x, y, z))
    
    # Create a loft between the bottom curve and top curve
    bottom_wire = cq.Workplane("XY").polyline(curve_points).wire()
    top_wire = cq.Workplane("XY").polyline(top_points).wire()
    
    # Create a thin wall fin using loft and then offset
    fin_solid = cq.Workplane("XY").add(bottom_wire).loft(cq.Workplane("XY").add(top_wire).wire(), ruled=True)
    
    # Create a shell by using offset to make it thin-walled (1mm thickness)
    try:
        fin_shell = fin_solid.shell(1.0)
        fins_model = fins_model.union(fin_shell)
    except:
        # If shell fails, just union the lofted solid
        fins_model = fins_model.union(fin_solid)

result = fins_model
