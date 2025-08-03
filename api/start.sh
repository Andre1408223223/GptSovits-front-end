#!/bin/bash
set -e

# Initialize conda
source /opt/conda/etc/profile.d/conda.sh

# Activate conda environment
conda activate gpt

# Check if installation has already been done
if [ ! -f /app/shared/gpt-installed.flag ]; then
    echo "Installing GPT-SoVITS..."

    # Clone GPT-SoVITS repo
    git clone https://github.com/RVC-Boss/GPT-SoVITS.git /app/GPT-SoVITS

    # add status to api call
    python3 -c "path = '/app/GPT-SoVITS/api_v2.py'; new_code = '\n@APP.get(\"/status\")\nasync def get_status():\n    return JSONResponse(content={\"status\": \"online\"})\n'; lines = open(path).readlines(); i = next((i for i, l in enumerate(lines) if '__main__' in l), len(lines)); lines.insert(i, new_code); open(path, 'w').writelines(lines)"

    python3 -c "path='/app/GPT-SoVITS/api_v2.py'; lines=open(path).readlines(); lines=[line.replace('host=host', 'host=\"0.0.0.0\"') if 'uvicorn.run(' in line and 'host=host' in line else line for line in lines]; open(path,'w').writelines(lines)"

    # Install python dependencies inside conda env
    pip install --upgrade pip
    pip install --no-cache-dir -r /app/GPT-SoVITS/extra-req.txt
    pip install --no-cache-dir -r /app/GPT-SoVITS/requirements.txt

    python3 -c "import nltk; nltk.download('averaged_perceptron_tagger_eng')"

    # Clone pretrained models
    rm -rf /app/GPT-SoVITS/GPT_SoVITS/pretrained_models
    git clone https://huggingface.co/lj1995/GPT-SoVITS /app/GPT-SoVITS/GPT_SoVITS/pretrained_models

    # Pull Git LFS files
    cd /app/GPT-SoVITS/GPT_SoVITS/pretrained_models
    git lfs pull

    # Mark installation done
    mkdir -p /app/shared/
    touch /app/shared/gpt-installed.flag

    echo "Installation complete!"
else
    echo "GPT-SoVITS already installed, skipping install"
fi

echo "starting api"

# Start the api
cd /app/GPT-SoVITS
python3 api_v2.py