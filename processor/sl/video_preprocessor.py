import argparse
import os
import shutil

from processor.io import IO
from torchlight import str2bool

from .preprocessor.downloader import Downloader_Preprocessor
from .preprocessor.openpose import OpenPose_Preprocessor
from .preprocessor.splitter import Splitter_Preprocessor
from .preprocessor.holdout import Holdout_Preprocessor
from .preprocessor.gendata import Gendata_Preprocessor

class Video_Preprocessor:
    def __init__(self, argv=None):
        self.load_arg(argv)

    def load_arg(self, argv=None):
        parser = self.get_parser()
        self.arg = parser.parse_args(argv)

    def start(self):
        workdir = self.arg.work_dir
        # self.create_dir(workdir)

        # 0. download videos
        # 1. split videos
        # 2. estimate pose (openpose)
        # 3. pad frames
        # 4. holdout
        # 5. process data (python) (generate pkl)
        pipeline = [
            Downloader_Preprocessor,
            Splitter_Preprocessor,
            OpenPose_Preprocessor,
            Holdout_Preprocessor,
            Gendata_Preprocessor
        ]

        for _, phase in enumerate(pipeline):
            phase(self.arg).start()

        # self.remove_dir(workdir)

    def create_dir(self, dir):
        self.remove_dir(dir)
        os.makedirs(dir)

    def remove_dir(self, dir):
        if os.path.exists(dir):
            shutil.rmtree(dir, ignore_errors=True)

    @staticmethod
    def get_parser(add_help=False):
        # parameter priority: command line > config > default
        parser = argparse.ArgumentParser(
            add_help=add_help,
            description='Data preprocessor')

        # region arguments yapf: disable
        parser.add_argument('--input_dir', help='Path to video input')
        parser.add_argument('--output_dir', help='Path to save results')
        parser.add_argument('--work_dir', help='Path to save partial outputs')
        parser.add_argument('--debug',  type=str2bool, default=False, help='Debug')
        parser.add_argument('--metadata_path', help='Path to metadata file')
        
        parser.add_argument('--download_videos', type=str2bool, default=False, help='Download video files?')

        parser.add_argument('--holdout_test', default=20, help='Percentage for test')
        parser.add_argument('--holdout_val', default=20, help='Percentage for validation')

        parser.add_argument('--openpose', help='Path to openpose')
        parser.set_defaults(print_log=False)
        # endregion yapf: enable

        return parser
