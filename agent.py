"""
StudyAssistantAI - Intelligent Study Helper
Main agent that routes user requests to appropriate tools
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from tools.summarizer import summarize_text, summarize_topic
from tools.quiz_generator import generate_quiz, generate_flashcards
from tools.habit_tracker import track_activity, get_progress, clear_tracker
from tools.pdf_parser import parse_pdf
from tools.youtube_parser import parse_youtube

# Initialize Rich console for beautiful output
console = Console()

# Load environment variables
load_dotenv()


class StudyAssistantAI:
    """Main AI Agent for study assistance"""
    
    def __init__(self):
        """Initialize the agent with Gemini API"""
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key or api_key == "your_gemini_api_key_here":
            console.print("[bold red]❌ ERROR: Please set your GEMINI_API_KEY in the .env file[/bold red]")
            exit(1)
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        console.print("[bold green]✅ StudyAssistantAI initialized successfully![/bold green]\n")
    
    def classify_intent(self, user_input: str) -> dict:
        """
        Classify user intent using Gemini
        
        Returns:
            dict: Intent type and extracted parameters
        """
        prompt = f"""
You are an intent classifier for a study assistant AI.
Given the user input, determine the intent and extract relevantṇ information.

User Input: "{user_input}"

Classify into one of these intents:
1. SUMMARIZE_TEXT - User provides text to summarize
2. SUMMARIZE_TOPIC - User asks to explain/summarize a topic
3. GENERATE_QUIZ - User wants MCQs, quiz, or flashcards
4. TRACK_HABIT - User wants to log study progress
5. SHOW_PROGRESS - User wants to see their progress
6. PARSE_PDF - User mentions a PDF file
7. PARSE_YOUTUBE - User provides a YouTube URL
8. GENERAL_QUERY - General question or unclear intent

