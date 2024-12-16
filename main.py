from flask import Flask, request, render_template, send_file
import cv2
import numpy as np
import os

app = Flask(__name__)

# Load YOLO
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/uploader', methods=['POST'])
def uploader_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and (file.filename.endswith('.jpg') or file.filename.endswith('.png')):
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        labeled_image_path = process_image(file_path)
        return send_file(labeled_image_path, mimetype='image/jpeg')

def process_image(image_path):
    # Load image
    img = cv2.imread(image_path)
    height, width, channels = img.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing information on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, f"{label} {confidence:.2f}", (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

    labeled_image_path = os.path.join('uploads', 'labeled_' + os.path.basename(image_path))
    cv2.imwrite(labeled_image_path, img)
    return labeled_image_path

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
