#!/usr/bin/env python3


import matplotlib.pyplot as plt
from svgpathtools import svg2paths

# Load the SVG file created in Inkscape
finger_paths, attributes = svg2paths(
    "hand_pic.svg"
)  # Replace 'your_hand_outline.svg' with your file path

fig, ax = plt.subplots(figsize=(8, 8))  # Setting a square figure size

# Plot the finger outline
for path in finger_paths:
    vertices = [segment.start for segment in path]
    x, y = zip(
        *[(point.real, -point.imag) for point in vertices]
    )  # Adjusting the y-coordinates
    ax.plot(x, y, color="black")

# Define coordinates for thumb's end
thumb_end_x = 150

thumb_end_y = 250

# Create inset for pie donut plot at thumb's end
thumb_inset = fig.add_axes(
    [thumb_end_x / 1000, (thumb_end_y + 250) / 1000, 0.2, 0.2]
)  # Adjust the size as needed

# Data for the pie donut plot
sizes = [25, 35, 20, 20]  # Sizes of different parts of the donut
labels = ["A", "B", "C", "D"]  # Labels for each part

# Plot the pie donut at the thumb's end
thumb_inset.pie(sizes, labels=labels, wedgeprops=dict(width=0.4))
thumb_inset.set_aspect("equal")


plt.title("Hand Outline from Inkscape")
# plt.axis("equal")


plt.savefig(
    "hand.png",
)
