from flask import Flask, jsonify
import tensorflow as tf
import torch
import cv2

app = Flask(__name__)

@app.route('/', methods=['GET'])
def root():
    return "Server is running!"

@app.route('/tensorflow-gpu', methods=['GET'])
def tensorflow_gpu():
    try:
        if tf.config.experimental.list_physical_devices('GPU'):
            return jsonify({'message': 'TensorFlow GPU is available', 'tensorflow_gpu': True})
        else:
            return jsonify({'message': 'TensorFlow GPU is not available', 'tensorflow_gpu': False})
    except Exception as e:
        return jsonify({'message': 'Error checking TensorFlow GPU availability', 'error': str(e)})

@app.route('/pytorch-gpu', methods=['GET'])
def pytorch_gpu():
    try:
        if torch.cuda.is_available():
            return jsonify({'message': 'PyTorch GPU is available', 'pytorch_gpu': True})
        else:
            return jsonify({'message': 'PyTorch GPU is not available', 'pytorch_gpu': False})
    except Exception as e:
        return jsonify({'message': 'Error checking PyTorch GPU availability', 'error': str(e)})

@app.route('/opencv-gpu', methods=['GET'])
def opencv_gpu():
    try:
        if cv2.cuda.getCudaEnabledDeviceCount() > 0:
            return jsonify({'message': 'OpenCV GPU support is available', 'opencv_gpu': True})
        else:
            return jsonify({'message': 'OpenCV GPU support is not available', 'opencv_gpu': False})
    except Exception as e:
        return jsonify({'message': 'Error checking OpenCV GPU support', 'error': str(e)})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
