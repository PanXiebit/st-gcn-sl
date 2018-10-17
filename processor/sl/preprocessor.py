import argparse

from processor.io import IO
from processor.sl.openpose import OpenPose_Preprocessor


class Data_Preprocessor:
    def __init__(self, argv=None):
        self.load_arg(argv)

    def load_arg(self, argv=None):
        parser = self.get_parser()
        self.arg = parser.parse_args(argv)

    def start(self):
        # 1. split videos
        # 2. estimate pose (openpose)
        # 3. pad frames
        # 4. holdout
        # 5. process data (python) (generate pkl)

        OpenPose_Preprocessor().start()

        pass

    @staticmethod
    def get_parser(add_help=False):
        # parameter priority: command line > config > default
        parent_parser = IO.get_parser(add_help=False)
        parser = argparse.ArgumentParser(
            add_help=add_help,
            parents=[parent_parser],
            description='Data preprocessor')

        # region arguments yapf: disable
        parser.add_argument('--input_dir', help='Path to video input')
        parser.add_argument('--output_dir', help='Path to save results')
        parser.add_argument('--debug', help='Debug', default=False)

        parser.add_argument('--openpose', default='3dparty/openpose/build', help='Path to openpose')
        parser.set_defaults(print_log=False)
        # endregion yapf: enable

        return parser
