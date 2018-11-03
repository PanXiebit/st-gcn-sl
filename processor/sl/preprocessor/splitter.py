#!/usr/bin/env python3
import os
import shutil

import ffmpy

from processor.io import IO

from .preprocessor import Preprocessor


class Splitter_Preprocessor(Preprocessor):
    """
        Preprocessor for splitting original videos
    """

    INPUT_FPS = 60
    OUTPUT_FPS = 30

    def start(self):
        input_dir = self.arg.input_dir
        output_dir = '{}/splits'.format(self.arg.work_dir)
        self.ensure_dir_exists(output_dir)

        # Load metadata:
        print("Loading metadata...")
        metadata = self.load_metadata(
            ['Main New Gloss.1', 'Session', 'Scene', 'Start', 'End'])

        # Split videos:
        print("Source directory: '{}'".format(input_dir))
        print("Splitting videos to '{}'...".format(output_dir))
        labels, files_labels = self.split_videos(
            metadata, input_dir, output_dir)

        # Save labels:
        print("Saving labels...")
        self.save_labels(output_dir, labels, files_labels)

        print("Split finished.")

    def split_videos(self, metadata, input_dir, output_dir):
        labels = set()
        files_labels = dict()

        for row in metadata.itertuples():
            filename = self.format_filename(row.Session, row.Scene)
            input_file = '{}/{}'.format(input_dir, filename)

            if os.path.isfile(input_file):
                sign = self.normalize(str(row.Main_New_Gloss_1)).lower()
                start = row.Start
                end = row.End

                # Store label:
                if sign not in labels:
                    labels.add(sign)

                # Process files:
                print("* {} \t {} ({} ~ {})".format(sign, filename, start, end))
                filename, _ = self.split_video(input_file, output_dir,
                                               sign, start, end,
                                               self.INPUT_FPS, self.OUTPUT_FPS)
                # File x label mapping:
                files_labels[filename] = sign

        return labels, files_labels

    def split_video(self, src_filename, output_dir,
                    sign, start, end,
                    input_fps, output_fps):
        # Create video name:
        filename, tgt_filepath = self.create_filename(sign, output_dir)
        start_sec = self.frame_to_sec(start, input_fps)
        length_sec = self.frame_to_sec(end - start, input_fps)
        self.run_ffmpeg(src_filename, tgt_filepath,
                        start_sec, length_sec, output_fps)
        return filename, tgt_filepath

    def run_ffmpeg(self, src, tgt, start, length, fps):
        if not os.path.isfile(src):
            print('Video not found: %s' % src)

        else:
            ff = ffmpy.FFmpeg(
                inputs={src: None},
                outputs={tgt: ['-ss', start,
                               '-t', length,
                               '-r', str(fps),
                               '-y',
                               '-loglevel', 'error'
                               ]}
            )
            ff.run()

    def save_labels(self, output_dir, labels, files_labels):
        labels_file = "{}/label_name.txt".format(output_dir)
        self.save_items(sorted(labels), labels_file)

        files_labels_file = "{}/file_label.txt".format(output_dir)
        self.save_map(files_labels, files_labels_file)

    def create_filename(self, sign, output_dir):
        idx = 0
        filename = None
        filepath = None

        while (not filepath) or os.path.isfile(filepath):
            idx += 1
            filename = "{!s}-{:03d}.mov".format(sign, idx)
            filepath = '{}/{}'.format(output_dir, filename)

        return filename, filepath

    def frame_to_sec(self, frame, fps):
        res = frame / fps
        secs, milis = divmod(res * 1000, 1000)
        mins, secs = divmod(secs, 60)
        hours, mins = divmod(mins, 60)
        return '%02d:%02d:%02d.%03d' % (hours, mins, secs, milis)
