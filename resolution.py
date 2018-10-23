from algo import Solver
import matplotlib.pyplot as plt
import os
import pickle

def full_swap(solver, data, verbose = False):
    #test tous les cas possibles
    if verbose: print("\n Swap")

    for c1 in solver.data[1:]:
        for c2 in solver.data[c1.id:]:
            if c1 != c2:
                solver.swap_conditions(c1, c2, verbose)

    if verbose: print("cout après swap", solver.cout_solution())

def full_relocate(solver, data, verbose = False):
        #test tous les cas possibles
        if verbose: print("\n relocate")

        for c1 in solver.data[1:]:
            for c2 in solver.data[c1.id:]:
                if c1 != c2:
                    solver.relocate_conditions(c1, c2, verbose)

        if verbose: print("cout après relocate", solver.cout_solution())

def full_invert(solver, data, verbose = False):
        #pareil
        if verbose: print("\n invert")

        for c1 in solver.data[1:]:
            for c2 in solver.data[c1.id:]:
                if c1 != c2:
                    solver.invert_conditions(c1, c2, verbose)

        if verbose: print("cout après invert", solver.cout_solution())

def full_swap_tail(solver, data, verbose = False):
        if verbose: print("\n swap_tail")

        for c1 in solver.data[1:]:
            for c2 in solver.data[c1.id:]:
                if c1 != c2:
                    solver.swap_tail_conditions(c1, c2, verbose)

        if verbose: print("cout après swap_tail", solver.cout_solution())

def resolution(data, affichage = False, localsearch = False, verbose = False):
    solver = Solver(data, 100)
    solver.calcule_temps_eco()

    #construit la premiere solution
    for couple in solver.temps_economise:
        solver.contrainte_fusion(couple[0][0], couple[0][1])

    solver.show(1)


    if localsearch:
        cout = 0

        if verbose:
            print("cout construction:", solver.cout_solution())
            print("nombres de routes:", len(solver.routes))

        while abs(solver.cout_solution() - cout) > 5:
            cout = solver.cout_solution()
            solver.del_routes_vide()

            #il faudrait trouver la meuilleur combinaison
            #full_relocate(solver, data, verbose)
            #full_swap(solver, data, verbose)
            #full_invert(solver,data, verbose)
            full_swap_tail(solver, data, verbose = True)

        if verbose: print("nombres de routes:", len(solver.routes))
        solver.show(2)

        if affichage: plt.show()

    else:
        print("Cout: ", solver.cout_solution())
        if affichage: plt.show()
    
    return (solver.cout_solution(), solver.routes)

if __name__ == "__main__":
    data = pickle.load(open("data.p", "rb"))
    cout, routes = resolution(data, True, True, True)
    print(cout)