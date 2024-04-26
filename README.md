# MusicMixer

MusicMixer is a tool I designed to augment music datasets -- specifically, I was working on [song2tab](https://github.com/c0nD/song2tab). It provides a simple web interface to apply a variety of audio effects to songs, creating an enriched dataset that can be used to improve the performance of the song2tab or any audio-based/music-based deep learning model.

## Features
- **Audio File Conversion**: Convert audio files into different formats for compatibility with various machine learning tools and libraries.
- **Audio Effect Application**: Apply multiple audio effects, such as reverb, delay, distortion, and more, with randomization to create a diverse dataset.
- **Batch Processing**: Upload and process multiple audio files or zip archives simultaneously.
- **Web Interface**: Hosted at [musicmixer.pro](https://musicmixer.pro/), providing an easy-to-use interface for audio processing.
- **Downloadable Results**: Download individual processed files or a zip archive of all processed files.

## Installation

MusicMixer is developed using Python and Flask. To install and run the project locally, you will need [Poetry](https://python-poetry.org/) for dependency management.

### Prerequisites
- Python 3.7 or higher
- Poetry

### Setup
First, clone the repository from GitHub:
```bash
git clone https://github.com/c0nD/MusicMixer
cd song2tab
```
Next, use Poetry to install the dependencies (from the root dir):
```bash
poetry install
```

Running the `app.py` file and going to the specified local-host URL will allow you to use the web interface.


## Licensing
This project is licensed under the [MIT License](https://github.com/c0nD/MusicMixer/blob/main/LICENSE). Please check the link for further information.
