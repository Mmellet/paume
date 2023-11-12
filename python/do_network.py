#!/usr/bin/env python3


import networkx as nx

import numpy as np

import matplotlib.pyplot as plt

from matplotlib.patches import ConnectionPatch
from matplotlib.path import Path
from matplotlib.patches import PathPatch


def get_midpoint(wedge):
    theta1, theta2 = wedge.theta1, wedge.theta2
    theta_mid = (theta1 + theta2) / 2
    r = wedge.r
    return r * np.cos(np.deg2rad(theta_mid)), r * np.sin(np.deg2rad(theta_mid))


def main3():
    sizes_1 = [25, 35, 20, 20]  # Sizes of slices for the first donut chart
    sizes_2 = [30, 25, 15, 30]  # Sizes of slices for the second donut chart
    labels_1 = [
        "Slice 1",
        "Slice 2",
        "Slice 3",
        "Slice 4",
    ]  # Labels for the first donut chart
    labels_2 = [
        "Slice A",
        "Slice B",
        "Slice C",
        "Slice D",
    ]  # Labels for the second donut chart
    edge_labels = [
        "Edge 1-2",
        "Edge 2-3",
        "Edge 3-4",
        "Edge 4-1",
    ]  # Labels for connecting edges

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    # First donut chart
    axs[0].pie(sizes_1, labels=labels_1, wedgeprops=dict(width=0.4), startangle=90)
    axs[0].axis("equal")

    # Second donut chart
    axs[1].pie(sizes_2, labels=labels_2, wedgeprops=dict(width=0.4), startangle=90)
    axs[1].axis("equal")

    for i in range(len(sizes_1)):
        current_wedge_1 = axs[0].patches[i]
        next_index = (i + 1) % len(
            sizes_1
        )  # Connect the last slice to the first in the loop
        current_wedge_2 = axs[1].patches[next_index]

        # Get midpoints of the edges of the wedges for both charts
        center_current_1 = get_midpoint(current_wedge_1)
        center_current_2 = get_midpoint(current_wedge_2)

        # Control point for the quadratic Bézier curve to connect the two donut charts
        control_point = (
            (center_current_1[0] + center_current_2[0]) / 2,
            (center_current_1[1] + center_current_2[1]) / 2,
        )

        # Plot a quadratic Bézier curve between midpoints of the edges of the wedges
        verts = [center_current_1, control_point, center_current_2]
        codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3]
        path = Path(verts, codes)
        path_patch = PathPatch(path, edgecolor="black", facecolor="none")
        axs[1].add_patch(path_patch)

        # Add labels for the edges connecting the two donut charts
        edge_label_x = control_point[0]
        edge_label_y = control_point[1]
        edge_label = edge_labels[i]
        plt.text(edge_label_x, edge_label_y, edge_label, ha="center", va="center")

    plt.suptitle("Two Side-by-Side Donut Charts with Connecting Edges and Labels")

    plt.savefig(
        "donut_chart.png",
    )


def main2():
    sizes = [25, 35, 20, 20]  # Sizes of different parts of the donut
    labels = ["Slice 1", "Slice 2", "Slice 3", "Slice 4"]  # Labels for each part
    edge_labels = ["Edge 1-2", "Edge 2-3", "Edge 3-4"]  # Labels for each edge

    fig, ax = plt.subplots()
    wedges, texts = ax.pie(
        sizes, labels=labels, wedgeprops=dict(width=0.4), startangle=90
    )
    ax.axis("equal")

    for i in range(len(wedges) - 1):
        current_wedge = wedges[i]
        next_wedge = wedges[i + 1]

        # Get midpoints of the edges of the wedges
        center_current = get_midpoint(current_wedge)
        center_next = get_midpoint(next_wedge)

        # Control point for the quadratic Bézier curve
        control_point = (center_current[0], center_next[1])

        # Plot a quadratic Bézier curve between midpoints of the edges of the wedges
        verts = [center_current, control_point, center_next]
        codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3]
        path = Path(verts, codes)
        path_patch = PathPatch(path, edgecolor="black", facecolor="none")
        ax.add_patch(path_patch)

        # Add labels for the edges
        edge_label_x = control_point[0]
        edge_label_y = control_point[1]

        edge_label = edge_labels[i]
        plt.text(edge_label_x, edge_label_y, edge_label, ha="center", va="center")

    plt.title("Donut Chart with Edges")

    plt.savefig("donut_chart.svg", format="svg")


def main():
    G = nx.complete_graph(5)
    A = nx.nx_agraph.to_agraph(G)  # convert to a graphviz graph
    X1 = nx.nx_agraph.from_agraph(A)  # convert back to networkx (but as Graph)
    X2 = nx.Graph(A)  # fancy way to do conversion
    G1 = nx.Graph(X1)  # now make it a Graph

    A.write("k5.dot")  # write to dot file
    X3 = nx.nx_agraph.read_dot("k5.dot")  # read from dotfile

    # You can also create .png directly with the AGraph.draw method
    A.draw("k5.png", prog="neato")


if __name__ == "__main__":
    pass
    main3()
