#!/usr/bin/env python3
import math
import os
import shutil
import subprocess
import tempfile
# from urllib import request

from .preprocessor import Preprocessor


class Downloader_Preprocessor(Preprocessor):
    """
        Preprocessor for splitting original videos
    """

    def __init__(self, argv=None):
        super().__init__(argv)
        self.url = self.arg.download['url']

    def start(self):
        self.start_download()

    def start_download(self):
        # Example: http://csr.bu.edu/ftp/asl/asllvd/asl-data2/quicktime/<session>/scene<scene#>-camera<camera#>.mov
        output_dir = '{}'.format(self.arg.input_dir)
        self.ensure_dir_exists(output_dir)

        nrows = None

        if self.arg.debug:
            nrows = 2

        # Load metadata:
        self.print_log("Loading metadata...")
        metadata = self.load_metadata(['Session', 'Scene'], nrows)

        if metadata.empty:
            self.print_log("Nothing to download.")
        else:
            # Download files:
            self.print_log("Source URL: '{}'".format(self.url))
            self.print_log("Downloading files to '{}'...".format(output_dir))
            self.ensure_dir_exists(output_dir)
            self.download_files_in_metadata(metadata, self.url, output_dir)
            self.print_log("Download complete.")

    def download_files_in_metadata(self, metadata, url, output_dir):
        for row in metadata.itertuples():
            src_filename = self.format_filename(row.Session, row.Scene)
            tgt_filename = src_filename.replace('/', '_')
            tgt_file = '{}/{}'.format(output_dir, tgt_filename)

            if not os.path.isfile(tgt_file):
                src_url = '{}/{}'.format(url, src_filename)
                tmp_file = '{}/{}'.format(tempfile.gettempdir(),
                                          tgt_filename)
                try:
                    # Download file:
                    self.print_log("Downloading '{}'...".format(src_url))
                    self.run_wget(src_url, tmp_file)

                    # Save file to directory:
                    shutil.move(tmp_file, tgt_file)

                except subprocess.CalledProcessError as e:
                    self.print_log(" FAILED ({} {})".format(e.returncode, e.output))

    def run_wget(self, url, file):
        command = 'wget {}'.format(url)
        args = {
            '-O': file,
            '-q': '',
            '--show-progress': ''
        }
        command_line = self.create_command_line(command, args)
        subprocess.check_call(command_line, shell=True,
                              stderr=subprocess.STDOUT)
