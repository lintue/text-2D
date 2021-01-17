"""Preprocess dataset for visualisation.

Extract text from CSV,
tokenise by n-grams,
compute TF*IDF,
output cosine similarity matrix,
encode to JSON.

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
    # Return lists with dims [n,] where n is total number of samples.
    # OPTIONAL: include metadata, in which case read relevant comments below.
    with open(args.data, "r") as csv_file:
        reader = csv.reader(csv_file, delimiter=";")
        next(reader, None)  # Skip header.
        # Data -- default to first column if no index given.
        data_col = (args.index[0] - 1) if args.index else 0
        # Labels -- default to second column if no index given.
        labels_col = (args.index[1] - 1) if args.index else 1
        # Loop through data and append to lists.
        data = []
        labels = []
        # OPTIONAL: if including metadata, add empty lists for each, as above.
        for rows in reader:
            data.append(rows[data_col])
            labels.append(rows[labels_col])
            # OPTIONAL: if including metadata, add append functions, as above.
        print("\n" + "Successfully read", len(data), "items." + "\n")
        # Remove duplicates if parameter -c included.
        if args.clean is True:
            counter = 0
            unique = []
            u_labels = []
            # OPTIONAL: if including metadata, add empty lists, as above.
            for i in data:
                if i not in unique:
                    unique.append(i)
                    u_labels.append(labels[counter])
                    # OPTIONAL: if including metadata, add append functions.
                counter += 1
            print("Removed", (len(data) - len(unique)), "duplicate entries." + "\n")
            data = unique
            labels = u_labels
            # OPTIONAL: if including metadata, replace variables, as above.

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
    # Dot product of TF*IDF vectors -> cosine similarity matrix.
    print("Computing cosine similarity matrix." + "\n")
    D = np.dot(X, X.T).todense()
    # Serialisation: output JSON.
    # OPTIONAL: if including metadata, add keys to dictionary below.
    map = {"similarity": D, "labels": labels}
    with open("similarity.json", "w") as json_file:
        json.dump(map, json_file, cls=JSON, indent=4)
        json_file.close()
    print("Encoded to JSON." + "\n")


if __name__ == "__main__":
    # Initialise with path to data.
    if args.data:
        main()
    else:
        sys.exit("\n" + "ERROR: Input data! \
                 Run tf-idf.py --help for details." + "\n")
