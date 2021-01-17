"""t-SNE visualisation.

Extract data from JSON,
(run PCA if high-dimensional),
run t-SNE,
output coordinate matrix,
plot in 2D,
save to CSV.

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
parser.add_argument("-t", "--test",
                    action="store_true",
                    help="Test mode (nonrandom initialisation), \
                          i.e., reproducible results.")
parser.add_argument("-s", "--save",
                    action="store_true",
                    help="Save data to CSV.")
args = parser.parse_args()


def main():
    # Read data from JSON.
    # Return NumPy array.
    with open(args.data, "r") as json_file:
        data = json.load(json_file)
        # Similarity values.
        X = np.asarray(data["similarity"])
        # Labels.
        Y = np.asarray(data["labels"])

        # OPTIONAL: include metadata and/or enumerate labels...
        # ... but modify CSV writer (lines 89-94) accordingly.
        # Examples below.
        # Metadata (include extra columns, titles and Z in CSV writer.)
        # e.g. Z = np.asarray([data["titles"], data["authors"], data["years"]])
        # Map labels to numerical IDs.
        label_ids = {"My label 1": "1",
                     "My label 2": "2",
                     "My label 3": "3",
                     "My label 4": "4",
                     "My label 5": "5",
                     "My label 6": "6"}
        # Iterate through labels and replace with IDs.
        # TO DO: find a simpler way to do this...
        # ... and find unique labels automatically?
        for i in range(len(Y)):
            for key, value in label_ids.items():
                Y[i] = Y[i].replace(key, value)

    # Determine initialisation (random vs deterministic).
    init = 1 if args.test is True else None

    # If feature dimensions > 50, use PCA before t-SNE.
    print("\n" + "Number of feature dimensions:", len(X[0]), "\n")
    if len(X[0]) > 50:
        print("Running PCA. Including 50 first principal components." + "\n")
        X = PCA(n_components=50,
                random_state=init
                ).fit_transform(X)

    # Run t-SNE.
    print("Initiating t-SNE..." + "\n")
    X_embedded = TSNE(n_components=2,
                      perplexity=50,
                      early_exaggeration=12,
                      learning_rate=75,  # try n/e_e
                      n_iter=1000,
                      random_state=init
                      ).fit_transform(X)

    # Output data to CSV.
    with open('t-sne.csv', 'w') as csv_file:
        # OPTIONAL: if including metadata, add columns ,{} and headers below.
        csv_file.write("{},{},{}\n".format("x", "y", "labels"))
        # OPTIONAL: if including metadata, add Z[0], Z[1], ..., Z[n] in zip().
        for i in zip(X_embedded.T[0], X_embedded.T[1], Y):
            # OPTIONAL: if including metadata, add i[3], i[4], ..., i[n].
            csv_file.write("{},{},{}\n".format(i[0], i[1], i[2]))
    print("Coordinates saved as CSV." + "\n")

    # Plot in 2D.
    x = X_embedded[:, 0]
    y = X_embedded[:, 1]
    colours = [(0, 0, 0)]
    area = np.pi * 3
    plt.scatter(x, y, s=area, c=colours, alpha=0.5)
    plt.title('t-SNE visualisation')
    plt.xlabel('x')
    plt.ylabel('y')
    args.save and plt.savefig("t-sne.png")
    plt.show()


if __name__ == "__main__":
    # Initialise with path to data.
    if args.data:
        main()
    else:
        sys.exit("\n" + "ERROR: Input data! \
                 Run t-sne.py --help for details." + "\n")
