#!/usr/bin/env python3
import os
import argparse
import json
import shutil
import glob

import numpy as np
import torch
import skvideo.io

from .io import IO
import tools
import tools.utils as utils


class OpenPose_Preprocessor:
    """
        Proprocessing using OpenPose
    """

    def __init__(self, argv=None):
        self.load_arg(argv)

    def load_arg(self, argv=None):
        parser = self.get_parser()
        self.arg = parser.parse_args(argv)

    def start(self):
        output_snippets_dir = '{}/temp/snippets'.format(self.arg.output_dir)
        output_sequence_dir = self.arg.output_dir
        input_dir = self.arg.input_dir

        # create or clear output directory:
        if os.path.exists(output_sequence_dir):
            shutil.rmtree(output_snippets_dir, ignore_errors=True)
        else:
            os.makedirs(output_sequence_dir)

        # video processing:
        self.process_videos(input_dir, output_snippets_dir,
                            output_sequence_dir)

        # remove temp directory content on exit:
        shutil.rmtree(output_snippets_dir, ignore_errors=True)

    def process_videos(self, input_dir, output_snippets_dir, output_sequence_dir):
        videos = glob.glob('{}/*.mov'.format(input_dir))
        videos = [os.path.basename(x) for x in videos]

        # label info:
        file_label, label_name = self.load_label_info(input_dir)

        if self.arg.debug:
            videos = videos[0:3]

        for idx, video in enumerate(videos):
            self.print_progress(idx, videos, video)
            video_path = '{}/{}'.format(input_dir, video)
            video_label = file_label[video]
            video_label_idx = label_name.index(video_label)

            # pose estimation
            self.run_openpose(video_path, output_snippets_dir)

            # pack openpose ouputs
            video_info = self.pack_outputs(
                video, video_path, output_snippets_dir, output_sequence_dir, video_label, video_label_idx)
            print('OK' if video_info['data'] else 'NOK')

    def load_label_info(self, input_dir):
        label_name_path = '{}/label_name.txt'.format(input_dir)
        file_label_path = '{}/file_label.txt'.format(input_dir)

        with open(label_name_path) as f:
            label_name = f.readlines()
            label_name = [line.rstrip() for line in label_name]

        with open(file_label_path) as f:
            file_label = f.readlines()
            file_label = [line.rstrip() for line in file_label]
            file_label = dict(map(lambda x: x.split(':'), file_label))
        return file_label, label_name

    def pack_outputs(self, video, video_path, output_snippets_dir, output_sequence_dir, label, label_idx):
        video_base_name = os.path.splitext(video)[0]
        output_sequence_path = '{}/{}.json'.format(
            output_sequence_dir, video_base_name)
        frames = utils.video.get_video_frames(video_path)
        height, width, _ = frames[0].shape
        video_info = utils.openpose.json_pack(
            output_snippets_dir, video_base_name, width, height, label, label_idx)
        with open(output_sequence_path, 'w') as outfile:
            json.dump(video_info, outfile)
        return video_info

    def run_openpose(self, video_path, snippets_dir):
        openpose = '{}/examples/openpose/openpose.bin'.format(
            self.arg.openpose)
        openpose_args = dict(
            video=video_path,
            write_json=snippets_dir,
            display=0,
            render_pose=0,
            model_pose='COCO',)

        if not self.arg.debug:
            openpose_args['hand'] = ''
            openpose_args['face'] = ''

        command_line = openpose + ' '
        command_line += ' '.join(['--{} {}'.format(k, v)
                                  for k, v in openpose_args.items()])
        shutil.rmtree(snippets_dir, ignore_errors=True)
        os.makedirs(snippets_dir)
        os.system(command_line)

    def print_progress(self, idx, videos, video):
        print('-' * 50)
        print('[{} / {}] Processing \'{}\'...'.format((idx + 1), len(videos), video))
        print('-' * 50)

    @staticmethod
    def get_parser(add_help=False):
        # parameter priority: command line > config > default
        parent_parser = IO.get_parser(add_help=False)
        parser = argparse.ArgumentParser(
            add_help=add_help,
            parents=[parent_parser],
            description='Preprocessing using OpenPose')

        # region arguments yapf: disable
        parser.add_argument('--input_dir',
                            help='Path to video input')
        parser.add_argument('--openpose',
                            default='3dparty/openpose/build',
                            help='Path to openpose')
        parser.add_argument('--output_dir',
                            help='Path to save results')
        parser.add_argument('--debug',
                            help='Debug', default=False)
        parser.set_defaults(print_log=False)
        # endregion yapf: enable

        return parser
