import requests
import time

response = requests.post(
    'http://localhost:80/synthesise',
    json={
        'infer_text': (
            "Good morning, Andre. How are you feeling today? "
            "I hope everything’s going well and you’re having a good start to your day. "
            "Did you sleep well last night? The weather outside looks lovely, perfect for a nice walk or some fresh air. "
            "Remember to take breaks if you’re working hard. Staying hydrated is important too! "
            "Have you got any exciting plans for today? Maybe a chance to catch up with friends or family? "
            "If you feel stressed, try to take a moment for yourself. "
            "It’s always good to stay positive and focused on your goals. "
            "Don’t forget to enjoy the little things that make your day special. "
            "I’m here if you want to chat or need anything else."
        ),
        'streaming_mode': True
    },
    stream=True  # ✅ Critical for streaming
)


with open("output.wav", "wb") as f:
    for chunk in response.iter_content(chunk_size=4096):
        if chunk:
            f.write(chunk)
            f.flush()
            print(f"Received chunk of size {len(chunk)} bytes")
            time.sleep(0.5)  # slow down to watch chunks arriving

