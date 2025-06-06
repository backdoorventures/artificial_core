import os
import tempfile
from google.cloud import texttospeech
from google.oauth2 import service_account

# Load credentials from env (as JSON string)
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["GOOGLE_SERVICE_ACCOUNT"]
)

tts_client = texttospeech.TextToSpeechClient(credentials=credentials)

def generate_voiceover(text, voice_name="en-US-Chirp3-HD-Algieba"):
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice_name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    response = tts_client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp_audio.write(response.audio_content)
    temp_audio.close()

    return temp_audio.name  # return path to .wav

