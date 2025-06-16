# Archivo Python que contiene las funciones de inferencia para los modelos de generación, tanto de texto como de audio.

# Se importan las librerías necesarias.
from transformers import GPT2LMHeadModel, GPT2TokenizerFast # Librerías de transformers para el modelo de lenguaje.
from audiocraft.models import MusicGen # Librería de audiocraft para el modelo de audio.
from audiocraft.data.audio import audio_write # Librería de audiocraft para escribir audio.
import torch # Librería de PyTorch para el manejo de tensores.


# Función para cargar el modelo preentrenado de GPT-2 y su tokenizador.
# Esta función toma como argumento la ruta del modelo y devuelve el tokenizador y el modelo cargados.
def load_model(model_path):
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2-medium")
    tokenizer.pad_token = tokenizer.eos_token
    model = GPT2LMHeadModel.from_pretrained(model_path)
    model.eval()
    return tokenizer, model

# Función de inferencia para el modelo de GPT-2.
# Esta función toma como argumento un prompt de texto, el tokenizador y el modelo, y devuelve la letra generada.
def generate_lyrics(prompt, tokenizer, model, max_length=200):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True)
    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]

    with torch.no_grad():
        outputs = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_length=max_length,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.convert_tokens_to_ids("<|endoflyric|>"),
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=1.0,
        )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Carga del modelo de audio.
# musicgen_model = MusicGen.get_pretrained("melody")
# musicgen_model.set_generation_params(duration=60)  # puedes ajustar duración

# # Función de inferencia para el modelo de audio.
# def generate_music_from_lyrics(lyrics, filename="output_song"):
#     prompt = lyrics.strip().replace("\n", " ")  # convertir versos a frase
#     waveform = musicgen_model.generate([prompt])
#     path = audio_write(filename, waveform[0].cpu(), musicgen_model.sample_rate, format="mp3")
#     return path