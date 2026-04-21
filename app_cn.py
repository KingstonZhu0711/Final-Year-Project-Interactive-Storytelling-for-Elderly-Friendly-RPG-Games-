# app_cn.py
# Updated: 30 March 2026, 17:00 HKT - Chinese scene length reduced to 30-60 characters

from flask import Flask, render_template, request, session, redirect, url_for
import os
from datetime import datetime
from langchain_ollama import ChatOllama
from gtts import gTTS

app = Flask(__name__)
app.secret_key = "elderly-rpg-secret-key"

# ↓↓↓ CHANGED: lower temperature for stricter formatting ↓↓↓
llm = ChatOllama(model="qwen2:7b", temperature=0.2)

# ================== CHINESE PROMPTS ==================
# ↓↓↓ CHANGED: OVERALL_PROMPT updated to be more explicit and include a concrete format example ↓↓↓
OVERALL_PROMPT = """你是溫暖、長者友好的RPG故事講述者。

輸出格式要求（非常重要，嚴格遵守）：
1. 只能使用這種格式：[舞台指示] 角色：「對話」
2. 不能使用任何標題、列表、角色介紹或說明文字。
3. 不能使用「###」「**」「- 」等任何Markdown格式。
4. 每個場景只用 2–4 行，並且每一行都必須是「[舞台指示] 角色：「對話」」形式。
5. 每個場景總字數為 50–90 個中文字（含標點）。
6. 每個場景結尾必須有 2 或 3 個選擇，格式如下（每行一個）：
1. 選擇一
2. 選擇二
3. 選擇三
7. 絕對不要在最前面寫「場景 X」或任何場景編號，直接寫內容。
8. 不要寫任何解釋、標註或額外說明，只輸出場景內容和最後的選擇。

格式範例（僅作為格式示範，不要照抄內容）：
[清晨公園，小路上] 阿林：「今天天氣很舒服，我們慢慢走。」
[清晨公園，長椅旁] 阿美：「是啊，陽光很溫暖，我們不趕時間。」

1. 阿林提議去喝豆漿。
2. 阿美想去看小朋友玩耍。
3. 他們決定坐下來休息一下。

你的任務：
- 使用非常短的句子和簡單日常語言。
- 語調必須平靕、支持、積極和充滿希望。絕對不要出現暴力、悲傷或恐懼。
- 每次生成只生成一个场景，三个选项
- 每個場景結尾必須有3個簡單清晰的選擇。
- 整個故事必須剛好有 {target_length} 個場景。
- 使用此歷史保持連貫性： {history}
- 絕對不要在開頭寫「場景 X」，直接寫故事內容。
- 直接輸出下一個場景的完整文字，不要解釋，不要加任何其他內容。"""

ENDING_PROMPT = """你是溫暖、長者友好的故事講述者。
使用以下故事摘要和上下文：

{history}

這是最後一個場景。
請用2到3句簡短、溫柔、積極和充滿希望的句子結束故事。
不要加入新事件，只做和平的總結和反思。
不要包含任何選擇或項目符號。
直接寫結尾文字即可。
"""

THEME_PROMPTS = {
    "peaceful village": "主題：戰後平靜村莊生活。重點在於一起重建家園、種植農作物、幫助鄰居、孩子們玩耍、自然聲音、溫暖陽光、簡單日常快樂、老朋友、社區聚餐、花朵盛開、溫柔笑聲。角色：善良的長者村民、友善的祖父母、好奇的孩子。語調：懷舊、平靜、溫暖、充滿希望。",
    "romantic": "主題：長者溫柔浪漫愛情故事。重點在於甜蜜共同回憶、互相照顧、寧靜相處時刻、愛情第二次機會、手牽手、在公園散步、家庭溫暖、溫柔情感、終生陪伴。角色：相愛的長者夫妻、支持的成年子女、溫暖的鄰居。語調：溫柔、溫馨、尊重、平靜。",
    "modern living life": "主題：現代長者日常生活。重點在於享受退休生活、與孫子孫女相處、健康晨運、社區中心活動、簡單科技使用、陽台種花、嘗試新食譜、放鬆興趣。角色：活躍的長者、愛的家人、友善的鄰居、孫子孫女。語調：開朗、實用、鼓舞人心、輕鬆。"
}

