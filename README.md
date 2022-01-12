# Quick Check Stress Detection 
Description here

## Prerequisites
- MacOS or Linux
- Python 3.6.13
- conda 
- pip
- Docker (For hosting)

## Setting Up
This project uses Python 3.6.13 but it should work with Python 3.7 as well. The project uses Tensorflow 1.15 therefore it wouldn't work with Python 3.8 and above since the only tensorflow packages available are v2 and above.

To setup the environment, please follow these steps:

- Create a new conda virtual environment in local or cloud services
```
conda create -n quick_check python=3.6 anaconda
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
### Install TensorFlow Model Server (Optional)
Install TensorFlow Model Server (For Debian based distro). Since this project uses Tensorflow 1.15, it's better to use same version for serving.
```
wget 'http://storage.googleapis.com/tensorflow-serving-apt/pool/tensorflow-model-server-1.15.0/t/tensorflow-model-server/tensorflow-model-server_1.15.0_all.deb'
dpkg -i tensorflow-model-server_1.15.0_all.deb
```

## Hosting the REST API Server
The model file can be downloaded from this link: https://quick-check-model.s3.ap-northeast-1.amazonaws.com/model.zip

### Hosting with Docker (Recommended)
First of all, pull the latest TensorFlow serving Docker image with this command
```
docker pull tensorflow/serving
```
The model file is hosted and is publicly available in this S3 bucket (s3://quick-check-model) and can be easily deployed through docker with these commands
```
docker run \
    -p 8500:8500 \
    -p 8501:8501 \
    -e AWS_REGION=ap-northeast-1 \
    -e S3_ENDPOINT=s3.ap-northeast-1.amazonaws.com \
    -e TF_CPP_MIN_LOG_LEVEL=3 \
    tensorflow/serving
    --model_config_file=s3://quick-check-model/config/models.config
```
### Hosting local model with Docker
To host the model locally with Docker, run these commands. Replace [Path to Model Directory] with the absolute path of the model directory.
```
docker run -t --rm -p 8501:8501 \
    -v "[Path to Model Directory]:/models/quick_check" \
    -e MODEL_NAME=quick_check \
    tensorflow/serving
```
### Hosting it locally with Tensorflow Model Server
```
tensorflow_model_server --port=8500 --rest_api_port=8501 --model_name=quick_check --model_base_path=/model
```

## Reference
- [BERT - REST Inference from the fine-tuned model](https://medium.com/delvify/bert-rest-inference-from-the-fine-tuned-model-499997b32851)
- [Predicting Movie Reviews with BERT on TF Hub](https://colab.research.google.com/github/google-research/bert/blob/master/predicting_movie_reviews_with_bert_on_tf_hub.ipynb)
- [Dreaddit: A Reddit Dataset for Stress Analysis in Social Media](https://arxiv.org/abs/1911.00133)
- [TensorFlow Serving with Docker](https://www.tensorflow.org/tfx/serving/docker)

