sudo apt update && apt install -y libsm6 libxext6

pip install -r requirements.txt 
cd torchlight; python setup.py install; cd ..

