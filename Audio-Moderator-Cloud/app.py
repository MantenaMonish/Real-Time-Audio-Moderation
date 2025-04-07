from flask import Flask, render_template_string, request
from threading import Thread
import os
import time
from tagger import process_audio
from pyngrok import conf, ngrok

app = Flask(__name__)
WATCH_FOLDER = os.path.join('data', 'WatchAudio')
SUPPORTED_FORMATS = ('.mp3', '.wav', '.flac')
processed_files = set()
results = []

def watch_folder():
    os.makedirs(WATCH_FOLDER, exist_ok=True)
    print(f"Watching folder: {WATCH_FOLDER}")
    while True:
        for fname in os.listdir(WATCH_FOLDER):
            if fname.endswith(SUPPORTED_FORMATS) and fname not in processed_files:
                path = os.path.join(WATCH_FOLDER, fname)
                result = process_audio(path)
                results.append({
                    'file': fname,
                    'tag': result["tag"],
                    'transcript': result["transcript"]
                })
                processed_files.add(fname)
        time.sleep(2)

@app.route('/')
def home():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Profanity Tagger</title>
            <style>
                table { width: 100%; border-collapse: collapse; }
                th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
                th { background-color: #f2f2f2; }
                .container { padding: 20px; max-width: 1200px; margin: 0 auto; }
                .upload-form { margin-bottom: 20px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Profanity Tagger</h1>
                <form class="upload-form" action="/upload" method="post" enctype="multipart/form-data">
                    <input type="file" name="file" accept=".mp3,.wav,.flac">
                    <button type="submit">Upload File</button>
                </form>
                <table>
                    <tr><th>File</th><th>Tag</th><th>Transcript</th></tr>
                    {% for item in results %}
                    <tr>
                        <td>{{ item.file }}</td>
                        <td>{{ item.tag }}</td>
                        <td>{{ item.transcript }}</td>
                    </tr>
                    {% endfor %}
                </table>
            </div>
        </body>
        </html>
    ''', results=results)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file uploaded', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file and file.filename.endswith(SUPPORTED_FORMATS):
        file.save(os.path.join(WATCH_FOLDER, file.filename))
        return 'File uploaded successfully', 200
    return 'Invalid file format', 400

if __name__ == "__main__":
    # Get ngrok auth token from environment variable
    conf.get_default().auth_token = os.environ.get('NGROK_AUTH_TOKEN')
    
    Thread(target=watch_folder, daemon=True).start()
    if os.environ.get('USE_NGROK', 'False') == 'True':
        public_url = ngrok.connect(5002, bind_tls=True).public_url
        print(f" * Web UI: {public_url}")
    app.run(host='0.0.0.0', port=5002)