def generate_audio(script, scene_num):
    audio_folder = session.get("audio_folder", "static/audio/chinese")
    os.makedirs(audio_folder, exist_ok=True)
    path = f"{audio_folder}/scene{scene_num}.mp3"
    tts = gTTS(text=script, lang='zh-CN', slow=True)
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
        
        session["scene_num"] = 1
        session["history_summary"] = "Story just started."
        
        session["full_story_log"] = []
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session["audio_folder"] = f"static/audio/chinese/story_{timestamp}"
        os.makedirs(session["audio_folder"], exist_ok=True)
        
        session["log_filename"] = f"log/Chinese/CHN_{timestamp}_Log.txt"
        session["history_filename"] = f"history/Chinese/CHN_{timestamp}_History.txt"
        
        os.makedirs("log/Chinese", exist_ok=True)
        os.makedirs("history/Chinese", exist_ok=True)
        
        with open(session["history_filename"], "w", encoding="utf-8") as f:
            f.write(f"=== NEW STORY STARTED - {timestamp} ===\n\n")
        return redirect(url_for("game"))
    return render_template("start_cn.html")

@app.route("/game", methods=["GET", "POST"])
def game():
    if "topic" not in session:
        return redirect(url_for("index"))

    current_scene_num = session.get("scene_num", 1)

    if request.method == "POST":
        choice = request.form.get("choice")
        previous_scene_text = session.get("last_scene", "")

        if previous_scene_text and choice:
            log_entry = f"\n\n[User Choice: {choice}]\n\n"
            session["full_story_log"].append(log_entry)
            session.modified = True

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

    if current_scene_num > session["target_length"]:
        os.makedirs("log/Chinese", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        full_story_text = "".join(session.get("full_story_log", []))

        with open(session["log_filename"], "w", encoding="utf-8") as f:
            f.write(
                f"Title: {session.get('story_title', 'Untitled')}\n"
                f"Theme: {session['topic']}\n"
                f"Total Scenes: {session['target_length']}\n\n"
            )
            f.write(full_story_text)

        ending_prompt = ENDING_PROMPT.format(history=session["history_summary"])
        positive_ending = llm.invoke(ending_prompt).content.strip()
            
        return render_template(
            "end_cn.html",
            positive_ending=positive_ending
        )

    base = OVERALL_PROMPT.format(
        target_length=session["target_length"],
        history=session["history_summary"]
    )
    topic_prompt = THEME_PROMPTS[session["topic"]]
    full_prompt = base + "\n" + topic_prompt

    response = llm.invoke(full_prompt).content.strip()

    # ↓↓↓ NEW: light post-processing to remove markdown-like noise the model might still emit ↓↓↓
    for junk in ["###", "**角色", "**對話", "**对话", "** 角色", "**角色：", "**對話：", "**对话："]:
        response = response.replace(junk, "")
    # Remove lines that start with common markdown symbols
    filtered_lines = [
        line for line in response.split("\n")
        if not line.strip().startswith(("#", "-", "*"))
    ]
    response = "\n".join(filtered_lines).strip()

    # ↓↓↓ UPDATED: script extraction stays simple – we already told the model not to use "場景" headings ↓↓↓
    script = response

    # ↓↓↓ UPDATED: stricter choice extraction, matching "1. 選擇..." style ↓↓↓
    lines = response.split("\n")
    raw_choices = []
    for line in lines:
        s = line.strip()
        # look for pattern "1. " or "2. " or "3. "
        if len(s) >= 3 and s[0] in "123" and s[1:3] == ". ":
            raw_choices.append(s)
    # Choices should be last 2–3 such lines; keep order
    choices = raw_choices[-3:] if len(raw_choices) >= 2 else raw_choices
    choices = choices[:3]

    session["last_scene"] = script
    session["full_story_log"].append(script)
    
    audio_path = generate_audio(script, current_scene_num)

    if "story_title" not in session:
        session["story_title"] = llm.invoke(
            f"Give a short warm title (max 6 words) for a {session['topic']} story, in chinese."
        ).content.strip()

    data = {
        "story_title": session["story_title"],
        "character": "Elderly Narrator",
        "script": script,
        "choices": choices,
        "audio": audio_path,
        "scene_num": current_scene_num,
        "total_scenes": session["target_length"]
    }
    
    session["scene_num"] = current_scene_num + 1
    session.modified = True
    
    return render_template("game_cn.html", **data)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
