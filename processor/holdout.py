#!/usr/bin/env python3
import argparse
import json
import math
import os
import random
import shutil

import tools
import tools.utils as utils

from .io import IO


class HoldOut_Preprocessor:
    """
        Proprocessing though Hold Out split
    """

    def __init__(self, argv=None):
        self.load_arg(argv)

    def load_arg(self, argv=None):
        parser = self.get_parser()
        self.arg = parser.parse_args(argv)

    def start(self):
        split = dict()
        split['val'] = float(self.arg.val)
        split['test'] = float(self.arg.test)
        split['train'] = float(self.arg.train)

        data_dir = '{}/data'.format(self.arg.input_dir)
        label_path = '{}/label.json'.format(self.arg.input_dir)
        output_dir = '{}'.format(self.arg.output_dir)

        items = os.listdir(data_dir)
        random.shuffle(items)
        num_items = len(items)

        # load labels for split:
        with open(label_path, 'r') as fp:
            labels = json.load(fp)

        start_idx = 0

        if os.path.exists(self.arg.output_dir):
            shutil.rmtree(output_dir, ignore_errors=True)
        os.makedirs(output_dir)

        for part, val in split.items():
            end_idx = math.ceil(start_idx + (val * num_items / 100))

            if end_idx > num_items:
                end_idx = num_items

            split_items = items[start_idx:end_idx]
            split_labels = {x: labels[x]
                            for x in labels if '{}.json'.format(x) in split_items}
            start_idx = end_idx

            if split_items:
                part_dest_dir = '{}/{}/data'.format(output_dir, part)
                part_label_path = '{}/{}/label.json'.format(output_dir, part)
                self.print_progress(part, val, split_items, part_dest_dir)
                self.copy_files(split_items, data_dir, part_dest_dir)
                self.save_label(part_label_path, split_labels)

    def save_label(self, path, items):
        with open(path, 'w') as outfile:
            json.dump(items, outfile)

    def print_progress(self, part, val, split_items, dest_dir):
        print('-' * 50)
        print('\'{}\' ({:0.0f}% / {} items)'.format(part.upper(),
                                                    val, len(split_items)))
        print('-' * 50)
        print('Copying items to \'{}\'...'.format(dest_dir))

    def copy_files(self, items, src_dir, dest_dir):
        os.makedirs(dest_dir)

        for item in items:
            print(' {}'.format(item))
            src = '{}/{}'.format(src_dir, item)
            dest = '{}/{}'.format(dest_dir, item)
            shutil.copy(src, dest)

    @staticmethod
    def get_parser(add_help=False):
        # parameter priority: command line > config > default
        parent_parser = IO.get_parser(add_help=False)
        parser = argparse.ArgumentParser(
            add_help=add_help,
            parents=[parent_parser],
            description='Preprocessing using Hold-Out split')

        # region arguments yapf: disable
        parser.add_argument('--input_dir', help='Path to input')
        parser.add_argument('--output_dir', help='Path to  output')
        parser.add_argument('--train', help='Percent for training')
        parser.add_argument('--test', help='Percent for training')
        parser.add_argument('--val', help='Percent for validation')
        parser.set_defaults(print_log=False)
        # endregion yapf: enable

        return parser
