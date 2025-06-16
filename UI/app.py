from flask import Flask, render_template, request, redirect, url_for

# Asegura que se incluya el directorio raíz del proyecto (LAILA)
import sys 
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from IA.inference import load_model, generate_lyrics
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
import torch
import uuid

app = Flask(__name__)

# Asegúrate de que estos directorios existen
os.makedirs("static/audio", exist_ok=True)
os.makedirs("static/lyrics", exist_ok=True)

# Cargar modelos y tokenizadores una sola vez
tokenizer_rock, model_rock = load_model("IA/lyrics_generator_rock/checkpoint-1000")
tokenizer_pop, model_pop = load_model("IA/lyrics_generator_pop/checkpoint-1000")
tokenizer_rap, model_rap = load_model("IA/lyrics_generator_rap/checkpoint-1000")

# MusicGen
musicgen_model = MusicGen.get_pretrained("melody")
musicgen_model.set_generation_params(duration=5) # puedes ajustar duración

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/genero")
def index():
    return render_template("index.html")

@app.route("/rock", methods=["GET", "POST"])
def rock():
    title = ""
    artist = ""
    lyrics_prompt = ""
    generated = ""
    audio_path = None

    if request.method == "POST":
        action = request.form.get("action")

        if action == "new":
            return render_template("rock.html")

        title = request.form.get("title")
        artist = request.form.get("artist")
        lyrics_prompt = request.form.get("lyrics_prompt")

        if action in ["repeat", "continue"]:
            full_prompt = f"Title: {title}\nArtist: {artist}\nLyrics: {lyrics_prompt}"
            output = generate_lyrics(full_prompt, tokenizer_rock, model_rock)
            generated = output.replace(full_prompt, "").strip()

        if action == "continue" and generated:
            prompt_for_music = f"A song in the style of {artist} with lyrics: {generated}"
            waveform = musicgen_model.generate([prompt_for_music])
            audio_path = audio_write("static/audio/rock_sample", waveform[0].cpu(), musicgen_model.sample_rate, format="mp3")

    return render_template("rock.html", title=title, artist=artist,
                           lyrics_prompt=lyrics_prompt, generated=generated,
                           audio_path=audio_path)

@app.route("/pop", methods=["GET", "POST"])
def pop():
    if request.method == "POST":
        action = request.form.get("action")
        title = request.form.get("title", "")
        artist = request.form.get("artist", "")
        prompt = request.form.get("lyrics_prompt", "")

        if action == "repeat":
            generated = generate_lyrics(prompt, tokenizer_pop, model_pop)
            return render_template("pop.html", title=title, artist=artist, lyrics_prompt=prompt, generated=generated)

        elif action == "new":
            return redirect(url_for("pop"))

        elif action == "continue":
            # Redirige a la ruta correspondiente cuando implementes la funcionalidad de música
            return redirect(url_for("melody"))

    return render_template("pop.html")

@app.route("/rap", methods=["GET", "POST"])
def rap():
    if request.method == "POST":
        action = request.form.get("action")
        title = request.form.get("title", "")
        artist = request.form.get("artist", "")
        prompt = request.form.get("lyrics_prompt", "")

        if action == "repeat":
            generated = generate_lyrics(prompt, tokenizer_rap, model_rap)
            return render_template("rock.html", title=title, artist=artist, lyrics_prompt=prompt, generated=generated)

        elif action == "new":
            return redirect(url_for("rap"))

        elif action == "continue":
            # Redirige a la ruta correspondiente cuando implementes la funcionalidad de música
            return redirect(url_for("melody"))

    return render_template("rap.html")

@app.route('/final', methods=['POST'])
def final_page():
    title = request.form.get("title")
    artist = request.form.get("artist")
    lyrics = request.form.get("lyrics")

    prompt = lyrics
    musicgen_model.set_generation_params(duration=5)
    waveform = musicgen_model.generate([prompt])

    audio_file = f"{uuid.uuid4().hex}.mp3"
    audio_path = os.path.join("static", "audio", audio_file)
    audio_write(audio_path[:-4], waveform[0].cpu(), musicgen_model.sample_rate, format="mp3")

    lyrics_file = audio_file.replace(".mp3", ".txt")
    lyrics_path = os.path.join("static", "lyrics", lyrics_file)
    with open(lyrics_path, "w", encoding="utf-8") as f:
        f.write(lyrics)

    return render_template("final.html", title=title, artist=artist, lyrics=lyrics,
                           audio_file=audio_file, lyrics_file=lyrics_file)

if __name__ == '__main__':
    app.run(debug=True)