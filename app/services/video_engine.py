import os
from moviepy import TextClip, ImageClip, ColorClip, CompositeVideoClip, AudioFileClip, concatenate_videoclips

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOCAL_FONT = os.path.join(BASE_DIR, "assets", "fonts", "arial.ttf")
LOGO_PATH = os.path.join(BASE_DIR, "assets", "logos", "FirmaSikno_Blanca.png")

def build_esentia_engine(project_data, image_paths, audio_path, output_path):
    """
    Ensambla un video premium a partir de imágenes generadas y una locución.
    """
    W, H = 1080, 1920
    
    # 1. Cargar el audio para determinar la duración total
    audio = AudioFileClip(audio_path)
    total_duration = audio.duration
    duration_per_clip = total_duration / len(image_paths)
    
    # 2. Crear clips de imagen a partir de la lista de rutas
    clips = []
    for img_path in image_paths:
        # Redimensionamos cada imagen para que llene el ancho
        img_clip = (ImageClip(img_path)
                    .resized(width=W)
                    .with_duration(duration_per_clip))
        clips.append(img_clip)
    
    # Concatenamos la secuencia de imágenes
    video_base = concatenate_videoclips(clips, method="compose")
    
    # 3. Elementos estéticos de marca (Tu diseño original)
    top_bar = ColorClip(size=(W, 300), color=(255, 255, 255)).with_duration(total_duration)
    bottom_bar = ColorClip(size=(W, 300), color=(255, 255, 255)).with_duration(total_duration)
    
    # Logo
    logo = (ImageClip(LOGO_PATH)
            .resized(height=150)
            .with_position(('center', 75))
            .with_duration(total_duration))
    
    # Texto: Usamos el nombre de la marca definido por el Agente Creativo
    brand_word = project_data.brand_name.upper()
    txt = (TextClip(text=brand_word, font_size=120, color='black', font=LOCAL_FONT)
            .with_position(('center', H - 225))
            .with_duration(total_duration))
    
    # 4. Composición final
    final = CompositeVideoClip([
        # Fondo oscuro para rellenar huecos
        ColorClip(size=(W, H), color=(50, 50, 50)).with_duration(total_duration),
        top_bar.with_position((0, 0)),
        bottom_bar.with_position((0, H - 300)),
        video_base.with_position('center'),
        logo,
        txt
    ], size=(W, H))
    
    # 5. Sincronizar audio y exportar
    final = final.with_audio(audio)
    
    print(f"🚀 Renderizando video final: {output_path}")
    final.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
    
    return output_path