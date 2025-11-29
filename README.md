# 🎓 StudyAssistantAI

**Your Intelligent Study Companion** - An AI-powered study helper that summarizes content, generates quizzes, and tracks your study habits.

## ✨ Features

- 📝 **Smart Summarization** - Summarize text, topics, PDFs, and YouTube videos
- 🎯 **Quiz Generation** - Create MCQs, flashcards, and practice tests
- 📊 **Habit Tracking** - Log study hours and track progress
- 📄 **PDF Parsing** - Extract and summarize PDF documents
- 📺 **YouTube Parsing** - Get transcripts and summaries from YouTube videos

## 🚀 Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

1. Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Open `.env` file and add your API key:

```env
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Run the Agent

```bash
python agent.py
```

## 💡 Usage Examples

### Summarize a Topic
```
You: Explain photosynthesis
```

### Generate a Quiz
```
You: Create a quiz on World War 2
```

### Track Study Time
```
You: Track 3 hours of Python coding
```

### Summarize a YouTube Video
```
You: Summarize this video: https://youtube.com/watch?v=...
```

### Parse a PDF
```
You: Summarize chapter1.pdf
```

### View Progress
```
You: Show my progress
```

## 🛠️ Project Structure

```
StudyAssistantAI/
├── agent.py                 # Main agent with intelligent routing
├── .env                     # API key configuration
├── requirements.txt         # Python dependencies
├── tools/
│   ├── summarizer.py       # Text & topic summarization
│   ├── quiz_generator.py   # MCQ & flashcard generation
│   ├── habit_tracker.py    # Study progress tracking
│   ├── pdf_parser.py       # PDF text extraction
│   └── youtube_parser.py   # YouTube transcript extraction
└── README.md               # This file
```

## 📦 Dependencies

- **google-generativeai** - Gemini AI for intelligence
- **python-dotenv** - Environment variable management
- **youtube-transcript-api** - YouTube transcript extraction
- **pypdf** - PDF parsing
- **rich** - Beautiful terminal output

## 🎨 Features in Detail

### Summarizer
- Provides 5-7 line summaries
- Lists key points in bullet format
- Includes relevant examples
- Offers quick revision notes

### Quiz Generator
- Creates 5 MCQs with 4 options each
- Generates flashcards in Q → A format
- Creates practice tests with open-ended questions

### Habit Tracker
- Logs study tasks with timestamps
- Tracks hours spent
- Shows progress statistics
- Stores data in JSON format

## 🔧 Customization

You can customize the number of questions, flashcards, or summary length by modifying the tool files in the `tools/` directory.

## 📝 License

This project is open source. Feel free to use and modify!

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

---

**Made with ❤️ for students who want to learn 10x faster**
