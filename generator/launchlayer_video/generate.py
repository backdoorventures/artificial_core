import os
import tempfile
import gc

from generator.launchlayer_video.script_writer import expand_keyword_to_script
from generator.launchlayer_video.title_maker import generate_title
from generator.launchlayer_video.description_builder import generate_description
from generator.launchlayer_video.voiceover import generate_voiceover
from generator.launchlayer_video.layout import generate_text_images
from generator.launchlayer_video.renderer import render_final_video

def generate_video(keyword, background_path, music_path, logo_path, affiliate_link, output_name="launchlayer_output.mp4"):
    try:
        script = expand_keyword_to_script(keyword)
        title = generate_title(script, keyword)
        description = generate_description(keyword, script, affiliate_link)

        voice_path = generate_voiceover(script)
        overlays = generate_text_images(script, duration=AudioDuration(voice_path))

        output_path = os.path.join(tempfile.gettempdir(), output_name)
        render_final_video(
            background_path=background_path,
            overlays=overlays,
            voice_path=voice_path,
            music_path=music_path,
            logo_path=logo_path,
            output_path=output_path
        )

        return output_path, keyword, title, description

    except Exception as e:
        import streamlit as st
        st.error(f"🔥 Video Generation Error: {str(e)}")
        raise e  # will show full traceback
        
    finally:
        gc.collect()

def AudioDuration(path):
    from moviepy.editor import AudioFileClip
    return AudioFileClip(path).duration