Respond ONLY with JSON in this format:
{{
    "intent": "INTENT_TYPE",
    "topic": "extracted topic if any",
    "text": "extracted text if any",
    "url": "extracted URL if any",
    "file_path": "extracted file path if any",
    "hours": "extracted hours if mentioned",
    "task": "extracted task if mentioned"
}}
"""
        
        response = self.model.generate_content(prompt)
        
        try:
            # Clean response and parse JSON
            import json
            result_text = response.text.strip()
            # Remove markdown code blocks if present
            if result_text.startswith("```"):
                result_text = result_text.split("```")[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
            return json.loads(result_text.strip())
        except:
            return {"intent": "GENERAL_QUERY"}
    
    def handle_request(self, user_input: str):
        """
        Main handler that routes requests to appropriate tools
        
        Args:
            user_input: User's request
        """
        # Classify intent
        intent_data = self.classify_intent(user_input)
        intent = intent_data.get("intent", "GENERAL_QUERY")
        
        console.print(f"[dim]🧠 Detected intent: {intent}[/dim]\n")
        
        # Route to appropriate tool
        if intent == "SUMMARIZE_TEXT":
            text = intent_data.get("text") or user_input
            result = summarize_text(self.model, text)
            self.display_result(result)
        
        elif intent == "SUMMARIZE_TOPIC":
            topic = intent_data.get("topic") or user_input
            result = summarize_topic(self.model, topic)
            self.display_result(result)
        
        elif intent == "GENERATE_QUIZ":
            topic = intent_data.get("topic") or user_input
            result = generate_quiz(self.model, topic)
            self.display_result(result)
        
        elif intent == "TRACK_HABIT":
            task = intent_data.get("task") or user_input
            hours = intent_data.get("hours")
            if hours:
                try:
                    hours = float(hours)
                except:
                    hours = None
            result = track_activity(task, hours)
            console.print(Panel(result.get("message", "Tracked!"), 
                              title="📊 Habit Tracker", style="green"))
        
        elif intent == "SHOW_PROGRESS":
            result = get_progress()
            self.display_progress(result)
        
        elif intent == "PARSE_PDF":
            file_path = intent_data.get("file_path") or user_input
            if file_path:
                # Clean file path - remove quotes and extra whitespace
                file_path = file_path.strip().strip('"').strip("'")
                
                # Add .pdf extension if not present
                if not file_path.lower().endswith('.pdf'):
                    file_path = file_path + '.pdf'
                
                # Check if file exists
                if not os.path.exists(file_path):
                    console.print(f"[red]❌ File not found: {file_path}[/red]")
                    console.print("[yellow]💡 Tip: Drag and drop the PDF file or provide the full path[/yellow]")
                else:
                    pdf_result = parse_pdf(file_path)
                    if pdf_result.get("success"):
                        # Summarize the PDF content
                        console.print(f"[green]📄 Extracted {pdf_result['num_pages']} pages[/green]\n")
                        result = summarize_text(self.model, pdf_result["text"][:10000])  # Limit text
                        self.display_result(result)
                    else:
                        console.print(f"[red]❌ Error: {pdf_result.get('error')}[/red]")
            else:
                console.print("[yellow]⚠️ Please provide the PDF file path[/yellow]")
        
        elif intent == "PARSE_YOUTUBE":
            url = intent_data.get("url") or user_input
            if url:
                # Extract URL if it's in the text
                import re
                url_match = re.search(r'(https?://[^\s]+|youtu\.be/[^\s]+)', url)
                if url_match:
                    url = url_match.group(1)
                
                console.print(f"[dim]🔍 Processing: {url}[/dim]\n")
                yt_result = parse_youtube(url)
                if yt_result.get("success"):
                    console.print(f"[green]📺 Extracted transcript ({yt_result['duration']:.0f}s)[/green]\n")
                    result = summarize_text(self.model, yt_result["transcript"])
                    self.display_result(result)
                else:
                    console.print(f"[red]❌ Error: {yt_result.get('error')}[/red]")
                    console.print("[yellow]💡 Tip: Make sure the video has captions/subtitles enabled[/yellow]")
            else:
                console.print("[yellow]⚠️ Please provide a YouTube URL[/yellow]")
        
        else:
            # General query - direct to Gemini
            response = self.model.generate_content(user_input)
            console.print(Panel(Markdown(response.text), 
                              title="💡 Response", style="cyan"))
    
    def display_result(self, result: dict):
        """Display formatted result"""
        content = result.get("content", "")
        result_type = result.get("type", "result")
        
        title_map = {
            "summary": "📝 Summary",
            "topic_summary": "📚 Topic Summary",
            "quiz": "🎯 Quiz Generated",
            "flashcards": "🗂️ Flashcards"
        }
        
        title = title_map.get(result_type, "📋 Result")
        console.print(Panel(Markdown(content), title=title, style="blue"))
    
    def display_progress(self, progress: dict):
        """Display study progress"""
        total_tasks = progress.get("total_tasks", 0)
        total_hours = progress.get("total_hours", 0)
        entries = progress.get("entries", [])
        
        console.print(Panel(
            f"[bold]Total Tasks:[/bold] {total_tasks}\n"
            f"[bold]Total Hours:[/bold] {total_hours:.1f}h",
            title="📊 Study Progress",
            style="green"
        ))
        
        if entries:
            console.print("\n[bold]Recent Activities:[/bold]")
            for entry in entries[-10:]:  # Show last 10
                hours_str = f" ({entry['hours']}h)" if entry.get('hours') else ""
                console.print(f"  • [{entry['date']}] {entry['task']}{hours_str}")
    
    def run(self):
        """Main interactive loop"""
        console.print(Panel.fit(
            "[bold cyan]StudyAssistantAI[/bold cyan]\n\n"
            "Your intelligent study companion\n\n"
            "Commands:\n"
            "  • Summarize a topic or text\n"
            "  • Generate quiz/MCQs/flashcards\n"
            "  • Track study habits\n"
            "  • Parse PDFs and YouTube videos\n"
            "  • Type 'exit' to quit",
            style="bold blue"
        ))
        
        while True:
            try:
                console.print("\n[bold yellow]You:[/bold yellow]", end=" ")
                user_input = input().strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    console.print("[bold green]👋 Happy studying![/bold green]")
                    break
                
                console.print()
                self.handle_request(user_input)
                
            except KeyboardInterrupt:
                console.print("\n[bold green]👋 Happy studying![/bold green]")
                break
            except Exception as e:
                console.print(f"[red]❌ Error: {str(e)}[/red]")


if __name__ == "__main__":
    agent = StudyAssistantAI()
    agent.run()
