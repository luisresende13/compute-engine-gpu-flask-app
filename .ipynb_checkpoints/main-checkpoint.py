import os
from flask import Flask, jsonify, Response, request
import tensorflow as tf
import torch
import cv2
from ultralytics import YOLO

# Load base url
# base_url = os.environ['BASE_URL']
base_url = "https://app.tixxi.rio/outvideo/?KEY=B0914&CODE={}"

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')

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

def generate_frames(video_url, mode='detect', use_gpu=False, frames=None, seconds=None, execution_seconds=None):
    device = 0 if use_gpu else 'cpu'
    print(f'video_url: {video_url}, device: {device}, mode: {mode}')
    
    cap = cv2.VideoCapture(video_url)

    frame_count = 0
    start_time = cv2.getTickCount()
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame_count += 1
        
        if mode == 'track':
            # Run YOLOv8 tracking on the frame, persisting tracks between frames
            results = model.track(frame, persist=True, device=device)
        elif mode == 'detect':
            # Run YOLOv8 detection on the frame, persisting tracks between frames
            results = model.predict(frame, device=device)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()
        # annotated_frame = frame

        # Convert the annotated frame to JPEG format
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame = buffer.tobytes()

        # Yield the frame for streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        elapsed_time = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
        video_duration = frame_count / 3  # Assuming FPS is 3 (adjust accordingly)
        
        # Check conditions for stopping processing
        if frames is not None and frame_count >= frames:
            break
        
        if seconds is not None and video_duration >= seconds:
            break

        if execution_seconds is not None and elapsed_time >= execution_seconds:
            break
    
    # Release the video capture object
    cap.release()

@app.route('/track/<int:code>')
def video_stream(code):
    video_url = base_url.format(code)
    mode = request.args.get('mode', 'detect').lower()
    use_gpu = request.args.get('gpu', '').lower() == 'true'
    frames = request.args.get('frames', None, type=int)
    seconds = request.args.get('seconds', None, type=int)
    execution_seconds = request.args.get('execution_seconds', None, type=int)
    
    # Check if video URL is provided
    if video_url:
        return Response(generate_frames(video_url, mode, use_gpu, frames, seconds, execution_seconds),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return "Error: Missing video URL parameter", 400

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
