#!/bin/bash
set -e

# Initialize conda
source /opt/conda/etc/profile.d/conda.sh

# Activate conda environment
conda activate gpt

# Check if installation has already been done
if [ ! -f /opt/gpt-installed.flag ]; then
    echo "Installing GPT-SoVITS..."

    # Clone GPT-SoVITS repo
    git clone https://github.com/RVC-Boss/GPT-SoVITS.git /app

    # add status to api call
    python3 -c "path = '/app/api.py'; new_code = '\n@app.get(\"/status\")\nasync def get_status():\n    return JSONResponse(content={\"status\": \"online\"})\n'; lines = open(path).readlines(); i = next((i for i, l in enumerate(lines) if '__main__' in l), len(lines)); lines.insert(i, new_code); open(path, 'w').writelines(lines)"

    # replace broken api ref call
    python3 -c "path='/app/api.py'; lines=open(path).readlines(); lines=[l.replace('path.name', 'path') if 'refer, audio_tensor = get_spepc(hps, path.name, dtype, device, is_v2pro)' in l else l for l in lines]; open(path, 'w').writelines(lines)"

    # Install python dependencies inside conda env
    pip install --upgrade pip
    pip install --no-cache-dir -r /app/extra-req.txt
    pip install --no-cache-dir -r /app/requirements.txt

    python3 -c "import nltk; nltk.download('averaged_perceptron_tagger_eng')"

    # Clone pretrained models
    rm -rf /app/GPT_SoVITS/pretrained_models
    git clone https://huggingface.co/lj1995/GPT-SoVITS /app/GPT_SoVITS/pretrained_models

    # Pull Git LFS files
    cd /app/GPT_SoVITS/pretrained_models
    git lfs pull

    # Mark installation done
    touch /opt/gpt-installed.flag

    echo "Installation complete!"
else
    echo "GPT-SoVITS already installed, skipping install"
fi

echo "starting api"

# Start the api
cd /app

python3 api.py