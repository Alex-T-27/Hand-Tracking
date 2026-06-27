# HandTracking

Real-time hand tracking with [OpenCV](https://opencv.org/) and [MediaPipe](https://developers.google.com/mediapipe). It captures your webcam feed, detects up to two hands, draws the hand skeleton, and labels each finger tip (Thumb, Index, Middle, Ring, Pinky) with a marker.

## Demo

![Hand tracking detecting a hand with finger-tip labels](assets/demo-1.png)

![Hand tracking detecting both hands](assets/demo-2.png)

## Features

- Live webcam capture with a mirrored (selfie) view
- Detects up to 2 hands at once via MediaPipe Hands
- Draws the full hand skeleton (landmarks + connections)
- Labels the 5 finger tips and marks them with a green dot
- Retries camera reads (5 attempts) so a slow camera start doesn't crash it

## Requirements

- Python 3.12
- A webcam

Dependencies are pinned in [`requirements.txt`](requirements.txt) to avoid the
numpy 2.x / mediapipe conflict.

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

Press **`q`** in the video window to quit.

## How it works

1. Grab a frame from the webcam (`cv2.VideoCapture`) and flip it horizontally.
2. Convert BGR → RGB (MediaPipe expects RGB) and run `hands.process()`.
3. For each detected hand, draw the landmarks and connections.
4. Convert the normalized finger-tip coordinates to pixels, then label and
   circle each tip.
