from flask import Flask, render_template, request, redirect, url_for

# Asegura que se incluya el directorio raíz del proyecto (LAILA)
import sys 
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from IA.inference import load_model, generate_lyrics


app = Flask(__name__)

# Cargar modelos y tokenizadores una sola vez
tokenizer_rock, model_rock = load_model("IA/lyrics_generator_rock/checkpoint-1000")
tokenizer_pop, model_pop = load_model("IA/lyrics_generator_pop/checkpoint-1000")
tokenizer_rap, model_rap = load_model("IA/lyrics_generator_rap/checkpoint-1000")


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/genero")
def index():
    return render_template("index.html")

@app.route("/rock", methods=["GET", "POST"])    
def rock():
    if request.method == "POST":
        action = request.form.get("action")
        title = request.form.get("title", "")
        artist = request.form.get("artist", "")
        prompt = request.form.get("lyrics_prompt", "")

        if action == "repeat":
            generated = generate_lyrics(prompt, tokenizer_rock, model_rock)
            return render_template("rock.html", title=title, artist=artist, lyrics_prompt=prompt, generated=generated)

        elif action == "new":
            return redirect(url_for("rock"))

        elif action == "continue":
            # Redirige a la ruta correspondiente cuando implementes la funcionalidad de música
            return redirect(url_for("melody"))

    return render_template("rock.html")
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

@app.route('/continue_music', methods=['POST'])
def continue_music():
    # Lógica para continuar con la música (implementación futura con MusicGen)
    return render_template('continue_music.html')

if __name__ == '__main__':
    app.run(debug=True)