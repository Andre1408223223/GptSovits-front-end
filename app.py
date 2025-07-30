from flask import Flask, request, jsonify,render_template
import os
from werkzeug.utils import secure_filename

tts_dir = os.path.join(os.getcwd(), 'tts_outputs')
os.makedirs(tts_dir, exist_ok=True)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inference', methods=['POST'])
def inference():
    # Parse form fields
    text = request.form.get('text')
    refer_wav = request.files.get('refer_wav_path')
    prompt_text = request.form.get('prompt_text')
    prompt_lang = request.form.get('prompt_language', 'eng')
    text_lang = request.form.get('text_language', 'eng')
    model = request.form.get('model', 'Hu Tao')
    cut_punc = request.form.get('cut_punc', None)
    top_k = int(request.form.get('top_k', 0))
    top_p = float(request.form.get('top_p', 1.0))
    temperature = float(request.form.get('temperature', 1.0))
    speed = float(request.form.get('speed', 1.0))
    sample_steps = int(request.form.get('sample_steps', 32))
    if_sr = request.form.get('if_sr') == 'true'
    output_file = request.form.get('output_file', 'output.wav')

    # Save reference audio if provided
    ref_path = None
    if refer_wav:
        filename = secure_filename(refer_wav.filename)
        ref_path = os.path.join(tts_dir, filename)
        refer_wav.save(ref_path)

    # Placeholder for actual GPT-SoVITS call
    # generate_audio(reference=ref_path, text=text, ... other params ...)
    # For demonstration, we simply touch the output file
    out_path = os.path.join(tts_dir, secure_filename(output_file))
    with open(out_path, 'wb') as f:
        f.write(b'')  # Replace with real audio bytes

    # Return JSON with success message and download URL
    return jsonify({
        'message': 'Inference completed',
        'download_url': f'/download/{os.path.basename(out_path)}'
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
