"""
Simulated Whisper Speech Recognition Engine
Since Antigravity cannot run actual Whisper models, this simulates recognition
by introducing random character removal to mimic speech recognition errors.
"""

import random


def recognize_speech(audio_file, expected_text: str) -> str:
    """
    Simulate speech recognition by randomly removing 1-2 characters from expected text.
    
    Args:
        audio_file: Audio file (not used in simulation)
        expected_text: The expected text to base simulation on
    
    Returns:
        Simulated recognized text with minor errors
    """
    if not expected_text:
        return ""
    
    # Convert to list for easier manipulation
    text_chars = list(expected_text)
    
    # Randomly remove 1-2 characters to simulate speech errors
    if len(text_chars) > 3:
        num_errors = random.randint(1, 2)
        for _ in range(num_errors):
            if len(text_chars) > 1:
                # Remove a random character (not spaces to keep word structure)
                non_space_indices = [i for i, c in enumerate(text_chars) if c != ' ']
                if non_space_indices:
                    remove_idx = random.choice(non_space_indices)
                    text_chars.pop(remove_idx)
    
    recognized_text = ''.join(text_chars)
    return recognized_text
