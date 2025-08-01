from flask import Blueprint, jsonify
import json
import os
from flask import request
import requests

# Create a Blueprint for this file
api_bp = Blueprint('api', __name__)

def get_model_info_by_name(data, target_name):
    for model in data.get("models", []):
        if model.get("name") == target_name:
            return {
                "name": model.get("name"),
                "ref_audio": model.get("ref_audio"),
                "ref_text": model.get("ref_text"),
                "ref_language": model.get("ref_language"),
                "extra_refs": model.get("extra_refs", [])
            }
    return None  # Not found


@api_bp.route("/synthesise", methods=["POST"])
def synthesise():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, "models.json")

    data = request.get_json()

    output_file = f"../models/{data.get('output_file')}"

    model = data.get("model")
    if not model:
        return jsonify({"error": "No model specified"}), 400

    try:
        with open(json_path, "r") as f:
            model_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return jsonify({"error": str(e)}), 500

    result = get_model_info_by_name(model_data, model)
    if not result:
        return jsonify({"error": "Model not found"}), 404

    infrance_text = data.get("infrance_text")
    if not infrance_text:
        return jsonify({"error": "Inference text missing"}), 400

    lang_map = {"eng": "英文"}
    ref_language = lang_map.get(result.get("ref_language"), result.get("ref_language"))
    output_language = lang_map.get(data.get("output_language", "eng"))

    # Transform path to gpt sovits path
    refer_audio_path = result.get("ref_audio")
    refer_gpt_sovits_path = f"../models/{model}/{refer_audio_path}"    

    payload = {
        "refer_wav_path": refer_gpt_sovits_path,
        "prompt_text": result.get("ref_text"),
        "prompt_language": ref_language,
        "text": infrance_text,
        "text_language": output_language,
        "cut_punc": data.get("cut_punc", None),
        "top_k": data.get("top_k", 15),
        "top_p": data.get("top_p", 1.0),
        "temperature": data.get("temperature", 1.0),
        "speed": data.get("speed", 1.0),
        "inp_refs": result.get("extra_refs"),
        "sample_steps": data.get("sample_steps", 32),
        "if_sr": data.get("if_sr", False)
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post("http://gpt-sovits-api:9880", headers=headers, data=json.dumps(payload), timeout=30)
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return None, None
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None, None

    if response.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(response.content)
        return jsonify({"output_file": output_file})
    else:
        print(f"❌ Failed ({response.status_code}): {response.text}")
        return None
