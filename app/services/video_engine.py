import os
import numpy as np
from moviepy import TextClip, ImageClip, ColorClip, CompositeVideoClip, AudioFileClip, concatenate_videoclips, vfx, afx
from moviepy.audio.AudioClip import CompositeAudioClip

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FONT_BOLD = os.path.join(BASE_DIR, "assets", "fonts", "Montserrat-Bold.ttf")
FONT_LIGHT = os.path.join(BASE_DIR, "assets", "fonts", "Montserrat-Light.ttf")
LOGO_PATH = os.path.join(BASE_DIR, "assets", "logos", "esentia.png")
BG_MUSIC = os.path.join(BASE_DIR, "assets", "audio", "background_music.mp3")

def build_esentia_engine(project_data, image_paths, audio_path, output_path):
    W, H = 720, 1280
    
    # 1. CARGA DE AUDIO Y CÁLCULO DE TIEMPOS
    voice_audio = AudioFileClip(audio_path)
    voice_duration = voice_audio.duration
    tiempo_extra_final = 2.5 

    # IMPORTANTE: La duración se divide entre el total de escenas planeadas
    # para mantener la sincronía con la locución, incluso si alguna imagen falla.
    total_escenas = len(image_paths)
    duracion_base_por_clip = voice_duration / total_escenas

    # --- FUNCIÓN AUXILIAR PARA EL DEGRADADO SUPERIOR ---
    def crear_degradado_top(ancho, alto_barra):
        imagen_rgba = np.zeros((alto_barra, ancho, 4), dtype=np.uint8)
        alpha_vertical = np.linspace(255, 0, alto_barra, dtype=np.uint8)
        imagen_rgba[:, :, 3] = alpha_vertical[:, np.newaxis]
        return ImageClip(imagen_rgba).with_position(('center', 'top'))

    # 2. CONSTRUCCIÓN DE ESCENAS
    clips = []
    
    # Inicializamos el respaldo con el logo por si falla la primera imagen
    ultima_imagen_valida = LOGO_PATH if os.path.exists(LOGO_PATH) else None

    # Iteramos sobre image_paths (incluye los Nones de DALL-E)
    for i, img_path in enumerate(image_paths):
        keyword = project_data.scenes[i].overlay_text if i < len(project_data.scenes) else "ESENTIA"

        # --- LÓGICA DE RESPALDO ---
        if img_path is not None:
            img_to_use = img_path
            ultima_imagen_valida = img_path # Guardamos esta como la nueva "última buena"
        else:
            print(f"⚠️ Reutilizando imagen para escena {i+1} por bloqueo de filtro.")
            img_to_use = ultima_imagen_valida

        # Tiempo dinámico: la última escena dura más
        duracion_actual = duracion_base_por_clip
        if i == total_escenas - 1:
            duracion_actual += tiempo_extra_final
        
        # Clip de Imagen (Efecto Ken Burns) con la imagen resuelta (img_to_use)
        img_clip = (ImageClip(img_to_use)
                    .resized(height=H)
                    .with_position('center')
                    .resized(lambda t: 1 + 0.04 * t)
                    .with_duration(duracion_actual)
                    .with_effects([vfx.FadeIn(0.5), vfx.FadeOut(0.5)]))

        # Power Word (Ajuste de tamaño dinámico)
        palabra = keyword.upper()
        tamanio_fuente = 70
        if len(palabra) > 10: tamanio_fuente = 55
        elif len(palabra) > 7: tamanio_fuente = 65

        txt_word = (TextClip(
                            text=palabra, 
                            font_size=tamanio_fuente, 
                            color='white', 
                            font=FONT_LIGHT,
                            size=(int(W * 0.8), int(tamanio_fuente * 1.4)),
                            text_align='center'
                        )
                        # Mantenemos la posición centrada
                        .with_position(('center', int(H * 0.65))) 
                        .with_duration(duracion_actual)
                        .with_effects([
                            vfx.FadeIn(0.5), 
                            vfx.FadeOut(0.5)
                        ]))
        
        scene_combined = CompositeVideoClip([img_clip, txt_word], size=(W, H))
        clips.append(scene_combined)
    
    video_base = concatenate_videoclips(clips, method="compose")
    total_video_duration = video_base.duration 
    
    # 3. MEZCLA DE AUDIO CON FADE OUT
    if os.path.exists(BG_MUSIC):
        bg_audio = (AudioFileClip(BG_MUSIC)
                    .with_volume_scaled(0.25) 
                    .with_duration(total_video_duration))
        final_audio = CompositeAudioClip([voice_audio, bg_audio])
        final_audio = final_audio.with_effects([afx.AudioFadeOut(2)])
    else:
        final_audio = voice_audio.with_effects([afx.AudioFadeOut(1)])

    # 4. CAPAS ESTÁTICAS (DEGRADADO Y LOGO ARRIBA)
    gradiente_top = (crear_degradado_top(W, 400)
                        .with_duration(total_video_duration))

    logo = None
    if os.path.exists(LOGO_PATH):
            logo = (ImageClip(LOGO_PATH)
                    .resized(height=90)
                    .with_position(('center', 40)) 
                    .with_duration(total_video_duration)
                    .with_start(0)
                    .with_effects([
                        vfx.FadeIn(1.5), 
                        vfx.FadeOut(1.5)
                    ]))
                    
    # 5. COMPOSICIÓN FINAL
    layers = [video_base, gradiente_top]
    if logo: layers.append(logo)

    final_video = CompositeVideoClip(layers, size=(W, H)).with_audio(final_audio)
    
    print(f"🚀 Renderizando versión cinematográfica...")
    final_video.write_videofile(
        output_path, 
        fps=24, 
        codec="libx264", 
        audio_codec="aac",
        bitrate="5000k",
        pixel_format="yuv420p"
    )
    
    voice_audio.close()
    if os.path.exists(BG_MUSIC): bg_audio.close()
    
    return output_path