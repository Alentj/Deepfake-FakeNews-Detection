
# AI-Powered Deepfake & Fake News Detection

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.2-orange)](https://flask.palletsprojects.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.14.0-red)](https://www.tensorflow.org/)
[![Transformers](https://img.shields.io/badge/Transformers-4.44.2-green)](https://huggingface.co/transformers/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

---

## Overview

This project provides a web-based AI dashboard for detecting:

- **Deepfake Images**: Determines if an image is real or fake using a Convolutional Neural Network (CNN).
- **Fake News Articles**: Determines if news content is FAKE or REAL using a **Zero-Shot Text Classifier** from Hugging Face.

---

## Features

- **Deepfake Detection**:
  - Upload an image via the dashboard.
  - Get prediction with confidence score.
  
- **Fake News Detection**:
  - Enter a keyword to fetch news from multiple APIs.
  - Detect news authenticity using zero-shot classification (`facebook/bart-large-mnli`).
  - Supports fallback labeling: if no news found, automatically marks as FAKE.

- **APIs Used**:
  - NewsAPI, GNews, Mediastack, Bing News, NYTimes, The Guardian, Currents API.

---

## Tech Stack

- **Backend**: Flask, Python
- **Deepfake Model**: TensorFlow / Keras CNN
- **Fake News Model**: Hugging Face Transformers (Zero-Shot Classification)
- **Frontend**: HTML, CSS, JavaScript

---

## Installation

```bash
# Clone the repository
git clone https://github.com/Alentj/Deepfake-FakeNews-Detection.git
cd Deepfake-FakeNews-Detection

# Create virtual environment
python -m venv venv

# Activate virtual environment (Linux/macOS)
source venv/bin/activate

# Activate virtual environment (Windows)
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py


