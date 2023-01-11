# This is a Python and Gurobi implementation of the Maximum Weight Spanning Tree (MWST) algorithm. 
# Authors: @jacobaguirre

import gurobipy as gp

def max_weight_spanning_tree(edges, weights):
    """
    Compute a maximum weight spanning tree using Gurobi.

    Parameters:
    - edges: list of tuples representing the edges in the graph
    - weights: list of floats representing the weight of each edge

    Returns:
    - A tuple containing the optimal objective value and a list of edges in the maximum weight spanning tree
    """
    # Create a new Gurobi model
    model = gp.Model()

    # Create binary variables for each edge
    x = model.addVars(edges, vtype=gp.GRB.BINARY, name='x')

    # Add the objective function: maximize the sum of the edge weights
    model.setObjective(gp.quicksum(x[e] * w for e, w in zip(edges, weights)), gp.GRB.MAXIMIZE)

    # Add the constraint that each vertex must be included in exactly one edge
    for v in set().union(*edges):
        model.addConstr(gp.quicksum(x[e] for e in edges if v in e) <= 1)

    # Add the constraint that only one edge can be selected per pair of nodes
    for i in range(len(edges)):
        for j in range(i + 1, len(edges)):
            if set(edges[i]).intersection(edges[j]):
                model.addConstr(x[edges[i]] + x[edges[j]] <= 1)

    # Solve the model
    model.optimize()

    # Extract the edges of the maximum weight spanning tree
    selected_edges = [e for e in edges if x[e].x > 0.5]

    return model.objVal, selected_edges
