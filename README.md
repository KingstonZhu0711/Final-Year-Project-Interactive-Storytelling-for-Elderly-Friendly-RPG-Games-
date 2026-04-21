# 🎭 Interactive Storytelling for Elderly-Friendly RPG Games

**Capstone Project (COMP4913)** | **The Hong Kong Polytechnic University**  
**Author:** Zhu Jin Shun (22101071d) | **Date:** April 2026

---

## 🌟 Overview
An AI-powered RPG storytelling system specifically designed for senior citizens. This project focuses on accessibility, cognitive ease, and emotional well-being by generating calm, positive, and engaging interactive narratives in both English and Chinese.

### ✨ Key Features
*   **Dual-Language Support:** Full localization for English and Chinese audiences.
*   **Calming Themes:** Curated story paths including *Peaceful Village Life*, *Romantic Love Story*, and *Modern Living*.
*   **Elderly-Centric UI:** Large fonts (18pt+), high-contrast elements, and simplified navigation.
*   **Voice Integration:** Slow-speed text-to-speech (TTS) narration for easier comprehension.
*   **Memory Coherence:** Uses rolling history summaries to ensure the AI doesn't lose the plot during long sessions.
*   **Quality Assurance:** Automatic story evaluation using **BERTScore**.

---

## 🛠️ Technologies Used
*   **Backend:** Python, Flask
*   **AI/LLM:** Ollama (Llama 3.1 & Qwen2), LangChain
*   **TTS:** gTTS (Google Text-to-Speech)
*   **Evaluation:** BERTScore
*   **Frontend:** HTML5, CSS3 (High-Contrast), JavaScript

---

## 🚀 Getting Started

### Prerequisites
1.  **Install Ollama:** Download from [ollama.com](https://ollama.com/download)
2.  **Download Models:** Open your terminal and run:
    ```bash
    ollama pull llama3.1:8b  # For the English version
    ollama pull qwen2:7b     # For the Chinese version
    ```

### Installation
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/elderly-rpg-storytelling.git
    cd elderly-rpg-storytelling
    ```
2.  **Set up a virtual environment:**
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # macOS/Linux:
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application
The project runs as two separate Flask instances for English and Chinese:

| Language | Command | Local URL |
| :--- | :--- | :--- |
| **English** | `python app_eng.py` | `http://127.0.0.1:5000` |
| **Chinese** | `python app_cn.py` | `http://127.0.0.1:5001` |

---

## 📖 How to Play
1.  **Select a Theme:** Choose from Village, Romantic, or Modern life.
2.  **Adjust Settings:** Select the number of scenes for your story length.
3.  **Start Story:** Click the "Start" button.
4.  **Interact:** 
    *   Read the text or click the **Speaker Icon** for audio narration.
    *   Select one of the 2–3 simplified choices provided at the end of each scene.
5.  **Completion:** Enjoy a warm, positive ending designed to leave the user feeling relaxed.

---

## 📂 Project Structure
```text
├── app_eng.py          # Flask application (English)
├── app_cn.py           # Flask application (Chinese)
├── bert_eng.py         # BERTScore evaluation scripts
├── bert_cn.py          # BERTScore evaluation scripts
├── static/
│   └── audio/          # Generated TTS voice files
├── log/                # Full story logs
├── history/            # Saved story summaries
└── requirements.txt    # Project dependencies

Tailwind CSS (UI)
