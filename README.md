# Quick Check Stress Detection 
Description here

## Prerequisites
- MacOS or Linux
- Python 3.6.13
- conda 
- pip

## Setting Up
This project uses Python 3.6.13 but it should work with Python 3.7 as well. The project uses Tensorflow 1.15 therefore it wouldn't work with Python 3.8 and above since the only tensorflow packages available are v2 and above.

To setup the environment, please follow these steps:

- Create a new conda virtual environment in local or cloud services
```
conda create -n quick_check python=3.6
conda activate quick_check
```
- Clone the github repository
```
git clone https://github.com/silverkip/quick-check.git
```
- Install the required packages in the conda environment
```
cd quick-check/build
conda install pip
pip install -r requirements.txt
```
### Install Tensorflow Model Server
Install Tensorflow Model Server (For Debian based distro). Since this project uses Tensorflow 1.15, it's better to use same version for serving.
```
wget 'http://storage.googleapis.com/tensorflow-serving-apt/pool/tensorflow-model-server-1.15.0/t/tensorflow-model-server/tensorflow-model-server_1.15.0_all.deb'
dpkg -i tensorflow-model-server_1.15.0_all.deb
```

## Reference
- [BERT - REST Inference from the fine-tuned model](https://medium.com/delvify/bert-rest-inference-from-the-fine-tuned-model-499997b32851)
- [Predicting Movie Reviews with BERT on TF Hub](https://colab.research.google.com/github/google-research/bert/blob/master/predicting_movie_reviews_with_bert_on_tf_hub.ipynb)
- [Dreaddit: A Reddit Dataset for Stress Analysis in Social Media](https://arxiv.org/abs/1911.00133).

