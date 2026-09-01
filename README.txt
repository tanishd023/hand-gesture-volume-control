# Hand Gesture Volume Control 🎚️

A computer vision project that controls Windows system volume using hand gestures.

## How It Works

The webcam captures the user's hand.

MediaPipe detects the hand landmarks.

The distance between the thumb and index finger is calculated.

- Fingers close → Low volume
- Fingers far apart → High volume

The calculated value is sent to the Windows audio system using Pycaw.

## Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy
- Pycaw
- Comtypes

## Features

- Real-time hand tracking
- Thumb and index finger detection
- Gesture-based volume control
- Real-time volume percentage
- Visual volume bar
