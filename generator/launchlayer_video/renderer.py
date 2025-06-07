import os
import numpy as np
from pathlib import Path
from PIL import Image as PILImage
from moviepy.editor import (
    VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip,
    CompositeAudioClip, ColorClip
)
from moviepy.video.fx.all import blackwhite

# === ANTIALIAS PATCH ===
if not hasattr(PILImage, 'ANTIALIAS'):
    PILImage.ANTIALIAS = PILImage.Resampling.LANCZOS

RESOLUTION = (1920, 1080)

def generate_background_clip(video_path, duration):
    clip = VideoFileClip(video_path).without_audio().fx(blackwhite)

    def resize_frame(frame):
        img = PILImage.fromarray(frame)
        return np.array(img.resize(RESOLUTION, PILImage.ANTIALIAS))

    resized = clip.fl_image(resize_frame).loop(duration=duration).set_duration(duration)
    overlay = ColorClip(size=RESOLUTION, color=(0, 0, 0)).set_opacity(0.4).set_duration(duration)
    return CompositeVideoClip([resized, overlay])

def mix_audio_layers(voice_path, music_path, duration):
    voice = AudioFileClip(voice_path).volumex(1.0).audio_fadein(0.5)

    music = AudioFileClip(music_path)\
        .volumex(0.1)\
        .audio_fadein(0.5)\
        .audio_fadeout(3)\
        .set_duration(duration + 3)

    return CompositeAudioClip([music, voice])

def render_final_video(background_path, overlays, voice_path, music_path, logo_path, output_path):
    voice = AudioFileClip(voice_path)
    duration = voice.duration
    total_duration = duration + 3

    bg = generate_background_clip(background_path, total_duration)

    text_clips = []
    start_time = 0
    for path, dur in overlays:
        text_clips.append(
            ImageClip(path)
            .set_duration(dur)
            .set_start(start_time)
            .set_position("center")
        )
        start_time += dur

    audio = mix_audio_layers(voice_path, music_path, duration).set_duration(total_duration)

    logo = (
        ImageClip(logo_path)
        .set_duration(3)
        .set_start(duration)
        .resize(height=200)
        .set_position("center")
        .fadein(0.5)
    )

    final = CompositeVideoClip([bg, *text_clips, logo], size=RESOLUTION).set_audio(audio)

    final.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        fps=30,
        threads=2,
        preset="ultrafast",
        verbose=False
    )

    final.close()
    voice.close()
    for c in text_clips:
        c.close()

    return output_path


