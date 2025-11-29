"""
Demo script to test StudyAssistantAI without running the interactive loop
This script tests various features of the agent
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

from tools.summarizer import summarize_topic
from tools.quiz_generator import generate_quiz
from tools.habit_tracker import track_activity, get_progress

# Load environment variables
load_dotenv()

print("=" * 60)
print("StudyAssistantAI - Demo Test")
print("=" * 60)

# Check API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key or api_key == "your_gemini_api_key_here":
    print("\n❌ ERROR: Please set your GEMINI_API_KEY in the .env file")
    print("Get your API key from: https://makersuite.google.com/app/apikey")
    exit(1)

print("\n✅ API Key found!")

# Initialize Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

print("✅ Gemini model initialized!")

# Test 1: Habit Tracker (no API needed)
print("\n" + "=" * 60)
print("TEST 1: Habit Tracker")
print("=" * 60)

result = track_activity("Studied Python basics", hours=2.5)
print(f"✅ {result['message']}")

result = track_activity("Read biology textbook", hours=1.0)
print(f"✅ {result['message']}")

progress = get_progress()
print(f"\n📊 Total tasks: {progress['total_tasks']}")
print(f"📊 Total hours: {progress['total_hours']:.1f}h")

# Test 2: Topic Summary (requires API)
print("\n" + "=" * 60)
print("TEST 2: Topic Summarization")
print("=" * 60)
print("Requesting summary for 'Photosynthesis'...")

try:
    result = summarize_topic(model, "Photosynthesis")
    print("\n✅ Summary generated!")
    print("-" * 60)
    print(result['content'][:500] + "..." if len(result['content']) > 500 else result['content'])
    print("-" * 60)
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Quiz Generation (requires API)
print("\n" + "=" * 60)
print("TEST 3: Quiz Generation")
print("=" * 60)
print("Generating quiz for 'Solar System'...")

try:
    result = generate_quiz(model, "Solar System", num_mcqs=3)
    print("\n✅ Quiz generated!")
    print("-" * 60)
    print(result['content'][:500] + "..." if len(result['content']) > 500 else result['content'])
    print("-" * 60)
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)
print("Demo completed successfully! 🎉")
print("=" * 60)
print("\nNext steps:")
print("1. Run 'python agent.py' for the full interactive experience")
print("2. Try: 'Explain quantum physics'")
print("3. Try: 'Create a quiz on World War 2'")
print("4. Try: 'Track 3 hours of coding'")
print("=" * 60)
