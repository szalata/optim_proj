import argparse
import os

import numpy as np

import pickle

from pathlib import Path
from sklearn.model_selection import train_test_split

if __name__ == '__main__':
    """
    A every next number in a sequence is an increment of the previous one
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--seq_len', type=int, default=10, help='length of the sequence/sample')
    parser.add_argument('--samples', type=int, default=5000, help='the number of samples to return')
    parser.add_argument('--increment', type=int, default=1000,
                        help='the difference between consecutive numbers')
    parser.add_argument('--max_starting_point', type=int, default=1000)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--test_fraction', type=float, default=0.1)
    parser.add_argument('--output_dir', type=str, help='name of the file to write', default="data/sequence_learning")
    parser.add_argument('--variable_length', action='store_true', help='if set, the sequences will have different length')
    parser.add_argument('--max_len', type=int, default=10, help='maximum length for variable length sequences')

    args = parser.parse_args()
    np.random.seed(args.seed)


    if args.variable_length:
        out_array = [] 
        targets_array = [] 
        for i in range(args.samples):
            
            out_array.append(np.random.uniform(
                -args.max_starting_point, high=args.max_starting_point, size=(1)))
            for j in range(1, args.seq_len - i % args.seq_len):
                out_array[i] = np.append(out_array[i],out_array[i][j-1]+ args.increment) 
            
            targets_array.append(out_array[i][-1] + args.increment)
    else:
        out_array = np.zeros((args.samples, args.seq_len))
        out_array[:, 0] = np.random.uniform(
            -args.max_starting_point, high=args.max_starting_point, size=args.samples)
        for i in range(1, args.seq_len):
            out_array[:, i] = out_array[:, i - 1] + args.increment
        targets_array = out_array[:, -1] + args.increment
        

    # create data splits
    X_train, X_test, y_train, y_test = train_test_split(out_array, targets_array,
                                                        test_size=args.test_fraction,
                                                        random_state=args.seed)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train,
                                                      test_size=args.test_fraction,
                                                      random_state=args.seed)
    # create directory if doesn't exist
    if args.variable_length:
        Path(args.output_dir+"/varied_length").mkdir(parents=True, exist_ok=True)
    else:
        Path(args.output_dir+"/fixed_length").mkdir(parents=True, exist_ok=True)

    split_data_mapping = {"train": (X_train, y_train),
                          "val": (X_val, y_val),
                          "test": (X_test, y_test)}
    
    for split in ["train", "val", "test"]:
        X, y = split_data_mapping[split]

        if args.variable_length:
            Xpath = os.path.join(args.output_dir+"/varied_length", f"X_{split}")
            ypath = os.path.join(args.output_dir+"/varied_length", f"y_{split}")
            
        else:
            Xpath = os.path.join(args.output_dir+"/fixed_length", f"X_{split}")
            ypath = os.path.join(args.output_dir+"/fixed_length", f"y_{split}")

        # if file already exists remove it
        if os.path.isfile(Xpath):
            os.remove(Xpath)

        Xfile = open(Xpath, 'ab')
        pickle.dump(X, Xfile)
        Xfile.close()
        
        # if file already exists remove it
        if os.path.isfile(ypath):
            os.remove(ypath)

        yfile = open(ypath, 'ab')
        pickle.dump(y, yfile)
        yfile.close()
  
