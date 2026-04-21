# Interactive Storytelling for Elderly-Friendly RPG Games

**COMP4913 Capstone Project**  
**Author:** Zhu Jin Shun (22101071d)  
**The Hong Kong Polytechnic University**  
**April 2026**

An elderly-friendly AI-powered RPG storytelling system that generates calm, positive, and accessible interactive stories in both English and Chinese.

### Key Features
- Dual-language support (English & Chinese)
- Three calming themes: Peaceful Village, Romantic, Modern Living Life
- Adjustable story length
- Large fonts (18pt+) and high-contrast UI for seniors
- Slow-speed voice narration
- Rolling history summary for story coherence
- BERTScore automatic evaluation

---

## How to Run the Project

### 1. Install Ollama
Download and install Ollama: [https://ollama.com/download](https://ollama.com/download)

Then pull the models in terminal:
```bash
ollama pull llama3.1:8b     # English
ollama pull qwen2:7b        # Chinese

### 2. Clone & Setup
Bashgit clone https://github.com/yourusername/elderly-rpg-storytelling.git
cd elderly-rpg-storytelling

# Create virtual environment
python -m venv venv
venv\Scripts\activate     # Windows

pip install -r requirements.txt

### 3. Run the Application
English Version:
Bashpython app_eng.py
Chinese Version:
Bashpython app_cn.py

English: Open http://127.0.0.1:5000
Chinese: Open http://127.0.0.1:5001
