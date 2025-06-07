import tempfile
from pathlib import Path
from PIL import Image as PILImage, ImageDraw, ImageFont
from generator.launchlayer_video.utils import split_sentences, wrap_text

RESOLUTION = (1920, 1080)
FONT_PATH = "generator/launchlayer_video/assets/Montserrat-Bold.ttf"
TEXT_COLOR = "white"
FONT_SIZE = 100

def generate_text_images(script_text, duration):
    sentences = split_sentences(script_text)
    word_counts = [len(s.split()) for s in sentences]
    durations = [(w / sum(word_counts)) * duration for w in word_counts]

    overlays = []
    for sentence, dur in zip(sentences, durations):
        max_width = RESOLUTION[0] - 120
        font_size = FONT_SIZE

        while True:
            font = ImageFont.truetype(FONT_PATH, font_size)
            wrapped = wrap_text(sentence, font, max_width)
            draw = ImageDraw.Draw(PILImage.new("RGBA", RESOLUTION))
            bbox = draw.textbbox((0, 0), wrapped, font=font)
            if bbox[2] <= max_width and bbox[3] <= RESOLUTION[1] - 100:
                break
            font_size -= 2

        img = PILImage.new("RGBA", RESOLUTION, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        x = (RESOLUTION[0] - bbox[2]) // 2
        y = (RESOLUTION[1] - bbox[3]) // 2
        draw.text((x + 2, y + 2), wrapped, font=font, fill="black")  # shadow
        draw.text((x, y), wrapped, font=font, fill=TEXT_COLOR)

        path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
        img.save(path)
        overlays.append((path, dur))

    return overlays  # list of (image_path, duration)

