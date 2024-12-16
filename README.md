# Computer Vision Server

This project is a simple Flask web server that allows users to upload JPG or PNG images, processes them with YOLOv3 to label areas, and displays the result on the same web page.

## Requirements

- Python 3.6+
- Flask
- OpenCV
- NumPy

## Setup

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd cvisionserver
    ```

2. Set up a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Download the YOLOv3 weights, configuration, and class names files:
    - [yolov3.weights](https://pjreddie.com/media/files/yolov3.weights)
    - [yolov3.cfg](https://github.com/pjreddie/darknet/blob/master/cfg/yolov3.cfg)
    - [coco.names](https://github.com/pjreddie/darknet/blob/master/data/coco.names)

    Place these files in the same directory as `main.py`.

5. Create an `uploads` directory:
    ```bash
    mkdir uploads
    ```

## Running the Server

1. Start the Flask server:
    ```bash
    python main.py
    ```

2. Open your web browser and go to `http://127.0.0.1:5000/`.

3. Upload a JPG or PNG image to see the labeled result.

## Running with Docker

1. Build the Docker image:
    ```bash
    docker build -t cvisionserver .
    ```

2. Run the Docker container:
    ```bash
    docker run -p 5000:5000 cvisionserver
    ```

3. Open your web browser and go to `http://127.0.0.1:5000/`.

4. Upload a JPG or PNG image to see the labeled result.

## License

This project is licensed under the MIT License.
