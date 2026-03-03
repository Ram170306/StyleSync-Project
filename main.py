from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import httpx
import torch
from transformers import CLIPProcessor, CLIPModel
import logging
from typing import Dict, Any
from routes import ai_routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="StyleSync AI Outfit Matcher")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize CLIP model
try:
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    logger.info("CLIP model loaded successfully")
except Exception as e:
    logger.error(f"Error loading CLIP model: {str(e)}")
    raise

async def get_ollama_recommendations(features: str) -> Dict[str, Any]:
    """Get fashion recommendations from Ollama."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama2",
                    "prompt": f"""Based on these clothing features: {features}
                    Provide fashion recommendations in JSON format with the following structure:
                    {{
                        "recommendations": [
                            {{
                                "outfit_style": "string",
                                "color_scheme": "string",
                                "occasion": "string",
                                "additional_items": ["string"]
                            }}
                        ]
                    }}""",
                    "stream": False
                }
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Error getting Ollama recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get fashion recommendations")

@app.post("/api/upload")
async def upload_image(file: UploadFile) -> Dict[str, Any]:
    """
    Upload an image and get AI-powered fashion recommendations.
    """
    try:
        # Read and validate image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Process image with CLIP
        inputs = processor(images=image, return_tensors="pt", padding="max_length", max_length=77)
        image_features = model.get_image_features(**inputs)
        
        # Get text features for clothing attributes
        clothing_attributes = [
            "formal wear", "casual wear", "sportswear",
            "red", "blue", "green", "black", "white",
            "striped", "patterned", "solid color"
        ]
        text_inputs = processor(text=clothing_attributes, return_tensors="pt", padding="max_length", max_length=77)
        text_features = model.get_text_features(**text_inputs)
        
        # Calculate similarity scores
        similarity = torch.nn.functional.cosine_similarity(
            image_features, text_features
        )
        
        # Get top matching attributes
        top_indices = torch.topk(similarity, k=3).indices
        detected_features = [clothing_attributes[idx] for idx in top_indices]
        
        # Get recommendations from Ollama
        features_str = ", ".join(detected_features)
        recommendations = await get_ollama_recommendations(features_str)
        
        return {
            "detected_features": detected_features,
            "recommendations": recommendations
        }
        
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )

# Include routers
app.include_router(ai_routes.router, prefix="/api/ai", tags=["ai"])

@app.get("/")
async def root():
    return {"message": "StyleSync API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 