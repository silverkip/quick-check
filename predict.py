# Predict Function that sends the request to the API and parses the result

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
 
import json
from bert import tokenization
import requests
import warnings
import logging, sys

logging.disable(sys.maxsize)
warnings.filterwarnings("ignore")

VOCAB_FILE = "assets/vocab.txt"

def tokenize(input_string):
  tokenizer = tokenization.FullTokenizer()
  token_a = tokenizer.tokenize(input_string)

  tokens = []
  tokens.append("[CLS]")
  segment_ids = []
  segment_ids.append(0)
  for token in token_a:
      tokens.append(token)
      segment_ids.append(0)
  tokens.append('[SEP]')
  segment_ids.append(0)
  input_ids = tokenizer.convert_tokens_to_ids(tokens)
  input_mask = [1] * len(input_ids)
  max_seq_length = 256
  while len(input_ids) < max_seq_length:
      input_ids.append(0)
      input_mask.append(0)
      segment_ids.append(0)
  label_id = 0
  instances = [{"input_ids":input_ids, "input_mask":input_mask, "segment_ids":segment_ids, "label_ids":label_id}]
  data = json.dumps({"signature_name":"serving_default", "instances":instances})
  return data

def predict(input_string):
  CLASSES=["non-stress", "stress"] # Represents the 'labels' key's value from output

  headers = {"content-type":"application-json"}
  endpoints = "https://quick-check-api.herokuapp.com/v1/models/quick_check:predict"

  response = requests.post(endpoints, data=tokenize(input_string), headers=headers)
  prediction = json.loads(response.text)
  # 'labels' is the prediction which is either 0 or 1. 0 for Non-Stress and 1 for Stress
  print('Input Text : ', input_string)
  print('Prediction : ', CLASSES[prediction['predictions'][0]['labels']])
  print('Probability Vectors : ', prediction['predictions'][0]['probabilities'])

predict("TEST")
