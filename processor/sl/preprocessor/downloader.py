#!/usr/bin/env python3
import math
import os
import shutil
from urllib import request

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
        print("Loading metadata...")
        metadata = self.load_metadata(['Session', 'Scene'], nrows)

        if metadata.empty:
            print("Nothing to download.")
        else:
            # Download files:
            print("Source URL: '{}'".format(self.url))
            print("Downloading files to '{}'...".format(output_dir))
            self.ensure_dir_exists(output_dir)
            self.download_files_in_metadata(metadata, self.url, output_dir)
            print("Download complete.")

    def download_files_in_metadata(self, metadata, url, output_dir):
        downloaded_sessions = set()

        for row in metadata.itertuples():
            src_filename = self.format_filename(row.Session, row.Scene)
            tgt_filename = src_filename.replace('/', '_')

            if tgt_filename not in downloaded_sessions:
                src_url = '{}/{}'.format(url, src_filename)
                tgt_file = '{}/{}'.format(output_dir, tgt_filename)

                # Download file:
                print("Downloading '{}'...".format(src_url))
                testfile = request.URLopener()
                (tempfilename, _) = testfile.retrieve(
                    url, None, self.reporthook)

                # Save file to directory:
                shutil.move(tempfilename, tgt_file)
                downloaded_sessions.add(tgt_filename)

    def reporthook(self, blocknum, bs, size):
        self.progress_bar(blocknum, math.ceil(size / bs))
