from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, after_this_request
import os
from werkzeug.utils import secure_filename
import zipfile
from effects_processor import EffectsProcessor
import uuid
import shutil

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed_audio'
app.config['SECRET_KEY'] = 'your_secret_key'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    files = request.files.getlist('file')
    processed_files = []

    batch_folder = os.path.join(app.config['UPLOAD_FOLDER'], "batch_" + uuid.uuid4().hex)
    os.makedirs(batch_folder, exist_ok=True)

    input_paths = []

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(batch_folder, filename)
            file.save(file_path)
            input_paths.append(file_path)

    if len(input_paths) == 1:
        process_path = input_paths[0]
    else:
        zip_path = os.path.join(batch_folder, "audio_files.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file_path in input_paths:
                zipf.write(file_path, os.path.basename(file_path))
        process_path = zip_path

    try:
        processor = EffectsProcessor(process_path, app.config['PROCESSED_FOLDER'])
        processor.process()
    except Exception as e:
        flash(f"An error occurred during processing: {e}")
        return redirect(request.url)

    zip_file = "processed_files.zip"
    zip_path = os.path.join(app.config['PROCESSED_FOLDER'], zip_file)
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in os.listdir(app.config['PROCESSED_FOLDER']):
            if file != zip_file:  # Avoid including the zip file itself
                file_path = os.path.join(app.config['PROCESSED_FOLDER'], file)
                zipf.write(file_path, file)

    processed_files = [f for f in os.listdir(app.config['PROCESSED_FOLDER']) if f != zip_file]
    processed_files.insert(0, zip_file)

    return render_template('process.html', files=processed_files)


@app.route('/downloads/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
    response = send_from_directory(app.config['PROCESSED_FOLDER'], filename, as_attachment=True)
    
    @after_this_request
    def cleanup(response):
        def remove_file(path):
            try:
                os.remove(path)
            except OSError as e:
                app.logger.error(f"Error removing file {path}: {e}")

        if filename == 'processed_files.zip':
            zip_file_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
            remove_file(zip_file_path)

            for f in os.listdir(app.config['PROCESSED_FOLDER']):
                file_path = os.path.join(app.config['PROCESSED_FOLDER'], f)
                if os.path.isfile(file_path) and f != filename:
                    remove_file(file_path)

        return response
    
    return response


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'wav', 'mp3', 'ogg', 'zip'}


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
