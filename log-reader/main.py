import re
import csv
import argparse

REGEX_EPOCH = r'Training epoch: (\d+)'
REGEX_LOSS_LR = r'Iter (\d+) Done. \| loss: ([-+]?\d*\.\d+|\d+) \| lr: ([-+]?\d*\.\d+|\d+)'
REGEX_MEAN_LOSS = r'mean_loss: ([-+]?\d*\.\d+|\d+)'
REGEX_TOP_1 = r'Top1: ([-+]?\d*\.\d+|\d+)%'
REGEX_TOP_5 = r'Top5: ([-+]?\d*\.\d+|\d+)%'


def read(file, output):
    cur_epoch = None
    cur_loss = None
    cur_lr = None
    cur_mean_loss = None
    cur_top_1 = None
    cur_top_5 = None

    with open(file, 'r') as f:
        line = f.readline()
        items = list()

        while line:
            line = f.readline()
            txt = line[20:].strip()

            m_epoch = re.search(REGEX_EPOCH, txt)
            m_loss_lr = re.search(REGEX_LOSS_LR, txt)
            m_mean_loss = re.search(REGEX_MEAN_LOSS, txt)
            m_top_1 = re.search(REGEX_TOP_1, txt)
            m_top_5 = re.search(REGEX_TOP_5, txt)

            # EPOCH
            if m_epoch:
                cur_epoch = m_epoch.group(1)

            # LOSS, LR
            if m_loss_lr:
                cur_lr = m_loss_lr.group(3)

            # MEAN LOSS
            if m_mean_loss:
                cur_mean_loss = m_mean_loss.group(1)

            # TOP 1
            if m_top_1:
                cur_top_1 = m_top_1.group(1)

            # TOP 5
            if m_top_5:
                cur_top_5 = m_top_5.group(1)

                items.append({
                    'Epoch': cur_epoch,
                    'Mean Loss': cur_mean_loss,
                    'LR': cur_lr,
                    'Top 1': cur_top_1,
                    'Top 5': cur_top_5
                })

        write_csv(output, items)


def write_csv(file_name, items):
    keys = items[0].keys()

    with open(file_name, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, keys)
        writer.writeheader()
        writer.writerows(items)


parser = argparse.ArgumentParser(description='Read model log.')
parser.add_argument('-f', dest='file', help='Log file', required=True)
parser.add_argument('-o', dest='output',
                    help='Output file', default='output.csv')

args = parser.parse_args()
read(args.file, args.output)
