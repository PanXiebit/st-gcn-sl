from pathlib import Path
import json

parts = ['pose_keypoints_2d', 'face_keypoints_2d',
         'hand_left_keypoints_2d', 'hand_right_keypoints_2d']


def json_pack(snippets_dir, video_name, frame_width, frame_height, label='unknown', label_index=-1):
    sequence_info = []
    p = Path(snippets_dir)

    for path in p.glob(video_name+'*.json'):
        json_path = str(path)
        # print(path)
        frame_id = int(path.stem.split('_')[-2])
        frame_data = {'frame_index': frame_id}
        data = json.load(open(json_path))
        skeletons = []

        for person in data['people']:
            skeleton = {}
            skeleton['pose'] = []
            skeleton['score'] = []

            for part_name in parts:
                score, coordinates = read_coordinates(
                    part_name, person, frame_width, frame_height)
                skeleton['pose'] += coordinates
                skeleton['score'] += score
            skeletons += [skeleton]

        frame_data['skeleton'] = skeletons
        sequence_info += [frame_data]

    video_info = dict()
    video_info['data'] = sequence_info
    video_info['label'] = label
    video_info['label_index'] = label_index
    return video_info


def read_coordinates(part_name, person, frame_width, frame_height):
    score, coordinates = [], []
    keypoints = person[part_name]
    for i in range(0, len(keypoints), 3):
        coordinates += [keypoints[i]/frame_width,
                        keypoints[i + 1]/frame_height]
        score += [keypoints[i + 2]]
    return score, coordinates
