# Interactive Storytelling for Elderly-Friendly RPG Games

**COMP4913 Capstone Project**  
**Author:** Zhu Jin Shun (22101071d)  
**The Hong Kong Polytechnic University**  
**April 2026**

An elderly-friendly AI-powered RPG storytelling system that generates calm, positive, and accessible interactive stories in both English and Chinese.

### Key Features
- Dual-language support (English & Chinese)
- Three calming themes: Peaceful Village Life, Romantic Love Story, Modern Living Life
- Adjustable story length
- Large fonts (18pt+) and high-contrast UI designed for seniors
- Slow-speed voice narration
- Rolling history summary to maintain story coherence
- BERTScore for automatic evaluation

---

## How to Run the Project

### Step 1: Install Ollama
1. Download and install Ollama from: https://ollama.com/download
2. Open terminal/command prompt and pull the models:

```bash
ollama pull llama3.1:8b     # English version
ollama pull qwen2:7b        # Chinese version
Step 2: Clone and Setup
Bashgit clone https://github.com/yourusername/elderly-rpg-storytelling.git
cd elderly-rpg-storytelling

python -m venv venv
venv\Scripts\activate        # On Windows

pip install -r requirements.txt
Step 3: Run the Application
English Version:
Bashpython app_eng.py
Chinese Version:
Bashpython app_cn.py

English: http://127.0.0.1:5000
Chinese: http://127.0.0.1:5001


How to Use

Select a theme (Peaceful Village, Romantic, or Modern Living Life)
Choose the number of scenes
Click Start Story
Read or listen to each scene (click the speaker icon for voice)
Choose one of the 2–3 simple options
Continue until the warm ending appears

All stories and audio files are automatically saved in timestamped folders.

Project Structure

app_eng.py → English version
app_cn.py → Chinese version
bert_eng.py / bert_cn.py → BERTScore evaluation
static/audio/ → Generated voice files
log/ and history/ → Saved story logs


Technologies Used

Flask (Web Framework)
Ollama + LangChain (Local LLMs)
gTTS (Text-to-Speech)
BERTScore (Evaluation)
Tailwind CSS (UI)
