import json
import os
from bert import tokenization

def tokenize(input_string, vocab_file):
  tokenizer = tokenization.FullTokenizer(vocab_file=vocab_file)
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

import requests


headers = {"content-type":"application-json"}
endpoints = "https://quick-check-api.herokuapp.com/v1/models/quick_check:predict"

input_string = "Man I'm so lazy today and just want to sleep all day. I don't feel like doing anything after that breakup."
vocab_file = "assets/vocab.txt"
response = requests.post(endpoints, data=tokenize(input_string, vocab_file), headers=headers)
prediction = json.loads(response.text)
print(prediction['predictions'][0]['labels'])
