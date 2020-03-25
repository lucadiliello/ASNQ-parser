"""
Given the ASNQ dataset, prepare it on your needs to allow the usage on different NLP systems
"""

import os
import argparse
import csv
import random
import shutil
from detect_delimiter import detect

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split Quora-Question-Pairs dataset in clusters')
    parser.add_argument("-i", "--input_file", required=True, type=str,
                        help="Quora dataset (in CSV format)")
    parser.add_argument("-d", "--delimiter", required=False, type=str, default=None,
                        help="Quora dataset (in CSV format)")
    parser.add_argument("-o", "--output_folder", required=True, type=str,
                        help="Output folder in which results will be saved (in CSV)")
   
    parser.add_argument("-f", "--force_overwrite", action="store_true",
                        help="Output files are overwritten if they already exists")

    parser.add_argument("-s", "--splits", required=False, nargs='+', type=int, default=[100],
                        help="List of splits in which the clusters should be divided in a balanced way"
                        "E.g. 10 10 40 40")
    parser.add_argument("--shuffle", required=False, default=False,
                        help="Whether dataset should be shuffled before being splitted")
    parser.add_argument("--seed", required=False, default=999, type=int,
                    help="seed for shuffling")

    parser.add_argument("--as-true", required=False, nargs='+', type=int, default=[4],
                        help="List of labels that must be considered as true (1)")

    args = parser.parse_args()

    # I/O
    input_file = args.input_file
    force = args.force_overwrite
    output_folder = args.output_folder
    delimiter = args.delimiter
    
    # Splits
    splits = args.splits
    shuffle = args.shuffle

    # Generation
    as_true = args.as_true
    
    # Mapping
    random.seed(args.seed)

    # Check over arguments
    assert sum([int(x) for x in splits]) == 100, "Splits MUST sum to 100"

    # Check file existence
    print("Checking file and directories")
    assert os.path.exists(input_file), "Input file {} does not exists".format(input_file)
    if os.path.exists(output_folder):
        assert force, "{} does already exists. Use -f option to overwrite it".format(output_folder)
        shutil.rmtree(output_folder)
    os.mkdir(output_folder)

    # Fix delimiter if not provided or file type has been given
    if delimiter == "csv":
        delimiter = ","
    elif delimiter == "tsv":
        delimiter = "\t"
    
    if delimiter is None:
        print("Inferring delimiter from input data")
        with open(input_file) as f:
            data = [f.readline() for i in range(50)]
            data = "\n".join([x for x in data if x])
            delimiter = detect(data)
            print(f"Delimiter is '{delimiter}'")

    # Import data
    print("Loading data from disk")
    input_data = None
    with open(input_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delimiter)
        next(csv_reader, None)
        input_data = list(csv_reader)

    print("Parsing and checking consistency")
    data = []
    for i, line in enumerate(input_data):
        assert len(line) == 3, f"Line {i} has a problem: {line}"
        label = int(int(line[2]) in as_true)
        data.append([str(line[0]), str(line[1]), label])

    if shuffle:
        print("Shuffling dataset")
        random.shuffle(data)
    else:
        print("Skipping shuffle")

    print(f"Dividing data in splits: {splits}")
    # Make splits cumulative [30, 30, 40] -> [0, 30, 60]
    cum_splits = [int(sum(splits[0: i])*len(data)/100) for i in range(len(splits))]

    data = [
        data[cum_splits[i]: (cum_splits[i+1] if (i+1) < len(cum_splits) else None)] for i in range(len(cum_splits))
    ]

    if delimiter == ",":
        extension = "csv"
    elif delimiter == "\t":
        extension = "tsv"
    else:
        extension = "txt"

    print("Writing splits to disk")
    for i, (s, data_split) in enumerate(zip(splits, data)):
        print(f"Writing split {i}-{s} with length {len(data_split)}")
        # writing originale eng questions
        with open(os.path.join(output_folder, f"{i}-{s}-en.{extension}"), mode='w') as f:
            writer = csv.writer(f, delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            writer.writerows(data_split)

    print("Results written to {}, exiting!".format(output_folder))


    