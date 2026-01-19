"""
Pronunciation Scorer using RapidFuzz
Compares expected text vs recognized text and generates feedback
"""

from rapidfuzz import fuzz


def compute_score(expected_text: str, recognized_text: str) -> dict:
    """
    Compute pronunciation score and generate feedback.
    
    Args:
        expected_text: The text that should have been spoken
        recognized_text: The text recognized from speech
    
    Returns:
        Dictionary containing score, feedback, and improvement tip
    """
    if not expected_text or not recognized_text:
        return {
            "score": 0,
            "feedback": "No text provided",
            "improvement_tip": "Please provide both expected and recognized text"
        }
    
    # Calculate similarity using rapidfuzz
    similarity_ratio = fuzz.ratio(expected_text.lower(), recognized_text.lower()) / 100
    score = round(similarity_ratio * 100, 2)
    
    # Generate feedback based on score
    if score >= 85:
        feedback = "Excellent"
    elif score >= 60:
        feedback = "Good"
    else:
        feedback = "Try again slowly"
    
    # Detect missing/incorrect characters for improvement tip
    improvement_tip = _generate_improvement_tip(expected_text, recognized_text)
    
    return {
        "score": score,
        "feedback": feedback,
        "improvement_tip": improvement_tip
    }


def _generate_improvement_tip(expected: str, recognized: str) -> str:
    """
    Generate improvement tips by detecting missing or incorrect characters.
    
    Args:
        expected: Expected text
        recognized: Recognized text
    
    Returns:
        Improvement tip string
    """
    # Find missing characters using set difference
    expected_chars = set(expected.lower())
    recognized_chars = set(recognized.lower())
    missing_chars = expected_chars - recognized_chars
    
    if missing_chars:
        missing_str = ', '.join(sorted(missing_chars - {' '}))  # Exclude spaces
        if missing_str:
            return f"Focus on pronouncing these characters clearly: {missing_str}"
    
    # If no missing characters, check for length difference
    if len(recognized) < len(expected):
        return "Try speaking more clearly and completely"
    elif len(recognized) > len(expected):
        return "Try to avoid adding extra sounds"
    
    return "Great job! Keep practicing for even better clarity"
