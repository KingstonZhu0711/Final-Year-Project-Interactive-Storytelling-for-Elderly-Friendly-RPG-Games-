from flask import Flask, render_template, request, session, redirect, url_for
import os
from datetime import datetime
from langchain_ollama import ChatOllama
from gtts import gTTS

app = Flask(__name__)
app.secret_key = "elderly-rpg-secret-key"

llm = ChatOllama(model="llama3.1:8b", temperature=0.7)

OVERALL_PROMPT = """You are a warm, elderly-friendly RPG storyteller.
- Write ONLY in script format: [Stage direction] Character: "Dialogue"
- Use very short sentences and simple everyday language.
- Tone: calm, supportive, positive and hopeful. Never violence, sadness or fear.
- Each scene: 60–150 words.
- End every scene with exactly 2 or 3 simple clear choices.
- Format choices exactly like this at the very end:
1. Choice one here
2. Choice two here
3. Choice three here
- The entire story must have exactly {target_length} scenes.
- Maintain perfect continuity using this history: {history}
- NEVER write "Scene X" at the beginning of the script."""

ENDING_PROMPT = """You are a warm, elderly-friendly storyteller.
Using this story summary and context:

{history}

Write a FINAL epilogue for the story in ONLY 2 to 4 short, simple sentences.
- Make it calm, gentle, positive and hopeful.
- No new events, just a peaceful wrap-up and reflection.
- Do NOT include any choices or bullet points.
- Do NOT mention "scene" or "epilogue" in the text.
Just write the ending text directly.
"""

THEME_PROMPTS = {
    "peaceful village": "Theme: Peaceful post-war village life. Focus on rebuilding homes together, planting crops, helping neighbors, children playing, nature sounds, warm sunlight, simple daily joys, old friendships, community meals, flowers blooming, gentle laughter. Characters: kind elderly villagers, friendly grandparents, curious children. Tone: nostalgic, peaceful, warm, hopeful.",
    "romantic": "Theme: Gentle romantic love story for seniors. Focus on sweet shared memories, caring for each other, quiet moments together, second chances at love, holding hands, walking in the park, family warmth, gentle affection, lifelong companionship. Characters: loving elderly couples, supportive adult children, warm-hearted neighbors. Tone: tender, heartwarming, respectful, peaceful.",
    "modern living life": "Theme: Modern everyday senior life. Focus on enjoying retirement, time with grandchildren, healthy morning walks, community center activities, simple technology, gardening on balcony, trying new recipes, relaxing hobbies. Characters: active seniors, loving family members, friendly neighbors, grandchildren. Tone: cheerful, practical, uplifting, light-hearted."
}

def generate_audio(script, scene_num):
    # ADDED: Use per-story audio folder if available
    audio_folder = session.get("audio_folder", "static/audio/english")
    os.makedirs(audio_folder, exist_ok=True)
    path = f"{audio_folder}/scene{scene_num}.mp3"
    tts = gTTS(text=script, lang='en', slow=True)
    tts.save(path)
    return path

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session.clear()
        session["topic"] = request.form.get("topic")
        length = request.form.get("length")
        custom = request.form.get("length_custom")
        session["target_length"] = int(custom) if custom and custom.isdigit() else int(length or 15)
        
        # Scene number represents the scene we are ABOUT to generate. Starts at 1.
        session["scene_num"] = 1
        session["history_summary"] = "Story just started."
        
        # Store full story log (scenes plus user choices).
        session["full_story_log"] = []
        
        # ADDED: Create unique audio folder for this story
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session["audio_folder"] = f"static/audio/english/story_{timestamp}"
        os.makedirs(session["audio_folder"], exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session["history_filename"] = f"history/English/ENG_history_{timestamp}.txt"
        os.makedirs("history", exist_ok=True)
        with open(session["history_filename"], "w", encoding="utf-8") as f:
            f.write(f"=== NEW STORY STARTED - {timestamp} ===\n\n")
        return redirect(url_for("game"))
    return render_template("start_eng.html")

@app.route("/game", methods=["GET", "POST"])
def game():
    if "topic" not in session:
        return redirect(url_for("index"))

    current_scene_num = session.get("scene_num", 1)

    # --- Step 1: Process the PAST action (if any) ---
    if request.method == "POST":
        choice = request.form.get("choice")
        previous_scene_text = session.get("last_scene", "")

        if previous_scene_text and choice:
            # Add the user's choice to the log for the PREVIOUS scene
            log_entry = f"\n\n[User Choice: {choice}]\n\n"
            session["full_story_log"].append(log_entry)
            session.modified = True

            # Update the summary based on the choice made
            summary_prompt = (
                f"Previous summary: {session['history_summary']}\n"
                f"New scene: {previous_scene_text}\n"
                f"Choice made: {choice}\n"
                "Respond with ONLY 2-3 sentence summary. No extra words."
            )
            new_summary = llm.invoke(summary_prompt).content.strip()
            session["history_summary"] = new_summary
            with open(session["history_filename"], "a", encoding="utf-8") as f:
                f.write(f"Scene {current_scene_num - 1} | Summary: {new_summary}\n\n")

    # --- FIXED: Correct ending logic (now ends AFTER the final scene) ---
    # If the user has just made a choice on the LAST scene, go to ending
    if current_scene_num > session["target_length"]:
        os.makedirs("log", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        full_story_text = "".join(session.get("full_story_log", []))

        with open(f"log/English/story_{timestamp}.txt", "w", encoding="utf-8") as f:
            f.write(
                f"Title: {session.get('story_title', 'Untitled')}\n"
                f"Theme: {session['topic']}\n"
                f"Total Scenes: {session['target_length']}\n\n"
            )
            f.write(full_story_text)

        # Generate positive ending
        ending_prompt = ENDING_PROMPT.format(history=session["history_summary"])
        positive_ending = llm.invoke(ending_prompt).content.strip()
            
        return render_template(
            "end_eng.html",
            positive_ending=positive_ending
        )

    # --- Step 2: Generate the CURRENT scene ---
    base = OVERALL_PROMPT.format(
        target_length=session["target_length"],
        history=session["history_summary"]
    )
    topic_prompt = THEME_PROMPTS[session["topic"]]
    full_prompt = base + "\n" + topic_prompt

    response = llm.invoke(full_prompt).content.strip()

    # Remove any leading "Scene X" if model adds it
    script = response.split("\n", 1)[-1].strip() if response.startswith("Scene") else response

    # Parse choices
    choices = [
        line.strip()
        for line in response.split("\n")[-6:]
        if line.strip() and line.lstrip()[0].isdigit()
    ]

    # --- Step 3: Store results ---
    session["last_scene"] = script
    session["full_story_log"].append(script)
    
    audio_path = generate_audio(script, current_scene_num)

    if "story_title" not in session:
        session["story_title"] = llm.invoke(
            f"Give a short warm title (max 6 words) for a {session['topic']} story."
        ).content.strip()

    data = {
        "story_title": session["story_title"],
        "character": "Elderly Narrator",
        "script": script,
        "choices": choices[:3],
        "audio": audio_path,
        "scene_num": current_scene_num,
        "total_scenes": session["target_length"]
    }
    
    # Increment for next scene
    session["scene_num"] = current_scene_num + 1
    session.modified = True
    
    return render_template("game_eng.html", **data)

if __name__ == "__main__":
    app.run(debug=True, port=5000)