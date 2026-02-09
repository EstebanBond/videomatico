import os
from moviepy import VideoFileClip, TextClip, ImageClip, ColorClip, CompositeVideoClip


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOCAL_FONT = os.path.join(BASE_DIR, "assets", "fonts", "arial.ttf")

def create_lsm_video(word: str, input_path: str, output_path: str):
    W, H = 1080, 1920
    
    # Clip base
    clip = VideoFileClip(input_path).resized(width=W) # En v2.0 es .resized()
    
    # Fondos
    top_bar = ColorClip(size=(W, 300), color=(255, 255, 255)).with_duration(clip.duration)
    bottom_bar = ColorClip(size=(W, 300), color=(255, 255, 255)).with_duration(clip.duration)
    
    # Logo
    logo = (ImageClip("assets/logos/FirmaSikno_Blanca.png")
            .resized(height=150)
            .with_position(('center', 75))
            .with_duration(clip.duration))
    
    # Texto (Requiere ImageMagick instalado en el sistema)
    txt = (TextClip(text=word, font_size=120, color='black', font=LOCAL_FONT)
            .with_position(('center', H - 225))
            .with_duration(clip.duration))
    
    # Composición final
    final = CompositeVideoClip([
        ColorClip(size=(W, H), color=(50, 50, 50)).with_duration(clip.duration),
        top_bar.with_position((0, 0)),
        bottom_bar.with_position((0, H - 300)),
        clip.with_position('center'),
        logo,
        txt
    ], size=(W, H))
    
    final.write_videofile(output_path, fps=30, codec="libx264")
    return output_path