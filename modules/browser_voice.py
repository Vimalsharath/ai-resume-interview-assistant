import streamlit.components.v1 as components

def speak(text):
    text = text.replace("'", "\\'")

    components.html(
        f"""
        <script>
        var msg = new SpeechSynthesisUtterance();
        msg.text = '{text}';
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(msg);
        </script>
        """,
        height=0
    )