import numpy as np
import matplotlib.pyplot as plt

custom_cmap = plt.get_cmap("tab20c")
custom_cmap = custom_cmap(np.arange(custom_cmap.N))
custom_cmap = np.vstack((custom_cmap, plt.get_cmap("tab20b")(np.arange(plt.get_cmap("tab20b").N))))
custom_cmap = plt.matplotlib.colors.ListedColormap(custom_cmap)
