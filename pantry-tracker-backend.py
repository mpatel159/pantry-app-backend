#app.py
import logging
from openai import OpenAI
import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


client = OpenAI()

def load_json_schema(schema_file: str) -> dict:
    with open(schema_file, 'r') as file:
        return json.load(file)


image_path = 'unnamed.jpg'





@app.route('/health-check')
def health_check():
    logger.info("in health check")
    return jsonify({"message": "Hello World!"})


@app.route('/processImage', methods=['POST'])
def get_data():
    logger.info('in process image')
    data = request.get_json()
    logger.info('data: ' + str(data))
    image_base64 = data.get('image')
    base64_string = image_base64.split(',')[1]
    logger.info('img: ' + image_base64)
    logger.info('img without ,: ' + base64_string)
    schema = load_json_schema('pantry_schema.json')

    with open(image_path, 'rb') as image_file:
        test_image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    logger.info('tst img; ' + test_image_base64)
    response = client.chat.completions.create(
    model='gpt-4o-mini',
    response_format={"type": "json_object"},
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Extract the properties from this image using the following JSON Schema as a guide: " +
                    json.dumps(schema)},
                {
                    "type": "image_url",
                    "image_url": {"url":
                        f"data:image/jpeg;base64,{base64_string}"}
                }
            ],
        }
    ],
    max_tokens=500,
)
    logger.info(response.choices[0].message.content)
    json_data = json.loads(response.choices[0].message.content)
    logger.info('js data: ' + str(json_data))
    return json_data

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

