from flask import Flask, Response
import os

app = Flask(__name__)

# Define the path to your large video file
video_path = 'static/SteinsGate_-_S01E01.mkv'

# Chunk size in bytes (adjust as needed)
chunk_size = 1024 * 1024  # 1MB chunks

@app.route('/video_stream')
def video_stream():
    def generate():
        with open(video_path, 'rb') as video_file:
            while True:
                data = video_file.read(chunk_size)
                if not data:
                    break
                yield data

    return Response(generate(), mimetype='video/mkv')

if __name__ == '__main__':
    app.run(debug=True)
 