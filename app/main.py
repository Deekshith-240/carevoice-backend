"""
FastAPI Backend for CareVoice Speech Analysis
Provides endpoint for analyzing pronunciation and speech quality
"""

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from .whisper_engine import recognize_speech
from .scorer import compute_score


# Create FastAPI app
app = FastAPI(
    title="CareVoice Speech Analysis API",
    description="API for analyzing speech pronunciation and quality",
    version="1.0.0"
)

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


class AnalysisResponse(BaseModel):
    """Response model for speech analysis"""
    recognized_text: str
    score: float
    feedback: str
    improvement_tip: str


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to CareVoice Speech Analysis API",
        "version": "1.0.0",
        "endpoints": {
            "/analyze-speech": "POST - Analyze speech pronunciation"
        }
    }


@app.post("/analyze-speech", response_model=AnalysisResponse)
async def analyze_speech(
    audio: UploadFile = File(..., description="Audio file to analyze"),
    expected_text: str = Form(..., description="Expected text that should be spoken")
):
    """
    Analyze speech pronunciation by comparing recognized text with expected text.
    
    Args:
        audio: Audio file (WAV, MP3, etc.)
        expected_text: The text that should have been spoken
    
    Returns:
        AnalysisResponse with recognized text, score, feedback, and improvement tip
    """
    # Read audio file (in real implementation, this would be processed)
    audio_content = await audio.read()
    
    # Simulate speech recognition
    recognized_text = recognize_speech(audio_content, expected_text)
    
    # Compute pronunciation score
    score_result = compute_score(expected_text, recognized_text)
    
    # Return analysis results
    return AnalysisResponse(
        recognized_text=recognized_text,
        score=score_result["score"],
        feedback=score_result["feedback"],
        improvement_tip=score_result["improvement_tip"]
    )


if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
