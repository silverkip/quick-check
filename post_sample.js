const {BertTokenizer} = require('bert-tokenizer');
const axios = require('axios')

const CLASSES = ["Non-stress", "Stress"] // For label value

const vocabUrl = 'node_modules/bert-tokenizer/assets/vocab.json'
const bertTokenizer = new BertTokenizer(vocabUrl, true);


function tokenizeInput(inputText) {
  let token = bertTokenizer.convertSingleExample(inputText);
  let listObj = '[{"input_ids": ['+ token["inputIds"] + '], "input_mask": [' + token["inputMask"] + '], "segment_ids": [' + token["segmentIds"] + '], "label_ids": 0}]';

  const obj= JSON.parse(listObj);

  var data = JSON.stringify({
    "signature_name":"serving_default",
    "instances":obj
  });
  // console.log(data);
  return data;
}

async function makeGetRequest(payload) {
  let res = await axios.post('http://192.168.11.9:8501/v1/models/quick_check:predict', payload);
  
  let data = res.data;
  // Data returns a dictionary and in the 'predictions' key there's a list with 1 item. The item contains 'labels' and 'probabilities' keys.
  // Label value of 0 means non-stress, and 1 means stress.
  console.log("Label : " + CLASSES[data['predictions'][0]['labels']])
  console.log("Probability Vectors : " + data['predictions'][0]['probabilities'])
}

const sampleText = "Man I'm so lazy today and just want to sleep all day. I don't feel like doing anything after that breakup.";

var payload = tokenizeInput(sampleText);
makeGetRequest(payload);