# Text Emotion Detection

A Flask-based web application for detecting emotions in text using machine learning.

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Docker (optional, for containerized deployment)

## Local Development Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd text-emotion-detection
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the development server:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to `http://localhost:5000`

## Production Deployment with Docker

1. Build the Docker image:
   ```bash
   docker build -t text-emotion-detection .
   ```

2. Run the container:
   ```bash
   docker run -d -p 5000:5000 --name emotion-detector text-emotion-detection
   ```

3. The application will be available at `http://<server-ip>:5000`

## API Endpoints

- `POST /predict` - Predict emotion from text
  - Request body: `{"text": "your text here"}`
  - Response: JSON with prediction results

## Project Structure

```
├── app.py                # Main application file
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker configuration
├── gunicorn_config.py    # Gunicorn server configuration
├── model/                # Trained model and related files
├── static/               # Static files (CSS, JS, images)
└── templates/            # HTML templates
```

## Environment Variables

- `FLASK_ENV`: Set to "production" in production
- `FLASK_APP`: Set to "app.py"

## License

[Your License Here]
