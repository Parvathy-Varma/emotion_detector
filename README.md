# AI-Powered Emotion-Based Recommender System

An AI-powered web application that detects a user's emotion through facial expression recognition and provides personalized recommendations, activities, and interactive games to improve user engagement and emotional well-being.

---

## Features

- Real-time facial emotion detection using a webcam
- Deep Learning-based emotion recognition using Convolutional Neural Networks (CNN)
- Detects multiple emotions:
  - Angry
  - Happy
  - Sad
  - Neutral
- Emotion-based personalized recommendations
- Interactive games and activities based on the detected emotion
- Responsive and user-friendly web interface
- Real-time emotion prediction using OpenCV and TensorFlow

---

## Tech Stack

### Backend
- Python
- Flask
- TensorFlow
- Keras
- OpenCV
- NumPy

### Machine Learning
- Convolutional Neural Network (CNN)
- Facial Emotion Recognition
- FER2013 Dataset

### Frontend
- HTML5
- CSS3
- JavaScript

---

## Dataset

This project uses the **FER2013 (Facial Expression Recognition 2013)** dataset, which contains grayscale facial images labeled with different emotions.

**Dataset Source:**
- Kaggle: https://www.kaggle.com/datasets/msambare/fer2013

> **Note:** The dataset is **not included** in this repository because of its size. Download it separately from the above link if you wish to retrain the model.

---

## Project Structure

```
emotion_detector/
│
├── emotion_webcam.py
├── emotion_model.h5
├── train_emotion_model.py
├── mp2_web/
│   ├── app.py
│   ├── templates/
│   ├── static/
│   └── init_db.py
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Parvathy-Varma/emotion_detector.git
cd emotion_detector
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, install the required packages manually:

```bash
pip install flask tensorflow keras opencv-python numpy
```

---

## How to Run

Navigate to the project folder:

```bash
cd emotion_detector/mp2_web
```

Run the Flask application:

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

Allow camera access when prompted.

---

## How It Works

1. The user opens the web application.
2. The webcam captures the user's face.
3. OpenCV detects the face region.
4. The trained CNN model predicts the user's emotion.
5. Based on the detected emotion, the system provides personalized recommendations and interactive games.

---

## Detected Emotions

- 😊 Happy
- 😐 Neutral
- 😢 Sad
- 😠 Angry

---

## Applications

- Mental Wellness Support
- Emotion-Aware Recommendation Systems
- Educational Applications
- Interactive Entertainment
- Human-Computer Interaction Research

---

## Future Enhancements

- Detect additional emotions such as Surprise, Fear, and Disgust
- User authentication and history tracking
- Personalized music and movie recommendations
- Cloud deployment
- Mobile application support

---

## Author

**Parvathy Varma**

GitHub: https://github.com/Parvathy-Varma
