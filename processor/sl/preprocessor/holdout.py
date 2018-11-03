#!/usr/bin/env python3
import argparse
import json
import math
import os
import random
import shutil

from sklearn.model_selection import train_test_split

import tools
import tools.utils as utils

from .preprocessor import Preprocessor


class Holdout_Preprocessor(Preprocessor):
    """
        Proprocessing though Hold Out split
    """

    def __init__(self, argv=None):
        super().__init__(argv)
        self.test_size = (self.arg.holdout['test'] / 100)
        self.val_size = (self.arg.holdout['val'] / 100)

    def start(self):
        # data_dir = '{}/data'.format(self.arg.input_dir)
        input_dir = '{}/poses'.format(self.arg.work_dir)
        label_path = '{}/label.json'.format(input_dir)
        output_dir = '{}/holdout'.format(self.arg.work_dir)

        print("Source directory: {}".format(input_dir))
        print("Holdout of data to '{}'...".format(output_dir))

        # load labels for split:
        with open(label_path, 'r') as fp:
            labels = json.load(fp)
        X = [k for k in labels]
        y = [v['label'] for (k, v) in labels.items()]

        if not labels:
            print("No data to holdout")
        else:
            # Holdout (train, test, val):
            X_train, X_test, X_val, y_train, y_test, y_val = self.holdout_data(
                X, y, self.test_size, self.val_size)

            # Copy items:
            self.copy_items('train', X_train, y_train,
                            input_dir, output_dir, labels)
            self.copy_items('test', X_test, y_test, input_dir, output_dir, labels)
            self.copy_items('val', X_val, y_val, input_dir, output_dir, labels)
            print("Holdout complete.")

    def holdout_data(self, X, y, test_size, val_size):
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=1)
        X_train, X_val, y_train, y_val = train_test_split(
            X_train, y_train, test_size=val_size, random_state=1)
        return X_train, X_test, X_val, y_train, y_test, y_val

    def copy_items(self, part, items, labels, input_dir, output_dir, data):
        if items:
            print("Saving '{}' data...".format(part))
            items_dir = '{}/{}'.format(output_dir, part)
            labels_path = '{}/{}_label.json'.format(output_dir, part)
            part_files = [ '{}.json'.format(x) for x in items ]
            part_labels = { x: data[x] for x in data if x in items }
            self.copy_files(part_files, input_dir, items_dir)
            self.save_json(part_labels, labels_path)

    def copy_files(self, items, src_dir, dest_dir):
        self.ensure_dir_exists(dest_dir)

        for item in items:
            print('* {}'.format(item))
            src = '{}/{}'.format(src_dir, item)
            dest = '{}/{}'.format(dest_dir, item)
            shutil.copy(src, dest)
