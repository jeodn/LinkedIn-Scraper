import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from pyvis.network import Network

# --- Load CSV ---
df = pd.read_csv('linkedin_mutual_connections_full.csv')  # replace with your real filename

# List of your connections
people = pd.concat([df['Person'], df['MutualConnection']]).drop_duplicates().tolist()
# Known mutual connections (edges between people)
mutual_connections = list(zip(df['Person'], df['MutualConnection']))


# WHICH VISUALIZATION VERSION ?
VIS_VERSION = "pyvis"  # networkx or pyvis

if VIS_VERSION == "pyvis":
    # --- Create PyVis Network ---
    net = Network(height='800px', width='100%', bgcolor='white', font_color='black')

    # Improve physics for nicer layout
    net.barnes_hut()

    # Add nodes
    for person in people:
        net.add_node(person, label=person, shape='dot', size=10)

    # Add edges
    for p1, p2 in mutual_connections:
        net.add_edge(p1, p2)

    # --- Show the network ---
    net.show('linkedin_social_network.html')

if VIS_VERSION == "networkx":
    # --- Create the graph ---
    G = nx.Graph()

    # Add people as nodes
    for person in people:
        G.add_node(person)

    # Add mutual connections as edges
    for p1, p2 in mutual_connections:
        G.add_edge(p1, p2)

    # --- Layout ---
    pos = nx.spring_layout(G, k=1.0, iterations=100, seed=42)

    # --- Draw ---
    plt.figure(figsize=(10, 8))
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=300)
    nx.draw_networkx_edges(G, pos, width=1.5, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=10)

    plt.title('Force-Directed LinkedIn Network', fontsize=18)
    plt.axis('off')
    plt.show()
