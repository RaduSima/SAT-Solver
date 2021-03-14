import sys
from time import time

# Node class, through which the tree will be represented
class Node: 
    def __init__(self,key): 
        self.left = None
        self.right = None
        self.val = key 

"""
  An exact copy of the "get_matrix" function used in the FNC-SAT algorithm,
the only difference being that it also returns a list of the variable names,
in order to properly remember them inside the tree
""" 
def get_matrix_and_nodes(fnc):
    fnc = fnc.replace("(", "")
    fnc = fnc.replace(")", "")
    clauses = fnc.split("^")
    clauses_number = len(clauses)
    for i in range(clauses_number):
        clauses[i] = clauses[i].split("V")
    
    dict = {}
    for i in range(clauses_number):
        for variable in clauses[i]:
            negate = False
            if variable[0] == "~":
                negate = True
                variable = variable.replace("~", "")
            column = dict.get(variable)
            if column == None:
                column = [0] * clauses_number
            if negate:
                column[i] = -1
            else:
                column[i] = 1
            dict.update({variable: column})
          
    keys = list(dict.keys())
    matrix = list(dict.values())
    transposed_matrix = []
    for element_index in range(len(matrix[0])):
        line = []
        for l in matrix:
            line.append(l[element_index])
        transposed_matrix.append(line)
        
    return [keys, transposed_matrix]

"""
   Function that creates the actual tree and gets the problem result
   The result paramether is only here in order to not have to traverse
 the tree to find if there exists a valid configuration of the variables,
 but the tree still gets fully built
"""
def create_tree(nodes_list, M, result):
    root = Node(nodes_list[0])
    root.left = create_node(nodes_list, M, 0, False, result)
    root.right = create_node(nodes_list, M, 0, True, result)
    return root

# Recursive function that creates the nodes of the tree
def create_node(nodes_list, M, parent_level, parent_truth_value, result):
    
    # Updates the matrix
    new_M = update_matrix(nodes_list, M, parent_level, parent_truth_value)
    
    """
      If it the function has reached the leaves of the tree, it checks if
    the matrix is empty - if it is, then a valid configuration has been found;
    otherwise, the configuration is not valid
    """
    if parent_level == (len(nodes_list) - 1):
        if len(new_M) == 0:
            new_node = Node(True)
            result[0] = 1
        else:
            new_node = Node(False)
    else:
        new_node = Node(nodes_list[parent_level + 1])
        new_node.left = create_node(nodes_list, new_M, parent_level + 1, False, result)
        new_node.right = create_node(nodes_list, new_M, parent_level + 1, True, result)
    return new_node

# Helper function that updates the matrix corresponding to each node
def update_matrix(nodes_list, M, variable_index, variable_truth_value):
    
    # Creates a deep copy of the matrix
    new_M = [row[:] for row in M]
    
    # Iterates through all the clauses
    clause_index = 0
    while clause_index < len(new_M):
        
        """
          Replaces the current variable with it's truth value
          If it is true, the current clause gets deleted
          If it is false, the corresponding position inside the matrix becomes 0
        """
        if new_M[clause_index][variable_index] != 0:
            if new_M[clause_index][variable_index] == -1:
                variable_truth_value = not variable_truth_value
            if variable_truth_value:
                new_M.pop(clause_index)
                clause_index -= 1
            else:
                new_M[clause_index][variable_index] = 0   
        clause_index += 1
    return new_M

# Actual driver program, reads input and calls the other functions
begin_time = time()

f = open(sys.argv[1],"r")
g = open("bdd.out", "a")
fnc = f.read()
f.close()

[nodes, M] = get_matrix_and_nodes(fnc)
result = [0]
tree = create_tree(nodes, M, result)
print(result[0])

end_time = time() - begin_time
g.write(str(len(nodes)) + ' ' + str(end_time) + '\n')
g.close()
