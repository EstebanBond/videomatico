import os
from moviepy import TextClip, ImageClip, ColorClip, CompositeVideoClip, AudioFileClip, concatenate_videoclips, vfx
from moviepy.audio.AudioClip import CompositeAudioClip

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FONT_BOLD = os.path.join(BASE_DIR, "assets", "fonts", "Montserrat-Bold.ttf")
FONT_LIGHT = os.path.join(BASE_DIR, "assets", "fonts", "Montserrat-Light.ttf")
LOGO_PATH = os.path.join(BASE_DIR, "assets", "logos", "esentia.png")
BG_MUSIC = os.path.join(BASE_DIR, "assets", "audio", "background_music.mp3")

def build_esentia_engine(project_data, image_paths, audio_path, output_path):
    # 1. Configuración de Lienzo 720p
    W, H = 720, 1280
    
    voice_audio = AudioFileClip(audio_path)
    total_duration = voice_audio.duration

    # Filtramos paths nulos (por si DALL-E bloqueó algo)
    valid_images = [p for p in image_paths if p is not None]
    if not valid_images:
        raise ValueError("No hay imágenes válidas para procesar")

    duration_per_clip = total_duration / len(image_paths)
    
    clips = []
    for i, img_path in enumerate(image_paths):
        # Extraemos la keyword generada por Gemini
        keyword = project_data.scenes[i].overlay_text if i < len(project_data.scenes) else "ESENTIA"
        
        # --- EFECTO KEN BURNS (ZOOM SUAVE) ---
        # Definimos una función de redimensionado que crece un 10% durante la escena
        img_clip = (ImageClip(img_path)
                            .resized(height=H)
                            .with_position('center')
                            .resized(lambda t: 1 + 0.04 * t)
                            .with_duration(duration_per_clip)
                            .with_effects([vfx.FadeIn(0.5), vfx.FadeOut(0.5)]))

        # --- POWER WORD (SUBTÍTULO LUXURY) ---
        txt_word = (TextClip(
                                text=keyword.upper(), 
                                font_size=80, 
                                color='white', 
                                font=FONT_LIGHT,
                                size=(W, None) # Centrado automático por ancho
                            )
                            .with_position(('center', H * 0.70))
                            .with_duration(duration_per_clip)
                            .with_effects([vfx.FadeIn(0.5), vfx.FadeOut(0.5)]))
        
        # Montamos la escena
        scene_combined = CompositeVideoClip([img_clip, txt_word], size=(W, H))
        clips.append(scene_combined)
    
    video_base = concatenate_videoclips(clips, method="compose")
    
# --- 2. MEZCLA DE AUDIO (Locución + Música de Envato) ---
    print(f"🎵 Buscando música en: {BG_MUSIC}")
    
    if os.path.exists(BG_MUSIC):
        print("✅ Música encontrada. Mezclando pistas...")
        try:
            # Cargamos la música
            bg_audio = AudioFileClip(BG_MUSIC)
            
            # Ajustes pro:
            # 1. Subimos volumen al 25% (0.25) para que se note
            # 2. La hacemos loopear si es más corta que el video
            # 3. La cortamos exactamente a la duración del video
            bg_audio = (bg_audio
                        .with_volume_scaled(0.25) 
                        .with_duration(total_duration)) 
            
            # Mezclamos locución + música
            final_audio = CompositeAudioClip([voice_audio, bg_audio])
            print("🔊 Audio compuesto exitosamente.")
        except Exception as e:
            print(f"⚠️ Error procesando la música: {e}")
            final_audio = voice_audio
    else:
        print(f"❌ ADVERTENCIA: No se encontró música en {BG_MUSIC}. Usando solo voz.")
        final_audio = voice_audio

    # 3. Logo en posición baja (Safe Area)
    logo = (ImageClip(LOGO_PATH)
            .resized(height=90)
            .with_position(('center', H - 160))
            .with_duration(total_duration)
            .with_start(0)
            )
    
    # 4. Composición y Exportación Final
    final_video = CompositeVideoClip([
        video_base,
        logo
    ], size=(W, H)).with_audio(final_audio)
    
    print(f"🚀 Renderizando versión cinematográfica de Esentia...")
    final_video.write_videofile(
        output_path, 
        fps=24, 
        codec="libx264", 
        audio_codec="aac",
        bitrate="5000k", # 6Mbps en 720p buena calidad
        pixel_format="yuv420p"
    )
    
    # Liberar memoria de audio
    voice_audio.close()
    if os.path.exists(BG_MUSIC): bg_audio.close()
    
    return output_path