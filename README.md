# LAILA
Using DeepLearning methods to generate music based on prompts introduced by users. 
This is my student final project for the AI & Big Data Master's Degree.

The goal of the project is to make easier the creation process of music. Natural Language Processing is in charge of generate lyrics according to a prompt, and AudioCraft(MusicGen) is the one who will produce a melody based on the previous lyric.

## Requirements

### 🖥️ Hardware Requirements

As mentioned before, the project won't have money invested. The project is heavy dependent on good hardware resources to work decently. Personally, I own a middle-tier computer with the following features:

- **GPU:** NVIDIA RTX 3060 12 GB VRAM with CUDA Support (Minimum 8GB, Recommended 16GB).
- **RAM:** 16GB (Minimum).
- **CPU**: AMD Ryzen 7 5800X (Could work with CPUs less powerful)
- **Storage:** At least 30 GB of free space to models, datasets and generated audios.

The audio generation part needs more resources to work faster, but with this resources can be a good beggining.

### 🧰 Software Requirements

- 🔧 **Environment**

     **OS:** Windows 11. (Could work on Windows 10 or Linux)

     **Virtual Environment:** I used Conda. (The environment will be uploaded).

     **IDE:** Visual Studio Code

- 📦 **Frameworks & Libraries**

Most parts of the project are developed using Python and it's libraries. The main libraries will be listed below:

    
    Transformers: (HuggingFace): NLP generation model.
    datasets: For fine-tuning methods.
    torch: Training models.
    audiocraft: Producing melodies with MusicGen.
    Flask: Web UI of the project.
    scikit-learn, matplotlib, pandas, seaborn: For data test, manipulation and visualization.

### Dataset 
- **Lyrics Dataset:** Lyrics from the music web Genius. *sebastiandizon/genius-song-lyrics* (From Hugging Face).
- **Language filter:** Only using english songs.
- **Genre filter:** Originally, it will work only with 3 music genres: Rock, Pop and Rap. This filter is stablished in order to improve the NLP models perfomances.

## Usage/Examples

    **environment_route\python.exe** UI/app.py (Full version)

    **environment_route\python.exe** UI/app_v0.py (Only the Lyrics Generator part)

Then go to 127.0.0.1/5000 on a navigator.

## Authors

- [@alegonzjur](https://www.github.com/alegonzjur)

For more information about the project, check the project documentation on the docs folder.

