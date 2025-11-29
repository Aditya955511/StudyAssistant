"""
Quiz Generator Tool - Creates MCQs, flashcards, and practice tests
"""

import google.generativeai as genai


def generate_quiz(model, topic: str, num_mcqs: int = 5) -> dict:
    """
    Generate MCQs, flashcards, and practice questions
    
    Args:
        model: Gemini model instance
        topic: Topic for quiz generation
        num_mcqs: Number of MCQs to generate
        
    Returns:
        dict: Contains MCQs, flashcards, and practice test
    """
    prompt = f"""
You are a study assistant creating a quiz on "{topic}".

Generate the following:

1. **MCQs** ({num_mcqs} questions)
   - Each with 4 options (A, B, C, D)
   - Mark the correct answer clearly
   
2. **FLASHCARDS** (5 cards)
   - Format: Q: [question] → A: [answer]
   
3. **PRACTICE TEST** (3 open-ended questions)
   - Questions that require detailed answers

Format everything clearly with headings and numbering.
Make questions challenging but appropriate for students.
"""
    
    response = model.generate_content(prompt)
    return {
        "type": "quiz",
        "topic": topic,
        "content": response.text
    }


def generate_flashcards(model, topic: str, num_cards: int = 10) -> dict:
    """
    Generate flashcards only
    
    Args:
        model: Gemini model instance
        topic: Topic for flashcard generation
        num_cards: Number of flashcards
        
    Returns:
        dict: Contains flashcards
    """
    prompt = f"""
Create {num_cards} flashcards on "{topic}".

Format each as:
**Card [number]:**
Q: [Question]
A: [Answer]

Make them concise and perfect for quick revision.
"""
    
    response = model.generate_content(prompt)
    return {
        "type": "flashcards",
        "topic": topic,
        "content": response.text
    }

