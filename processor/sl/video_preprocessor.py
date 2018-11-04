import argparse
import os
import shutil
import yaml

from processor.io import IO
from torchlight import str2bool
from torchlight import str2dict
from tools.utils.parser import str2list

from .preprocessor.downloader import Downloader_Preprocessor
from .preprocessor.openpose import OpenPose_Preprocessor
from .preprocessor.splitter import Splitter_Preprocessor
from .preprocessor.holdout import Holdout_Preprocessor
from .preprocessor.gendata import Gendata_Preprocessor

from .preprocessor.io import IO

class Video_Preprocessor(IO):

    def __init__(self, argv=None):
        self.load_arg(argv)
        super().__init__(self.arg)

    def load_arg(self, argv=None):
        parser = self.get_parser()

        # load arg form config file
        p = parser.parse_args(argv)

        if p.config:
            # load config file
            with open(p.config, 'r') as f:
                default_arg = yaml.load(f)

            # update parser from config file
            key = vars(p).keys()
            for k in default_arg.keys():
                if k not in key:
                    self.print_log('Unknown Arguments: {}'.format(k))
                    assert k in key

            parser.set_defaults(**default_arg)

        self.arg = parser.parse_args(argv)

    def start(self):
        workdir = self.arg.work_dir

        # Clean workdir:
        if self.arg.clean_workdir:
            self.remove_dir(workdir)
            self.create_dir(workdir)

        # 0. download videos
        # 1. split videos
        # 2. estimate pose (openpose)
        # 3. pad frames
        # 4. holdout
        # 5. process data (python) (generate pkl)
        pipeline = self.get_phases()

        # Select phases:
        if self.arg.phases:
            pipeline = {k: v
                        for (k, v) in pipeline.items()
                        if k in self.arg.phases}

        # Run pipeline:
        for name, phase in pipeline.items():
            self.print_phase(name)
            phase(self.arg).start()

        # Remove workdir:
        if self.arg.clean_workdir:
            self.remove_dir(workdir)

        self.print_log("\nDONE")

    def get_phases(self):
        phases = dict()
        phases['download'] = Downloader_Preprocessor
        phases['split'] = Splitter_Preprocessor
        phases['pose'] = OpenPose_Preprocessor
        phases['holdout'] = Holdout_Preprocessor
        phases['gendata'] = Gendata_Preprocessor
        return phases

    def print_phase(self, name):
        self.print_log("")
        self.print_log("-" * 80)
        self.print_log(name.upper())
        self.print_log("-" * 80)

    @staticmethod
    def get_parser(add_help=False):
        # parameter priority: command line > config > default
        parser = argparse.ArgumentParser(
            add_help=add_help,
            description='Data preprocessor')

        # region arguments yapf: disable
        parser.add_argument('-c', '--config',
                            help='configuration file')
        parser.add_argument('-i', '--input_dir',
                            help='input directory')
        parser.add_argument('-o', '--output_dir',
                            help='output directory')
        parser.add_argument('-w', '--work_dir',
                            help='working directory')
        parser.add_argument('-cw', '--clean_workdir',  type=str2bool, default=True,
                            help='clean working directory')
        parser.add_argument('-m', '--metadata_file',
                            help='metadata file')
        parser.add_argument('-op', '--openpose',
                            help='path to OpenPose')

        parser.add_argument('-d', '--debug',  type=str2bool, default=False,
                            help='debug flag')
        parser.add_argument('--save_log', type=str2bool, default=True,
                            help='save logging or not')
        parser.add_argument('--print_log', type=str2bool, default=True,
                            help='print logging or not')

        parser.add_argument('-ph', '--phases', type=str2list, default=[],
                            help='phases of pipeline')
        parser.add_argument('-ho', '--holdout', type=str2dict, default="{}",
                            help='holdout configuration')
        parser.add_argument('-sp', '--split', type=str2dict, default="{}",
                            help='split configuration')
        parser.add_argument('-dl', '--download', type=str2dict, default="{}",
                            help='download configuration')
        parser.add_argument('-gd', '--gendata', type=str2dict, default="{}",
                            help='data generation configuration')
        # endregion yapf: enable

        return parser
