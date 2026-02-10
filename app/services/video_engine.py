import os
from moviepy import TextClip, ImageClip, ColorClip, CompositeVideoClip, AudioFileClip, concatenate_videoclips

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOCAL_FONT = os.path.join(BASE_DIR, "assets", "fonts", "arial.ttf")
LOGO_PATH = os.path.join(BASE_DIR, "assets", "logos", "FirmaSikno_Blanca.png")

def build_esentia_engine(project_data, image_paths, audio_path, output_path):
    """
    Ensambla un video premium con validación estricta de activos.
    """
    W, H = 1080, 1920
    
    # 1. Validación de Audio (Culpable principal del startswith)
    if not audio_path or not isinstance(audio_path, str):
        raise ValueError(f"Ruta de audio inválida: {audio_path}")
    
    audio = AudioFileClip(audio_path)
    total_duration = audio.duration
    
    # 2. Filtrado y creación de clips de imagen
    # Eliminamos cualquier None que se haya colado en la lista
    valid_image_paths = [p for p in image_paths if p and isinstance(p, str) and os.path.exists(p)]
    
    if not valid_image_paths:
        raise ValueError("No se encontraron imágenes válidas para procesar.")
        
    duration_per_clip = total_duration / len(valid_image_paths)
    
    clips = []
    for img_path in valid_image_paths:
        img_clip = (ImageClip(img_path)
                    .resized(width=W)
                    .with_duration(duration_per_clip))
        clips.append(img_clip)
    
    video_base = concatenate_videoclips(clips, method="compose")
    
    # 3. Elementos estéticos de marca
    top_bar = ColorClip(size=(W, 300), color=(255, 255, 255)).with_duration(total_duration)
    bottom_bar = ColorClip(size=(W, 300), color=(255, 255, 255)).with_duration(total_duration)
    
    # Logo con validación de existencia
    if os.path.exists(LOGO_PATH):
        logo = (ImageClip(LOGO_PATH)
                .resized(height=150)
                .with_position(('center', 75))
                .with_duration(total_duration))
    else:
        print(f"⚠️ Logo no encontrado en {LOGO_PATH}. Continuando sin logo.")
        logo = ColorClip(size=(1,1), color=(0,0,0,0)).with_duration(total_duration)
    
    # Texto: Manejo robusto de errores
    try:
        brand_text = getattr(project_data, 'brand_name', 'ESENTIA') or 'ESENTIA'
        txt = (TextClip(text=brand_text.upper(), font_size=120, color='black', font=LOCAL_FONT)
                .with_position(('center', H - 225))
                .with_duration(total_duration))
    except Exception as e:
        print(f"⚠️ Error en fuente/texto: {e}. Usando configuración básica.")
        txt = (TextClip(text="ESENTIA", font_size=100, color='white')
                .with_position(('center', H - 225))
                .with_duration(total_duration))
    
    # 4. Composición final
    final = CompositeVideoClip([
        ColorClip(size=(W, H), color=(50, 50, 50)).with_duration(total_duration),
        top_bar.with_position((0, 0)),
        bottom_bar.with_position((0, H - 300)),
        video_base.with_position('center'),
        logo,
        txt # El texto ya tiene duración y posición
    ], size=(W, H))
    
    # 5. Sincronizar audio y exportar
    final = final.with_audio(audio)
    
    print(f"🎬 Renderizando video final en: {output_path}")

    final.write_videofile(
        output_path, 
        fps=24, 
        codec="libx264", 
        audio_codec="aac",
        temp_audiofile="temp-audio.m4a",
        remove_temp=True,
        pixel_format="yuv420p" 
)
    
    # Limpieza de memoria (Previene errores de FFMPEG_AudioReader)
    audio.close()
    final.close()
    
    return output_path