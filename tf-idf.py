"""Process dataset for visualisation.

Extract text from CSV,
tokenise by n-grams,
compute TF*IDF,
output distance matrix.

pixel-tree, 2020."""

import argparse
import csv
import json
import sys

import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer

# Parameters.
# --data required, others optional, read below; documentation for more details.
parser = argparse.ArgumentParser(description=None)
parser.add_argument("-d", "--data",
                    type=str,
                    help="Enter CSV filepath relative to current directory, \
                          e.g., ./data/cats.csv")
parser.add_argument("-i", "--index",
                    type=int,
                    nargs=2,
                    help="Enter column indices A B: \
                          where text for processing under A; and \
                          corresponding labels (for visualisation) under B.")
parser.add_argument("-c", "--clean",
                    action="store_true",
                    help="Include flag to remove duplicate entries.")
args = parser.parse_args()


# Encoder: NumPy matrix to JSON.
class JSON(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.matrix):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def main():
    # Read data from CSV.
    # Return list with dims [n,] where n is total number of samples.
    with open(args.data, "r") as csv_file:
        reader = csv.reader(csv_file, delimiter=";")
        next(reader, None)  # Skip header.
        # Data -- default to first column if no index given.
        data_col = (args.index[0] - 1) if args.index else 0
        # Labels -- default to second column if no index given.
        labels_col = (args.index[1] - 1) if args.index else 5
        # Loop through data and append to lists.
        data = []
        labels = []
        for rows in reader:
            data.append(rows[data_col])
            labels.append(rows[labels_col])
        print("\n" + "Successfully read", len(data), "items." + "\n")
        # Remove duplicates if parameter -c included.
        if args.clean is True:
            counter = 0
            unique = []
            u_labels = []
            for i in data:
                if i not in unique:
                    unique.append(i)
                    u_labels.append(labels[counter])
                counter += 1
            print("Removed", (len(data) - len(unique)), "duplicate entries." + "\n")
            data = unique
            labels = u_labels

    # N-grams.
    # L2 normalised TF*IDF.
    vectoriser = TfidfVectorizer(min_df=2,
                                 stop_words="english",
                                 strip_accents="unicode",
                                 lowercase=True,
                                 ngram_range=(1, 2),
                                 norm="l2")
    X = vectoriser.fit_transform(data)
    print("TF*IDF matrix dims:", X.shape, "\n")
    # Dot product of TF*IDF vectors. Create distance matrix.
    D = np.dot(X, X.T).todense()
    # Serialisation: output JSON.
    map = {"distances": D, "labels": labels}
    with open("output.json", "w") as json_file:
        json.dump(map, json_file, cls=JSON, indent=4)
        json_file.close()
    print("Distance matrix saved as JSON." + "\n")


if __name__ == "__main__":
    # Initialise with path to data.
    if args.data:
        main()
    else:
        sys.exit("\n" + "ERROR: Input data!" + "\n")
