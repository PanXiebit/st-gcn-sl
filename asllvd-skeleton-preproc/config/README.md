# Estimated JSON

This is an example JSON estimated by OpenPose. Keypoints are disposed in this sequence:
* Pose (or body)
* Face
* Hands
    * Left
    * Right

```
{
    "version":1.1,
    "people":[
        {
            "pose_keypoints_2d":[582.349,507.866,0.845918,746.975,631.307,0.587007,...],
            "face_keypoints_2d":[468.725,715.636,0.189116,554.963,652.863,0.665039,...],
            "hand_left_keypoints_2d":[746.975,631.307,0.587007,615.659,617.567,0.377899,...],
            "hand_right_keypoints_2d":[617.581,472.65,0.797508,0,0,0,723.431,462.783,0.88765,...]
            "pose_keypoints_3d":[582.349,507.866,507.866,0.845918,507.866,746.975,631.307,0.587007,...],
            "face_keypoints_3d":[468.725,715.636,715.636,0.189116,715.636,554.963,652.863,0.665039,...],
            "hand_left_keypoints_3d":[746.975,631.307,631.307,0.587007,631.307,615.659,617.567,0.377899,...],
            "hand_right_keypoints_3d":[617.581,472.65,472.65,0.797508,472.65,0,0,0,723.431,462.783,0.88765,...]
        }
    ],
    // If `--part_candidates` enabled
    "part_candidates":[
        {
            "0":[296.994,258.976,0.845918,238.996,365.027,0.189116],
            "1":[381.024,321.984,0.587007],
            "2":[313.996,314.97,0.377899],
            "3":[238.996,365.027,0.189116],
            "4":[283.015,332.986,0.665039],
            "5":[457.987,324.003,0.430488,283.015,332.986,0.665039],
            "6":[],
            "7":[],
            "8":[],
            "9":[],
            "10":[],
            "11":[],
            "12":[],
            "13":[],
            "14":[293.001,242.991,0.674305],
            "15":[314.978,241,0.797508],
            "16":[],
            "17":[369.007,235.964,0.88765]
        }
    ]
}
```


# Estimated keypoints

## Body

Estimated keypoints for body, according to COCO model:
<p>
    <img src="../doc/media/keypoints_pose_18.png", width="200">
</p>

| Keypoints | JSON Index | Body Part |
|-----------|------------|-----------|
| 0 - 1     | 0 - 1      | Neck      |
| 2 - 4     | 2 - 4      | Right arm |
| 5 - 7     | 5 - 7      | Left arm  |
| 8 - 10    | 8 - 10     | Right leg |
| 11 - 13   | 11 - 13    | Left leg  |
| 14 - 17   | 14 - 17    | Head      |


## Head

Estimated keypoints for head:

<p>
    <img src="../doc/media/keypoints_face.png", width="450">
</p>

| Keypoints | JSON Index | Body Part     |
|-----------|------------|---------------|
| 0 - 16    | 18 - 34    | Face          |
| 17 - 21   | 35 - 39    | Right eyebrow |
| 22 - 26   | 40 - 44    | Left eyebrow  |
| 27 - 35   | 45 - 53    | Nose          |
| 36 - 41   | 54 - 59    | Right eye     |
| 42 - 47   | 60 - 65    | Left eye      |
| 48 - 67   | 66 - 85    | Mouth         |
| 68        | 86         | Right eyeball |
| 69        | 87         | Left eyeball  |


## Hands

Estimated keypoints for left and right hands:

<p>
    <img src="../doc/media/keypoints_hand.png", width="200">
</p>


### Left Hand

| Keypoints | JSON Index | Body Part     |
|-----------|------------|---------------|
| 0         | 88         | Wrist         |
| 1 - 4     | 89 - 92    | Thumb finger  |
| 5 - 8     | 93 - 96    | Index finger  |
| 9 - 12    | 97 - 100   | Middle finger |
| 13 - 16   | 101 - 104  | Ring finger   |
| 17 - 20   | 105 - 108  | Little finger |

### Right Hand

| Keypoints | JSON Index | Body Part     |
|-----------|------------|---------------|
| 0         | 109        | Wrist         |
| 1 - 4     | 110 - 113  | Thumb finger  |
| 5 - 8     | 114 - 117  | Index finger  |
| 9 - 12    | 118 - 121  | Middle finger |
| 13 - 16   | 122 - 125  | Ring finger   |
| 17 - 20   | 126 - 129  | Little finger |


# Configuration file

This is an example of a configuration file for preprocessing

```
# Example configuration file:

work_dir:       /home/student/dl2/grp5/cca5/dataset/workdir
metadata_file:  /home/student/dl2/grp5/cca5/dataset/dai-asllvd.xlsx
clean_workdir:  False

phases: 
  download, 
  segment, 
  skeleton, 
  filter,
  split,
  normalize

download:
  output_dir:     ../../original
  url:            http://csr.bu.edu/ftp/asl/asllvd/asl-data2/quicktime
  file_pattern:   '{session}/scene{scene}-camera{camera}.mov'
  metadata_url:   http://www.bu.edu/asllrp/dai-asllvd-BU_glossing_with_variations_HS_information-extended-urls-RU.xlsx

segment:
  input_dir:    ../../original
  output_dir:   segmented
  fps_in:       60
  fps_out:      30

skeleton:
  openpose:   /home/student/dl2/grp5/cca5/openpose/openpose/build
  input_dir:  ./segmented
  output_dir: ./skeleton
  model_path: ./st-gcn/models

filter:
  input_dir:  ./skeleton
  output_dir: ./filtered
  points:     1, 2, 3, 5, 6,
              88, 90, 92, 94, 96, 98, 100, 102, 104, 106, 108,
              109, 111, 113, 115, 117, 119, 121, 123, 125, 127, 129

split:
  input_dir:  ./filtered
  output_dir: ./splitted
  test:       20
  val:        0
  seed:       2

normalize:
  input_dir:      ./splitted
  output_dir:     ./normalized
  joints:         27
  channels:       3
  num_person:     1
  repeat_frames:  True
  max_frames:     63

# debug_opts:
#  download_items:   5
#  split_items:      5
#  pose_items:       5
#  gendata_items:    5
#  gendata_joints:   27

```