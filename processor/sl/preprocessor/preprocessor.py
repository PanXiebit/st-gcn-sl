import os
import shutil
import json

import pandas
import xlrd
import re
import string
import torchlight
from .io import IO


class Preprocessor(IO):
    """
        Base Processor
    """

    METADATA_COLUMNS = ['Main New Gloss.1',
                        'Consultant', 'Session', 'Scene', 'Start', 'End']
    METADATA_IGNORED_VALUES = ['============', '------------']

    def __init__(self, argv=None):
        super().__init__(argv)
        self.file_pattern = self.arg.download['file_pattern']

    def start(self):
        pass

    def progress_bar(self, current, total):
        increments = 50
        percentual = ((current / total) * 100)
        i = int(percentual // (100 / increments))
        text = "\r|{0: <{1}}| {2:.0f}%".format('█' * i, increments, percentual)
        print(text, end="\n" if percentual >= 100 else "")

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
