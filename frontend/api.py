from flask import Blueprint, jsonify
import json
import os
from flask import request, send_file
import requests
import re
import glob

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

def is_valid_audio_filename(filename):
    # Allow only alphanumeric, underscores, dashes, dots; must end with valid audio extension
    valid_audio_exts = ('.mp3', '.wav', '.ogg', '.flac', '.m4a')
    if not filename:
        return False
    if not any(filename.lower().endswith(ext) for ext in valid_audio_exts):
        return False
    # Prevent directory traversal by disallowing slashes or backslashes
    if '/' in filename or '\\' in filename:
        return False
    # Basic filename pattern check (no weird characters)
    pattern = r'^[\w,\s-]+\.[A-Za-z]{3,4}$'  # e.g. output_01.mp3
    if not re.match(pattern, filename):
        return False
    return True

@api_bp.route("/list_models",)
def list_models():
    models = os.listdir("../models")
    return jsonify(models)


@api_bp.route("/synthesise_stream", methods=["POST"])
def synthesise_stream():
    pass

@api_bp.route("/synthesise", methods=["POST"])
def synthesise():
    # get the params
    data = request.get_json()

    model =               data.get("model", "Hu Tao")                     # (optional) str: text to be synthesized  
    output_lan  =         data.get("output_lan", "en")                    # (optional) str: output language
    infer_text =          data.get("infer_text", None)                    # (required) str: language of the text to be synthesized  
           
    top_k =               data.get("top_k", 5)                            # (optional) int: top-k sampling  
    top_p =               float(data.get("top_p", 1))                     # (optional) float: top-p sampling  
    temperature =         float(data.get("temperature", 1))               # (optional) float: temperature for sampling  
           
    text_split_method =   data.get("text_split_method", "cut0")           # (optional) str: text split method (see text_segmentation_method.py for options)  
    batch_size =          data.get("batch_size", 1)                       # (optional) int: batch size for inference  
    batch_threshold =     float(data.get("batch_threshold", 0.75))        # (optional) float: threshold for batch splitting  
    split_bucket =        data.get("split_bucket", True)                  # (optional) bool: whether to split the batch into multiple buckets  
           
    speed_factor =        float(data.get("speed_factor", 1.0))            # (optional) float: control the speed of the synthesized audio  
    streaming_mode =      data.get("streaming_mode", False)               # (optional) bool: whether to return a streaming response  
    fragment_interval =   float(data.get("fragment_interval", 0.3))       # (optional) float. to control the interval of the audio fragment.
    seed =                data.get("seed", -1)                            # (optional) int: random seed for reproducibility  
    parallel_infer =      data.get("parallel_infer", True)                # (optional) bool: whether to use parallel inference  
    repetition_penalty =  float(data.get("repetition_penalty", 1.35))     # (optional) float: repetition penalty for T2S model  
    sample_steps =        data.get("sample_steps", 32)                    # (optional) int: number of sampling steps for VITS model V3  
    super_sampling =      data.get("super_sampling", False)               # (optional) bool: whether to use super-sampling for audio when using VITS model V3  
    output_file =         data.get("output_file", "output.wav")           # (optional) str: output file name
    

    errors = []

    # format output file to wav
    output_file = os.path.splitext(os.path.basename("output.mp3"))[0] + ".wav"

    # get model data
    model_path      =   os.path.join("models", model)

    if os.path.exists(model_path):
       ref_audio_path  =   os.path.join("models", model, "ref_audio.ogg")
       ref_json_path   =   os.path.join("models", model, "refrance.json")
       ref_audio_text =    json.load(open(ref_json_path, "r", encoding="utf-8")).get("ref_audio_text", None)
       ref_audio_lang =    json.load(open(ref_json_path, "r", encoding="utf-8")).get("ref_audio_lang", None)
    else:
        ref_audio_path = ref_audio_text = ref_audio_lang = None
        errors.append(f"Model {model} does not exist")

    # validate inputs
    required_fields = [
    (infer_text, "infer_text cannot be None"),
    (ref_audio_text, "ref_audio_text in json not found"),
    (ref_audio_lang, "ref_audio_lang in json not found"),
    ]

    for value, error_message in required_fields:
        if not value:
            errors.append(error_message)

    type_checks = [
     (model, str, "model must be a string"),
     (infer_text, str, "infer_text must be a string"),   
     (top_k, int, "top_k must be an integer"),
     (top_p, float, "top_p must be a float"),
     (temperature, float, "temperature must be a float"),
     (text_split_method, str, "text_split_method must be a string"),
     (batch_size, int, "batch_size must be an integer"),
     (batch_threshold, float, "batch_threshold must be a float"),
     (split_bucket, bool, "split_bucket must be a boolean"),
     (speed_factor, float, "speed_factor must be a float"),
     (streaming_mode, bool, "streaming_mode must be a boolean"),
     (fragment_interval, float, "fragment_interval must be a float"),
     (seed, int, "seed must be an integer"),
     (parallel_infer, bool, "parallel_infer must be a boolean"),
     (repetition_penalty, float, "repetition_penalty must be a float"),
     (sample_steps, int, "sample_steps must be an integer"),
     (super_sampling, bool, "super_sampling must be a boolean"),
     (output_file, str, "output_file must be a string"),
     (output_lan, str, "output_lan must be a string"),
    ]

    for var, expected_type, message in type_checks:
     if type(var) is not expected_type:
        errors.append(message) 

    extra_refs_dir = os.path.join("models", model, "extra_refs")
    extra_refs = [os.path.join(extra_refs_dir, f) for f in os.listdir(extra_refs_dir) if os.path.isfile(os.path.join(extra_refs_dir, f)) and any(f.endswith(ext) for ext in ['.mp3', '.wav', '.ogg', '.flac', '.m4a'])] if os.path.exists(extra_refs_dir) else []

    if errors:
     return errors
    
    payload = {
     "text": infer_text,
     "text_lang": output_lan,
     "ref_audio_path": f"/app/{ref_audio_path}",
     "aux_ref_audio_paths": extra_refs,
     "prompt_text": ref_audio_text,
     "prompt_lang": ref_audio_lang,
     "top_k": top_k,
     "top_p": top_p,
     "temperature": temperature,
     "text_split_method": text_split_method,
     "batch_size": batch_size,
     "batch_threshold": batch_threshold,
     "split_bucket": split_bucket,
     "speed_factor": speed_factor,
     "streaming_mode": streaming_mode,
     "seed": seed,
     "parallel_infer": parallel_infer,
     "repetition_penalty": repetition_penalty,
     "sample_steps": sample_steps,
     "super_sampling": super_sampling
     }
    
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(
            "http://gpt-sovits-api:9880/tts",
            headers=headers,
            data=json.dumps(payload),
            timeout=60,
            stream=True
        )

        if response.status_code == 200:
            with open(output_file, "wb") as f:
                for chunk in response.iter_content(chunk_size=4096):
                    if chunk:
                        f.write(chunk)
            print("✅ Audio saved")
            return send_file(output_file, mimetype="audio/wav", as_attachment=True)

        else:
            print(f"❌ Failed ({response.status_code}): {response.text}")
            return jsonify({"error": "Bad response", "status_code": response.status_code}), 500

    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return jsonify({"error": "Request timed out"}), 504

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return jsonify({"error": str(e)}), 502 