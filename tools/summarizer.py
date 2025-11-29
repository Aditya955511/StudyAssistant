"""
Summarizer Tool - Generates summaries with key points and examples
"""

import google.generativeai as genai


def summarize_text(model, text: str) -> dict:
    """
    Summarize text with structured output
    
    Args:
        model: Gemini model instance
        text: Text to summarize
        
    Returns:
        dict: Contains summary, key_points, examples, quick_revision
    """
    prompt = f"""
You are a study assistant. Summarize the following content for a student.

CONTENT:
{text}

Provide your response in the following structure:
1. SUMMARY (5-7 lines)
2. KEY POINTS (bullet points)
3. EXAMPLES (if relevant)
4. QUICK REVISION (3 main takeaways)

Format your response clearly with headings.
"""
    
    response = model.generate_content(prompt)
    return {
        "type": "summary",
        "content": response.text
    }


def summarize_topic(model, topic: str) -> dict:
    """
    Generate a comprehensive summary for a given topic
    
    Args:
        model: Gemini model instance
        topic: Topic to explain and summarize
        
    Returns:
        dict: Contains explanation and structured summary
    """
    prompt = f"""
You are a study assistant. Explain the topic "{topic}" to a student.

Provide:
1. SUMMARY (5-7 lines explaining the concept)
2. KEY POINTS (bullet points covering main ideas)
3. EXAMPLES (at least 2 real-world examples)
4. QUICK REVISION (3 most important takeaways)

Be clear, concise, and student-friendly.
"""
    
    response = model.generate_content(prompt)
    return {
        "type": "topic_summary",
        "topic": topic,
        "content": response.text
    }

