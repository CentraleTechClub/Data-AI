import os
import base64
import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

MODEL_PATH = os.path.join('runs', 'classify', 'face_recognition', 'weights', 'best.pt')
CONFIDENCE_THRESHOLD = 0.80

_model = None


def get_model():
    global _model
    if _model is None:
        from ultralytics import YOLO
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
        _model = YOLO(MODEL_PATH)
    return _model


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    
    try:
        data = request.get_json(force=True)
        img_b64 = data['image'].split(',')[1]
        img_bytes = base64.b64decode(img_b64)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        model = get_model()
        results = model(frame, verbose=False)
        probs = results[0].probs
        label = results[0].names[probs.top1]
        conf = float(probs.top1conf)

        return jsonify({
            'label': label,
            'confidence': round(conf, 4),
            'authorized': label == 'owner' and conf >= CONFIDENCE_THRESHOLD,
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/model-stats')
def model_stats():
    import csv
    stats_path = os.path.join('runs', 'classify', 'face_recognition', 'results.csv')
    epochs = []
    try:
        with open(stats_path, newline='') as f:
            for row in csv.DictReader(f):
                epochs.append({
                    'epoch':     int(float(row['epoch'])),
                    'train_loss': round(float(row['train/loss']), 4),
                    'val_loss':   round(float(row['val/loss']), 4),
                    'accuracy':   round(float(row['metrics/accuracy_top1']) * 100, 1),
                })
    except FileNotFoundError:
        return jsonify({'error': 'results.csv not found'}), 404
    return jsonify({
        'model':          'YOLOv8n-cls',
        'epochs':         epochs,
        'total_epochs':   len(epochs),
        'final_accuracy': epochs[-1]['accuracy'] if epochs else 0,
        'final_loss':     epochs[-1]['val_loss']  if epochs else 0,
        'threshold':      CONFIDENCE_THRESHOLD,
    })


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/denied')
def denied():
    return render_template('denied.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
