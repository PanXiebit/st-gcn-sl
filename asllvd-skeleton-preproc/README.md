# ASLLVD-Skeleton Dataset Preprocessing

This project aims to process the ASLLVD database to create the **ASLLVD-Skeleton** database. For details on the database and processing steps, check the links below.

[[ST-GCN for Sign Language Paper]](http://www.cin.ufpe.br/~cca5/st-gcn-sl/paper/)

[[ASLLVD-Skeleton Website]](http://www.cin.ufpe.br/~cca5/asllvd-skeleton/)

[[ASLLVD-Skeleton-20 Website]](http://www.cin.ufpe.br/~cca5/asllvd-skeleton-20/)



## Installation

After checkout the project, run the following command to install and get the required libraries
```
bash setup.sh 
```


## Preprocessing

To preprocess ASLLVD dataset, run
```
python main.py preprocessing -c config/preproc-27.yaml [--work_dir <work folder>]
```
The training results, configurations and logging files, will be saved under the ```./work_dir``` by default or ```<work folder>``` if you appoint it.

You can modify the preprocessing parameters in the command line or configuration files. The order of priority is:  command line > config file > default parameter. For more information, use ```main.py -h```.


## Configuration

Details on how to configure preprocessing can be obtained below

[config/](config/)


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
