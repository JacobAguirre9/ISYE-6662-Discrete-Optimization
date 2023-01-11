import gurobipy as gp

def knapsack(items, weights, values, capacity):
    """
    Solve the knapsack problem using Gurobi.

    Parameters:
    - items: list of strings representing the items
    - weights: list of floats representing the weight of each item
    - values: list of floats representing the value of each item
    - capacity: float representing the maximum weight that can be carried

    Returns:
    - A tuple containing the optimal objective value and a dictionary of items and whether or not they are in the knapsack
    """

    # Create a new Gurobi model
    model = gp.Model()

    # Create binary variables for each item
    x = model.addVars(items, vtype=gp.GRB.BINARY, name='x')

    # Add the objective function: maximize the sum of the item values
    model.setObjective(gp.quicksum(x[i]*v for i, v in zip(items, values)), gp.GRB.MAXIMIZE)

    # Add the constraint that the total weight of the items in the knapsack cannot exceed the capacity
    model.addConstr(gp.quicksum(x[i]*w for i, w in zip(items, weights)) <= capacity)

    # Solve the model
    model.optimize()

    # Extract the solution
    selected_items = {i: x[i].x > 0.5 for i in items}

    return model.objVal, selected_items

