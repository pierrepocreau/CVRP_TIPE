from algo import Solver
import matplotlib.pyplot as plt
import os
import pickle
import random

def gain_operation(solver, op, n1, n2):
    if op == "reloc": return solver.relocate_conditions(n1, n2)
    elif op == "swap": return solver.swap_conditions(n1, n2)
    elif op == "invert": return solver.invert_conditions(n1, n2)
    elif op == "tail_swap": return solver.swap_tail_conditions(n1, n2)
    
def exe_operation(solver, op, n1, n2, gain, verbose = False):
    if op == "reloc": return solver.relocate(n1, n2, gain, verbose)
    elif op == "swap": return solver.swap(n1, n2, gain, verbose)
    elif op == "invert": return solver.invert(n1, n2, gain, verbose)
    elif op == "tail_swap": return solver.swap_tail(n1, n2, gain, verbose)

def resolution(data, affichage = False, localsearch = False, verbose = False):
    solver = Solver(data, 100)
    solver.calcule_temps_eco()

    for couple in solver.temps_economise:
        solver.contrainte_fusion(couple[0][0], couple[0][1])
    
    print(solver.cout_solution())
    solver.show(1)
    if localsearch:
        while True:
            gain_max, best_op, n1, n2 = 0, "", 0, 0
            #for operation in ["reloc", "swap", "invert", "tail_swap"]:
            for operation in ["tail_swap", "invert", "swap", "reloc"]:
                for c1 in solver.data[1:]:
                    for c2 in solver.data[1:]:
                        gain = solver.operation_condition(operation, c1, c2)
                        if gain > gain_max and c1 != c2:
                            gain_max, best_op = gain, operation
                            n1, n2 = c1, c2
            if gain_max > 0.1:
                exe_operation(solver, best_op, n1, n2, gain_max, verbose)
            else: break
    
        #if verbose: 
        #    print("nombres de routes:", len(solver.routes))
        solver.show(2)

        if affichage: plt.show()

    else:
        print("Cout: ", solver.cout_solution())
        if affichage: plt.show()
    
    print(solver.cout_solution())
    return (solver.cout_solution(), solver.routes)

if __name__ == "__main__":
    data = pickle.load(open("data.p", "rb"))
    cout, routes = resolution(data, True, True, True)
    print(cout)