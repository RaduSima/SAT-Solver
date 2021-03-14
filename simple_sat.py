import sys
from time import time

# Function that transforms the SAT problem from a string representation 
#to a matrix one
def get_matrix(fnc):
    
    # Splits the string into a list of clauses and eliminates the parentheses
    fnc = fnc.replace("(", "")
    fnc = fnc.replace(")", "")
    clauses = fnc.split("^")
    
    # Splits the clauses into lists of variables
    clauses_number = len(clauses)
    for i in range(clauses_number):
        clauses[i] = clauses[i].split("V")
    
    """
     Creates a dictionary of lists of 0, 1 and -1,
    with the keys being strings (the variables)
     This is done so it is assured that the variables will not 
    repeat themselves inside the matrix
    """   
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
          
    """
      Creates the actual matrix from the dictionary (a list of lists) and
     transposes it, in order to have the clauses as lines and
     the variables as columns
    """
    matrix = list(dict.values())
    transposed_matrix = []
    for element_index in range(len(matrix[0])):
        line = []
        for l in matrix:
            line.append(l[element_index])
        transposed_matrix.append(line)
        
    return transposed_matrix

# Recursive function that solves the SAT problem given a matrix 
#reprezentation and returns True or False
def solve_fnc(M, configuration):
    
    # If the configuration is final, checks if it is a valid one
    if len(M[0]) == len(configuration):
        
        # Iterates through all the clauses in the matrix
        for clause in M:
            flag = False
            
            # Iterates through all the variables in a clause and replaces them
            #with their corresponding truth value 
            for variable_index in range(len(clause)):
                if clause[variable_index] == 1:
                    if configuration[variable_index]:
                        flag = True
                        break
                elif clause[variable_index] == -1:
                    if not configuration[variable_index]:
                        flag = True
                        break
            if not flag:
                return False
        return True
    
    # Checks all possible configurations of variables
    for v in [True, False]:
        new_configuration = list(configuration)
        new_configuration.append(v)
        if solve_fnc(M, new_configuration):
            return True
        
    # From here, all paths return False
    return False
    
# Actual driver program, reads input and calls the other functions
begin_time = time()

f = open(sys.argv[1],"r")
g = open("simple.out", "a")
fnc = f.read()
f.close()

M = get_matrix(fnc)
result = solve_fnc(M, [])
if result:
    print(1)
else:
    print(0)

end_time = time() - begin_time
g.write(str(len(M[0])) + ' ' + str(end_time) + '\n')
g.close()
