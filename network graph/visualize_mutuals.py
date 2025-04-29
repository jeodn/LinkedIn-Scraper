import pandas as pd
import networkx as nx
from pyvis.network import Network

# --- Load your CSV ---
df = pd.read_csv('linkedin_mutual_connections_full.csv')

# List of all names
people = pd.concat([df['Person'], df['MutualConnection']]).drop_duplicates().tolist()

# List of edges
mutual_connections = list(zip(df['Person'], df['MutualConnection']))

# --- Create a networkx Graph (for community detection) ---
G = nx.Graph()
G.add_edges_from(mutual_connections)

# --- Detect communities (friend groups) using greedy modularity ---
from networkx.algorithms.community import greedy_modularity_communities

communities = list(greedy_modularity_communities(G))

# Map person -> community ID
community_map = {}
for idx, community in enumerate(communities):
    for person in community:
        community_map[person] = idx

# --- Create PyVis Graph ---
net = Network(height='800px', width='100%', bgcolor='white', font_color='black')
net.barnes_hut()

# --- Add nodes ---
for person in people:
    degree = G.degree(person)  # Number of connections

    community_id = community_map.get(person, 0)  # Default to 0 if missing

    net.add_node(
        person,
        label=person,
        title=f'{person}\nConnections: {degree}',  # Hover tooltip
        group=community_id,                         # Cluster group
        size=10 + degree * 2                        # Bigger if more connected
    )

# --- Add edges ---
for p1, p2 in mutual_connections:
    net.add_edge(p1, p2)

# --- Save and show ---
net.show('linkedin_social_network_clustered.html')
