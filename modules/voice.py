import json
from pathlib import Path

import streamlit.components.v1 as components


_COMPONENT_PATH = Path(__file__).resolve().parent / "voice_recorder"

_voice_component = components.declare_component(
    "voice_recorder",
    path=str(_COMPONENT_PATH),
)


def speak(text):
    text = text or ""
    script = f"""
    <script>
    const speechText = {json.dumps(text)};
    if (window.speechSynthesis) {{
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(speechText);
        utterance.lang = "en-US";
        utterance.rate = 1;
        utterance.pitch = 1;
        utterance.volume = 1;
        window.speechSynthesis.speak(utterance);
    }}
    </script>
    """
    components.html(script, height=0)


def listen():
    transcript = _voice_component()
    return transcript or ""
