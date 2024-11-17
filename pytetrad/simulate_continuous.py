import jpype
import jpype.imports

import os
jar_path = os.path.abspath("resources/tetrad-current.jar")
if not jpype.isJVMStarted():
    try:
        jpype.startJVM(jpype.getDefaultJVMPath(), "-Xmx2g", classpath=[jar_path])
    except OSError:
        print("can't load jvm")
        pass

import pytetrad.tools.translate as tr
import pytetrad.tools.simulate as sim

D, G = sim.simulateContinuous(num_meas=100, samp_size=1000)

D2 = tr.tetrad_data_to_pandas(D)
G2 = tr.graph_to_matrix(G)

# Save data to a file
D2.to_csv('../mydata.csv', index=False)
G2.to_csv('../mygraph.csv', index=False)
