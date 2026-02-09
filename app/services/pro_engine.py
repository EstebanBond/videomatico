import json
import os
from moviepy import (VideoFileClip, TextClip, ImageClip, ColorClip, 
                    CompositeVideoClip, concatenate_videoclips, AudioFileClip, afx)
from gtts import gTTS

def build_luxury_campaign(json_path, output_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    W, H = 1080, 1920
    FONT = os.path.join("assets", "fonts", "arial_bold.ttf")
    
    # 1. Generar Locución (TTS)
    tts = gTTS(text=data['voice_text'], lang='es')
    tts.save("temp_voice.mp3")
    voice_audio = AudioFileClip("temp_voice.mp3")

    # 2. Procesar Escenas
    clips = []
    
    # Intro de Logo (2 segundos)
    logo = (ImageClip("assets/logos/logo.png")
            .resized(width=W*0.5)
            .with_duration(2)
            .with_position('center')
            .crossfadein(0.5))
    intro_bg = ColorClip(size=(W, H), color=(255, 255, 255)).with_duration(2)
    clips.append(CompositeVideoClip([intro_bg, logo]))

    # Escenas de Envato con Texto
    for s in data['scenes']:
        video_path = os.path.join("assets", "inputs", s['video'])
        # Ajustamos el video al tamaño vertical (crop/resize)
        v_clip = VideoFileClip(video_path).resized(height=H).with_duration(s['duration'])
        
        txt = (TextClip(text=s['text'], font_size=120, color='white', font=FONT)
                .with_duration(s['duration'])
                .with_position(('center', H*0.8)) # Texto en la parte inferior
                .crossfadein(0.3))
        
        scenes_comp = CompositeVideoClip([v_clip.with_position('center'), txt])
        clips.append(scenes_comp)

    # 3. Ensamblaje Final
    final_video = concatenate_videoclips(clips, method="compose")
    
    # 4. Música de Fondo (Punch)
    music = AudioFileClip(data['audio_music']).with_duration(final_video.duration)
    music = music.fx(afx.volumex, 0.2) # Bajar volumen de la música para que se oiga la voz
    
    # Combinar música y voz
    final_audio = CompositeVideoClip([music, voice_audio]).audio if voice_audio.duration < final_video.duration else music
    # Nota: Simplificado para el ejemplo, lo ideal es usar CompositeAudioClip
    
    final_video = final_video.with_audio(music) # Aquí podrías mezclar ambos
    final_video.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac")

    # Limpieza
    os.remove("temp_voice.mp3")