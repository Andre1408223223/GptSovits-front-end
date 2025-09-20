**GPT Sovits Frontend**
This is the frontend code for GPT Sovits. It also automatically installs GPT Sovits.

**requrments**
Docker
Dokcer compose
Cuda in wsl 

**installation**
Simply navigate to the GptSovits-front-end directory, then run:
docker compose up

to chek if you have cude in wsl run 
nvidia-smi

if you see your gpu cuda is working if not please install cuda 


**Installing Different Models**
The frontend code does not update automatically yet. To add a new model:

Create a new folder inside the models directory.

Name the folder after the model you want to add.

Add a reference audio file to that folder.

You will need to adjust the models file accordingly.

**API Parameters**
refer_wav_path: Path to the reference audio file that guides the voice synthesis.

prompt_text: Text corresponding to the reference audio.

prompt_language: Language of the reference audio text.

text: The sentence you want to convert into speech.

text_language: Language of the input sentence.

cut_punc (optional): Cut punctuation parameter to control how punctuation is handled. Useful for languages with complex tokenization, helping the model segment the text more effectively.

top_k (optional): Top-k sampling parameter controlling output diversity by limiting candidate tokens at each step. Balances randomness and determinism.

top_p (optional): Top-p (nucleus) sampling parameter that sets a cumulative probability threshold for token selection. 1.0 means no truncation; lower values make output more focused and deterministic.

temperature (optional): Controls randomness of the output. Higher values (e.g., 1.0) produce more creative speech, while lower values (e.g., 0.5) yield more predictable output.

speed (optional): Speed of the generated speech. 1.0 is normal speed; greater than 1.0 speeds up speech; less than 1.0 slows it down.

inp_refs (optional): List of additional reference audio files providing more context or variation, helping generate speech with a broader range of vocal characteristics.

sample_steps (optional): Number of sampling steps during speech generation. More steps can improve quality but increase processing time.

if_sr (optional): Flag indicating whether to apply super-resolution to the audio output. Setting to True enhances audio quality, making it clearer and more natural.
