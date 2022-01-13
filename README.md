# Quick Check Stress Detection 
This is an API that takes training data from Dreaddit database for mental health detection in texts. The idea is to train a NLP model to help supplement mental health apps with stress detection through user's texts inputs. The API is meant to be simple as it only have one function, to give prediction on whether the user is stressed or not based on the text input.

## Prerequisites
- MacOS or Linux
- Python 3.6.13
- conda 
- pip
- Docker (For hosting)

## Setting Up
This project uses Python 3.6.13 but it should work with Python 3.7 as well. The project uses Tensorflow 1.15 therefore it wouldn't work with Python 3.8 and above since the only tensorflow packages available are v2 and above.

To setup the environment, please follow these steps:

1. Create a new conda virtual environment in local or cloud services
```
conda create -n quick_check python=3.6 anaconda
conda activate quick_check
```
2. Clone the github repository
```
git clone https://github.com/silverkip/quick-check.git
```
3. Install the required packages in the conda environment
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

## Using the API
API Link (Hosted on Heroku) : https://quick-check-app.herokuapp.com/v1/models/quick-check:predict
Since the SavedModel doesn't include preprocessing, we have to do it before sending the POST request to the server. The request_sample files provided shows two samples on how to make a request to the API server in Python and Node.js. These files also include a function that does the preprocessing.

### API's Output Structure
The API takes JSON input in this specific format. 
```
{
    "signature_name":"serving_default",
    "instances":[ {"input_ids": [...],
                   "input_mask": [...],
                   "segment_ids": [...],
                   "label_ids": ...} ]
}
```
Do note that the key "instances" contain a single item list containing the dictionary.
### API's Output Structure
The API returns JSON in this specific format. "probabilities" contain an array with the probability vectors used to predict the label using argmax. "labels" is the prediction represented by either 0 or 1. A value of 0 means it's "Non-stress" and a value of 1 is "Stress".
```
{
    "predictions": [ {"probabilities": [Array],
                      "labels": ... } ]
}
```
Inside the "predictions" key is also a single item list containing the dictionary.

## Future Improvements
A very important improvement that can be made is the addition of built-in Tokenizer into the API so that raw string can be posted to the API without having to go through pre-processing.
## References
- [BERT - REST Inference from the fine-tuned model](https://medium.com/delvify/bert-rest-inference-from-the-fine-tuned-model-499997b32851)
- [Predicting Movie Reviews with BERT on TF Hub](https://colab.research.google.com/github/google-research/bert/blob/master/predicting_movie_reviews_with_bert_on_tf_hub.ipynb)
- [Dreaddit: A Reddit Dataset for Stress Analysis in Social Media](https://arxiv.org/abs/1911.00133)
- [TensorFlow Serving with Docker](https://www.tensorflow.org/tfx/serving/docker)
- [Deploy your Tensorflow models on Heroku with a button click](https://towardsdatascience.com/deploy-your-tensorflow-models-on-heroku-with-a-button-click-4fbb0252f870)

