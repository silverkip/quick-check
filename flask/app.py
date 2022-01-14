import numpy as np
import requests
from flask import Flask, request, jsonify
import json
from flask_cors import CORS
from bert import tokenization

app = Flask(__name__)
CORS(app)

VOCAB_FILE = "assets/vocab.txt"

def tokenize(input_string):
  tokenizer = tokenization.FullTokenizer(vocab_file= VOCAB_FILE)
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
  data = {"input_text" : input_string, "prediction":CLASSES[prediction['predictions'][0]['labels']], "probability-vectors":prediction['predictions'][0]['probabilities']}
  return data

# Testing URL
@app.route('/hello/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello, World!'

@app.route('/quickcheck/predict/', methods=['POST'])
def predict_stress():
    response = []
    # Decoding and pre-processing base64 image
    input_string = json.loads(request.data.decode(encoding="ascii"))
    for x in input_string:
        print(x)
        response.append(predict(x))
    return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0')