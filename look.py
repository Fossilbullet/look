from flask import Flask, request, jsonify
import http.client
import json
from flask_cors import CORS
import os  # ✅ Required for reading environment variables

app = Flask(__name__)
CORS(app, origins=["https://a-i-face-video-generator-wnb1vi.flutterflow.app/"])

@app.route('/generate-video', methods=['POST'])
def generate_video():
    data = request.get_json()
    prompt = data.get('prompt')
    image_url = data.get('image_url') 
    if not prompt:
        return jsonify({"error": "Missing 'prompt' in request body"}), 400

    # ✅ Get API key from environment variable
    API_KEY = os.getenv("PIAPI_API_KEY")
    if not API_KEY:
        return jsonify({"error": "API key not set in environment"}), 500

    conn = http.client.HTTPSConnection("api.piapi.ai")

    payload = json.dumps({
        "model": "kling",
        "task_type": "video_generation",
        "input": {
            "prompt": prompt,
            "image_url": image_url,
            "negative_prompt": "",
            "cfg_scale": 0.5,
            "duration": 5,
            "aspect_ratio": "1:1",
            "camera_control": {
                "type": "simple",
                "config": {
                    "horizontal": 0,
                    "vertical": 0,
                    "pan": -10,
                    "tilt": 0,
                    "roll": 0,
                    "zoom": 0
                }
            },
            "mode": "pro",
            "version": "1.6"
        },
        "config": {
            "service_mode": "",
            "webhook_config": {
                "endpoint": "",
                "secret": ""
            }
        }
    })

    headers = {
        'x-api-key': API_KEY,
        'Content-Type': 'application/json'
    }

    try:
        conn.request("POST", "/api/v1/task", payload, headers)
        res = conn.getresponse()
        response_data = res.read().decode("utf-8")
        return jsonify(json.loads(response_data))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))