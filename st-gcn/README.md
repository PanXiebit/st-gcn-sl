# Spatial Temporal Graph Convolutional Networks for Sign Language (ST-GCN-SL) Recognition


This repository is a fork of the original repository available at the URL below, which is the codebase for the paper **Spatial Temporal Graph Convolutional Networks for Skeleton-Based Action Recognition** Sijie Yan, Yuanjun Xiong and Dahua Lin, AAAI 2018.


[[ST-GCN Github Repository]](https://github.com/yysijie/st-gcn)

[[ST-GCN Arxiv Preprint]](https://arxiv.org/abs/1801.07455)


You can download **Spatial-Temporal Graph Convolutional Networks
for Sign Language Recognition** paper through the link below

[[ST-GCN-SL Preprint]](http://www.cin.ufpe.br/~cca5/st-gcn-sl/preprint/)

[[ST-GCN-SL Final Paper]](http://www.cin.ufpe.br/~cca5/st-gcn-sl/paper/)


## Installation

After checkout the project, run the following command to install and get the required libraries
```
bash setup.sh 
```


### Get pre-trained body, hand and face models
The body, hand and face models can be downloaded by running the script
```
bash tools/get_models.sh
```
The downloaded models will be stored under ```./models```.


### Get pre-trained weights
The weights trained for the **ASLLVD-Skeleton** and **ASLLVD-Skeleton-20**  databases, according to the article presented above, can be downloaded from the link

[[Pre-trained Weights]](http://www.cin.ufpe.br/~cca5/st-gcn-sl/weights/)

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
@InProceedings{st-gcn-sl-2019,
  author="de Amorim, Cleison Correia 
          and Mac{\^e}do, David
          and Zanchettin, Cleber",
  editor="Tetko, Igor V.
          and K{\r{u}}rkov{\'a}, V{\v{e}}ra
          and Karpov, Pavel
          and Theis, Fabian",
  title="Spatial-Temporal Graph Convolutional Networks for Sign Language Recognition",
  booktitle="Artificial Neural Networks and Machine Learning -- ICANN 2019: Workshop and Special Sessions",
  year="2019",
  publisher="Springer International Publishing",
  address="Cham",
  pages="646--657",
  isbn="978-3-030-30493-5"
}
```

## Contact
For any question, feel free to contact me at
```
Cleison Amorim  : cca5@cin.ufpe.br
```
