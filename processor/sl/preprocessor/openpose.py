#!/usr/bin/env python3
import json
import os
import subprocess

from tools import utils

from .preprocessor import Preprocessor


class OpenPose_Preprocessor(Preprocessor):
    """
        Preprocessor form pose estimation with OpenPose
    """

    def __init__(self, argv=None):
        super().__init__(argv)
        self.openpose = '{}/examples/openpose/openpose.bin'.format(
            self.arg.openpose)

        if not os.path.isfile(self.openpose):
            raise ValueError('Path to OpenPose is not valid.')

    def start(self):
        output_dir = '{}/poses'.format(self.arg.work_dir)
        label_map_path = '{}/label.json'.format(output_dir)
        snippets_dir = '{}/snippets'.format(output_dir)
        input_dir = '{}/splits'.format(self.arg.work_dir)
        self.ensure_dir_exists(output_dir)

        file_label, label_name = self.load_label_info(input_dir)

        if not file_label:
            print("Nothing to esimate.")
        else:
            # video processing:
            print("Source directory: '{}'".format(input_dir))
            print("Estimating poses to '{}'...".format(output_dir))
            label_map = self.process_videos(input_dir, snippets_dir, output_dir,
                                            file_label, label_name)

            # save label map
            self.save_json(label_map, label_map_path)
            print("Estimation complete.")

    def process_videos(self, input_dir, snippets_dir, output_dir,
                       file_label, label_name):
        # label info:
        label_map = dict()

        idx = 0
        total = len(file_label)

        for video, label in file_label.items():
            video_path = '{}/{}'.format(input_dir, video)

            if self.arg.debug and idx >= 5:
                break

            if os.path.isfile(video_path):
                label_idx = label_name.index(label)
                idx += 1
                self.print_progress(idx, total, video)

                try:
                    # pose estimation
                    self.ensure_dir_exists(snippets_dir)
                    self.run_openpose(video_path, snippets_dir)

                    # pack openpose ouputs
                    video_base_name = os.path.splitext(video)[0]
                    video_info = self.pack_outputs(
                        video_base_name, video_path, snippets_dir, output_dir, label, label_idx)

                    # label details for current video
                    cur_video = dict()
                    cur_video['has_skeleton'] = len(video_info['data']) > 0
                    cur_video['label'] = video_info['label']
                    cur_video['label_index'] = video_info['label_index']
                    label_map[video_base_name] = cur_video

                except subprocess.CalledProcessError as e:
                    print(" FAILED ({} {})".format(e.returncode, e.output))

                finally:
                    self.remove_dir(snippets_dir)

        return label_map

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

    def pack_outputs(self, video_base_name, video_path, snippets_dir, output_dir, label, label_idx):
        output_sequence_path = '{}/{}.json'.format(
            output_dir, video_base_name)
        frames = utils.video.get_video_frames(video_path)
        height, width, _ = frames[0].shape
        video_info = utils.openpose.json_pack(
            snippets_dir, video_base_name, width, height, label, label_idx)
        self.save_json(video_info, output_sequence_path)
        return video_info

    def run_openpose(self, video_path, snippets_dir):
        command = self.openpose
        args = {
            '--video': video_path,
            '--write_json': snippets_dir,
            '--display': 0,
            '--render_pose': 0,
            '--model_pose': 'COCO'
        }

        if not self.arg.debug:
            args['--hand'] = ''
            args['--face'] = ''

        command_line = self.create_command_line(command, args)
        FNULL = open(os.devnull, 'w')
        subprocess.check_call(command_line, shell=True,
                              stdout=FNULL, stderr=subprocess.STDOUT)

    def print_progress(self, current, total, video):
        print("* [{} / {}] \t Estimating '{}'...".format(current, total, video))
