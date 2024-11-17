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

## Simulates data with both continuous and discrete columns.
D, G = sim.simulateLeeHastie(num_meas=100, samp_size=1000)

D = tr.tetrad_data_to_pandas(D)
G = tr.graph_to_matrix(G)

# Save data to a file
D.to_csv('../mydata.csv', index=False)
G.to_csv('../mygraph.csv', index=False)
