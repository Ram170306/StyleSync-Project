# StyleSync AI Outfit Matcher Backend

This is the backend service for the StyleSync AI Outfit Matching system. It uses FastAPI, CLIP, and Ollama to provide AI-powered fashion recommendations based on uploaded images.

## Prerequisites

- Python 3.8+
- Ollama installed and running with LLaMA 2 model
- pip (Python package manager)

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make sure Ollama is running with LLaMA 2:
```bash
ollama run llama2
```

## Running the Server

Start the FastAPI server:
```bash
uvicorn main:app --reload --port 8000
```

The server will be available at `http://localhost:8000`

## API Endpoints

### POST /api/upload
Upload an image to get AI-powered fashion recommendations.

**Request:**
- Content-Type: multipart/form-data
- Body: image file

**Response:**
```json
{
    "detected_features": ["feature1", "feature2", "feature3"],
    "recommendations": {
        "recommendations": [
            {
                "outfit_style": "string",
                "color_scheme": "string",
                "occasion": "string",
                "additional_items": ["string"]
            }
        ]
    }
}
```

## Error Handling

The API includes comprehensive error handling for:
- Invalid image files
- CLIP model processing errors
- Ollama communication errors
- General server errors

All errors are logged and returned with appropriate HTTP status codes and error messages. 