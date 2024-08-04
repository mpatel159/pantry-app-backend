#app.py
from openai import OpenAI
import json
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

client = OpenAI()

def load_json_schema(schema_file: str) -> dict:
    with open(schema_file, 'r') as file:
        return json.load(file)


@app.route('/health-check')
def health_check():
    return jsonify({"message": "Hello World!"})


@app.route('/processImage', methods=['GET'])
def get_data():
    data = request.get_json()
    image_base64 = data.get('image')
    schema = load_json_schema('pantry_schema.json')
    
    response = client.chat.completions.create(
    model='gpt-4o',
    response_format={"type": "json_object"},
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "provide JSON file that represents this document. Use this JSON Schema: " +
                    json.dumps(schema)},
                {
                    "type": "image_url",
                    "image_url": {"url":
                        f"data:image/jpeg;base64,{image_base64}"}
                }
            ],
        }
    ],
    max_tokens=500,
)
    print(response.choices[0].message.content)
    json_data = json.loads(response.choices[0].message.content)
    return json_data

if __name__ == '__main__':
    app.run(debug=True)

