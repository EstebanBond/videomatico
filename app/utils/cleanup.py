import os
import shutil

def cleanup_assets(image_paths, audio_path):
    """
    Borra los archivos temporales de imagen y audio después del renderizado.
    """
    print("🧹 Iniciando limpieza de recursos temporales...")
    
    # Limpiar imágenes
    for path in image_paths:
        if path and os.path.exists(path):
            try:
                os.remove(path)
                print(f"🗑️ Imagen eliminada: {path}")
            except Exception as e:
                print(f"⚠️ No se pudo borrar {path}: {e}")

    # Limpiar audio
    if audio_path and os.path.exists(audio_path):
        try:
            os.remove(audio_path)
            print(f"🗑️ Audio eliminado: {audio_path}")
        except Exception as e:
            print(f"⚠️ No se pudo borrar el audio: {e}")