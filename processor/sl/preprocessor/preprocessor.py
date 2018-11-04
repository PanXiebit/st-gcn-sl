import os
import shutil
import json

import pandas
import xlrd
import re
import string


class Preprocessor:
    """
        Base Processor
    """

    METADATA_COLUMNS = ['Main New Gloss.1',
                        'Consultant', 'Session', 'Scene', 'Start', 'End']
    METADATA_IGNORED_VALUES = ['============', '------------']

    def __init__(self, argv=None):
        self.arg = argv
        self.file_pattern = self.arg.download['file_pattern']

    def start(self):
        pass

    def progress_bar(self, current, total):
        increments = 50
        percentual = ((current / total) * 100)
        i = int(percentual // (100 / increments))
        text = "\r|{0: <{1}}| {2:.0f}%".format('█' * i, increments, percentual)
        print(text, end="\n" if percentual >= 100 else "")

    def ensure_dir_exists(self, dir):
        if not os.path.exists(dir):
            self.create_dir(dir)

    def create_dir(self, dir):
        os.makedirs(dir)

    def remove_dir(self, dir):
        if os.path.exists(dir):
            shutil.rmtree(dir, ignore_errors=True)

    def load_metadata(self, columns=None, nrows=None):
        if not columns:
            columns = self.METADATA_COLUMNS

        df = pandas.read_excel(self.arg.metadata_file,
                               na_values=self.METADATA_IGNORED_VALUES,
                               keep_default_na=False)
        df = df[columns]
        df = df.dropna(how='all')
        df = df.head(nrows)
        norm_columns = {x: self.normalize(x) for x in columns}
        df = df.rename(index=str, columns=norm_columns)
        return df

    def format_filename(self, session, scene):
        return self.file_pattern.format(session=session,
                                        scene=int(scene),
                                        camera=1)

    def normalize(self, text):
        special_chars = re.escape(string.punctuation + string.whitespace)
        return re.sub(r'['+special_chars+']', '_', text)

    def save_items(self, items, path):
        with open(path, 'w') as f:
            for item in items:
                f.write("{}{}".format(item, os.linesep))

    def save_map(self, map, path):
        with open(path, 'w') as f:
            for key, val in map.items():
                f.write("{}:{}{}".format(key, val, os.linesep))

    def save_json(self, data, path):
        with open(path, 'w') as f:
            json.dump(data, f)

    def create_command_line(self, command, args):
        command_line = command + ' '
        command_line += ' '.join(['{} {}'.format(k, v)
                                  for k, v in args.items()])
        return command_line
