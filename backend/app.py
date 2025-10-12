from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from gemini_client import GeminiClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Fluenter Grammar API", version="1.0.0")

# CORS middleware to allow Electron client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini client
gemini_client = GeminiClient()


class TextInput(BaseModel):
    text: str
    context: str = ""


class CorrectionResponse(BaseModel):
    original: str
    corrected: str
    suggestions: list[str] = []
    has_errors: bool


@app.get("/")
async def root():
    return {"message": "Fluenter Grammar API is running", "status": "active"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "fluenter-backend"}


@app.post("/correct", response_model=CorrectionResponse)
async def correct_text(input_data: TextInput):
    """
    Analyze and correct grammar in the provided text using Gemini AI.
    """
    try:
        if not input_data.text or len(input_data.text.strip()) == 0:
            return CorrectionResponse(
                original=input_data.text,
                corrected=input_data.text,
                suggestions=[],
                has_errors=False
            )
        
        logger.info(f"Processing text: {input_data.text[:50]}...")
        
        # Get correction from Gemini
        corrected_text, suggestions = await gemini_client.correct_grammar(
            input_data.text, 
            input_data.context
        )
        
        has_errors = corrected_text.strip() != input_data.text.strip()
        
        return CorrectionResponse(
            original=input_data.text,
            corrected=corrected_text,
            suggestions=suggestions,
            has_errors=has_errors
        )
    
    except Exception as e:
        logger.error(f"Error processing text: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")


@app.post("/rephrase")
async def rephrase_text(input_data: TextInput):
    """
    Rephrase text for better clarity and style.
    """
    try:
        if not input_data.text or len(input_data.text.strip()) == 0:
            return {"original": input_data.text, "rephrased": []}
        
        logger.info(f"Rephrasing text: {input_data.text[:50]}...")
        
        rephrased_options = await gemini_client.rephrase_text(input_data.text)
        
        return {
            "original": input_data.text,
            "rephrased": rephrased_options
        }
    
    except Exception as e:
        logger.error(f"Error rephrasing text: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error rephrasing text: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
