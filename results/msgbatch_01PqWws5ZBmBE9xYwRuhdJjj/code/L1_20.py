import cadquery as cq

# Create a new workplane on the XZ plane
wp = cq.Workplane("XZ")

# Draw the trapezoidal profile in the XZ plane
# Base is along the X-axis from (0,0) to (80,0)
# Left end (at x=0) goes up to height 30mm
# Right end (at x=80) goes up to height 5mm
# Trapezoid vertices: (0,0) -> (80,0) -> (80,5) -> (0,30) -> back to (0,0)

trapezoid = wp.polyline([
    (0, 0),      # Bottom left
    (80, 0),     # Bottom right
    (80, 5),     # Top right (height 5mm)
    (0, 30),     # Top left (height 30mm)
]).close()

# Extrude the trapezoidal profile along the +Y direction with width 40mm
result = trapezoid.extrude(40.0)
