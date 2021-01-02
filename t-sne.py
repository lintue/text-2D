"""t-SNE visualisation.

Extract distances and labels from JSON,
run t-SNE (PCA first if high-dimensional),
output coordinate matrix,
plot in 2D,
encode data to JSON.

pixel-tree, 2020."""

import argparse
import json
import sys

import matplotlib.pyplot as plt
import numpy as np

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# Parameters.
# --data required, read below; documentation for more details.
parser = argparse.ArgumentParser(description=None)
parser.add_argument("-d", "--data",
                    type=str,
                    help="Enter JSON filepath relative to current directory, \
                          e.g., ./data/cats.json")
# TO DO: implement save...
parser.add_argument("-s", "--save",
                    action="store_true",
                    help="Include flag to save data.")
args = parser.parse_args()


def main():
    # Read data from JSON.
    # Return NumPy array.
    with open(args.data, "r") as json_file:
        data = json.load(json_file)
        # Distances.
        X = np.asarray(data["distances"])
        # Labels.
        Y = np.asarray(data["labels"])

        # TO DO: find unique labels,
        # enumerate for ID,
        # create map sample id: label(s),
        # include metadata, etc.
        #
        # # Find unique labels, enumerate for ID and map.
        # unique = []
        # labels = {"id": [], "label": [], "key": []}
        # for i in enumerate(Y):
        #     labels["id"].append(i[0])
        #     if i[1] not in unique:
        #         if "; " in i[1]:
        #             print(i[1].split("; "))
        #         labels.append(i[1])

    # If feature dimensions > 50, use PCA before t-SNE.
    # TO DO: make arg for PCA feature number.
    print("\n" + "Number of feature dimensions:", len(X[0]), "\n")
    if len(X[0]) > 50:
        print("Initiating PCA. Reducing dimensionality of features..." + "")
        X = PCA(n_components=50).fit_transform(X)

    # Run t-SNE.
    X_embedded = TSNE(n_components=2,
                      perplexity=50,
                      early_exaggeration=12,
                      learning_rate=75,  # try n/e_e
                      n_iter=1000,
                      random_state=None  # None unless running tests
                      ).fit_transform(X)

    x = X_embedded[:, 0]
    y = X_embedded[:, 1]
    colours = [(0, 0, 0)]
    area = np.pi * 3

    plt.scatter(x, y, s=area, c=colours, alpha=0.5)
    plt.title('t-SNE')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()
    # TO DO: save plot plt.savefig().
    # TO DO; encode data to JSON.


if __name__ == "__main__":
    # Initialise with path to data.
    if args.data:
        main()
    else:
        sys.exit("\n" + "ERROR: Input data! \
                 Run t-sne.py --help for details." + "\n")
