import jpype.imports

try:
    # jpype.startJVM(classpath=[f"resources/tetrad-gui-7.2.2-launch.jar"])
    jpype.startJVM(classpath=[f"resources/tetrad-gui-bugfix-launch.jar"])
except OSError:
    print("JVM already started")

import pandas as pd
import tools.translate as tr

import edu.cmu.tetrad.search as ts

def print_graph(alg_name, G):
    print(f"\n{alg_name}\n")
    print(G)
    print(tr.tetrad_graph_to_pcalg(G))
    print(tr.tetrad_graph_to_causal_learn(G))


def run_searchs(df):

    data = tr.pandas_to_tetrad(df)
    print(data)

    score = ts.BDeuScore(data)
    score.setSamplePrior(10)
    score.setStructurePrior(1)

    test = ts.IndTestChiSquare(data, 0.1)

    fges = ts.Fges(score)
    fges_graph = fges.search()
    print_graph('fGES', fges_graph)

    boss = ts.Boss(test, score)
    boss.setUseDataOrder(False)
    boss.setNumStarts(1)
    boss.bestOrder(score.getVariables())
    boss_graph = boss.getGraph(True)
    print_graph('BOSS', boss_graph)

    print("\nGRaSP\n")
    grasp = ts.Grasp(test, score)
    grasp.setOrdered(False)
    grasp.setUseDataOrder(False)
    grasp.setNumStarts(5)
    grasp.bestOrder(score.getVariables())
    grasp_graph = grasp.getGraph(True)
    print_graph('GRaSP', grasp_graph)

    print("\nFCI\n")
    fci = ts.Fci(test)
    fci_graph = fci.search()
    print_graph('FCI', fci_graph)

    print("\nGFCI\n")
    gfci = ts.GFci(test, score)
    gfci_graph = gfci.search()
    print_graph('GFCI', gfci_graph)

    print("\nGRaSP-FCI\n")
    grasp_fci = ts.GraspFci(test, score)
    grasp_fci_graph = grasp_fci.search()
    print_graph('GRaSP-FCI', grasp_fci_graph)

df = pd.read_csv("resources/bridges.data.version211_rev.txt", sep="\t")
run_searchs(df)