# Spatial Temporal Graph Convolutional Networks (ST-GCN) for Sign Language Recognition


This repository is a fork of the original repository available at the URL below, which is the codebase for the paper **Spatial Temporal Graph Convolutional Networks for Skeleton-Based Action Recognition** Sijie Yan, Yuanjun Xiong and Dahua Lin, AAAI 2018.


[[ST-GCN Github Repository]](https://github.com/yysijie/st-gcn)

[[ST-GCN Arxiv Preprint]](https://arxiv.org/abs/1801.07455)


You can download **Spatial-Temporal Graph Convolutional Networks
for Sign Language Recognition** paper through the link below

[[ST-GCN for Sign Language Paper]](http://www.cin.ufpe.br/~cca5/st-gcn-sl-paper/)


## Installation

After checkout the project, run the following command to install and get the required libraries
```
bash setup.sh 
```


### Get pre-trained body, hand and face models
The model weights can be downloaded by running the script
```
bash tools/get_models.sh
```
The downloaded models will be stored under ```./models```.


## Training
To train a new ST-GCN model, run
```
python main.py recognition -c config/sl/train.yaml [--work_dir <work folder>]
```
The training results, including **model weights**, configurations and logging files, will be saved under the ```./work_dir``` by default or ```<work folder>``` if you appoint it.

You can modify the training parameters such as ```work_dir```, ```batch_size```, ```step```, ```base_lr``` and ```device``` in the command line or configuration files. The order of priority is:  command line > config file > default parameter. For more information, use ```main.py -h```.

Finally, custom model evaluation can be achieved by this command as we mentioned above:
```
python main.py -c config/sl/test.yaml --weights <path to model weights>
```


## Citation
Please cite the following paper if you use this repository in your reseach.
```
@article{stgcnsl2019,
  title     = {Spatial-Temporal Graph Convolutional Networks for Sign Language Recognition},
  author    = {Cleison Correia de Amorim and David Macêdo and Cleber Zanchettin},
  year      = {2019},
}
```

## Contact
For any question, feel free to contact me at
```
Cleison Amorim  : cca5@cin.ufpe.br
```
