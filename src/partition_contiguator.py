from gerrychain.constraints.contiguity import contiguous_components
import numpy as np
from itertools import combinations
from gerrychain import Graph, Partition
from gerrychain.constraints import contiguous
from gerrychain.constraints.contiguity import contiguous_components

def contiguate(graph, districting):
    mutant_graph = graph.copy()
    if contiguous(districting):
        print("No work to do, districting is already contiguous.")
        return mutant_graph
    for part in districting.parts:
        precincts_idx = list(districting.parts[part])
        subset_partition = Partition(mutant_graph.subgraph(precincts_idx), assignment={x : 1 for x in precincts_idx},)
        if not contiguous(subset_partition):
            bridge_edges = find_bridge_edges(subset_partition)
            print(f"Adding {len(bridge_edges)} edges to connect district {part}")
            for e in bridge_edges:
                mutant_graph.add_edge(*e)
    assert contiguous(Partition(mutant_graph, assignment=districting.assignment))
    return mutant_graph

def find_bridge_edges(district_partition):
    components = list(contiguous_components(district_partition).values())[0]
    comp_to_node_ids_dict = {i: list(component.nodes) for i, component in enumerate(components)}
    number_of_edges_to_add = 5
    # iterate over every pair of components and add that many edges randomly
    edges_to_add = []
    for i, j in combinations(comp_to_node_ids_dict.keys(), 2):
        comp1_nodes = comp_to_node_ids_dict[i]
        comp2_nodes = comp_to_node_ids_dict[j]
        if len(comp1_nodes) <5:
            nodes_from_comp1 = np.random.choice(comp1_nodes, number_of_edges_to_add, replace=True)
        else:
            nodes_from_comp1 = np.random.choice(comp1_nodes, number_of_edges_to_add, replace=False)
        if len(comp2_nodes) <5:
            nodes_from_comp2 = np.random.choice(comp2_nodes, number_of_edges_to_add, replace=True)
        else:
            nodes_from_comp2 = np.random.choice(comp2_nodes, number_of_edges_to_add, replace=False)
        edges_to_add.extend(list(zip(nodes_from_comp1, nodes_from_comp2)))
    return edges_to_add