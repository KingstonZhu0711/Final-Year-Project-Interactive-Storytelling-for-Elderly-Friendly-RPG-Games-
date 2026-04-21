# bert_cn.py
# Updated: 2 April 2026
# Reads gold standard from gold_standards/chinese/ TXT files

from bert_score import score
import os
from datetime import datetime

LOG_FOLDER = r"C:\Users\Zhu Jin Shun\Desktop\COMP 4913 Capstone Project\FYP Work\Work\Code\elderly-rpg-prototype\New Code\log\Chinese"
GOLD_FOLDER = r"C:\Users\Zhu Jin Shun\Desktop\COMP 4913 Capstone Project\FYP Work\Work\Code\elderly-rpg-prototype\New Code\gold_standards\chinese"
REPORT_FOLDER = r"C:\Users\Zhu Jin Shun\Desktop\COMP 4913 Capstone Project\FYP Work\Work\Code\elderly-rpg-prototype\New Code\report"

# Theme to gold-standard filename mapping
GOLD_FILES = {
    "peaceful village": "gold_peaceful_village.txt",
    "romantic": "gold_romantic.txt",
    "modern living life": "gold_modern_living.txt"
}

# Find the newest Chinese log file
log_files = [f for f in os.listdir(LOG_FOLDER) if f.startswith("CHN_") and f.endswith("_Log.txt")]
if not log_files:
    print("No Chinese log files found in log/Chinese folder.")
    exit()

latest_log = max(log_files, key=lambda f: os.path.getctime(os.path.join(LOG_FOLDER, f)))
log_path = os.path.join(LOG_FOLDER, latest_log)

print(f"Evaluating latest Chinese log file: {latest_log}\n")

with open(log_path, "r", encoding="utf-8") as f:
    log_content = f.read()

# Detect theme
theme = "peaceful village"
if "Theme: peaceful village" in log_content:
    theme = "peaceful village"
elif "Theme: romantic" in log_content:
    theme = "romantic"
elif "Theme: modern living life" in log_content:
    theme = "modern living life"

# Load gold standard from TXT file
gold_filename = GOLD_FILES[theme]
gold_path = os.path.join(GOLD_FOLDER, gold_filename)

with open(gold_path, "r", encoding="utf-8") as f:
    gold_standard = f.read().strip()

print(f"Detected Theme: {theme} → Using {gold_filename}\n")

# Extract story text
if "Total Scenes:" in log_content:
    story_text = log_content.split("Total Scenes:", 1)[1].strip()
else:
    story_text = log_content

# Compute BERTScore
P, R, F1 = score([story_text], [gold_standard], lang="zh", verbose=True)

print("\n" + "="*70)
print("BERTScore Evaluation Report - CHINESE VERSION")
print("="*70)
print(f"Story File      : {latest_log}")
print(f"Theme           : {theme}")
print(f"Precision (P)   : {P.mean().item():.4f}")
print(f"Recall (R)      : {R.mean().item():.4f}")
print(f"F1 Score        : {F1.mean().item():.4f}")
print("="*70)

# Save report
os.makedirs(REPORT_FOLDER, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
report_path = os.path.join(REPORT_FOLDER, f"CNY_{timestamp}_report.txt")

with open(report_path, "w", encoding="utf-8") as f:
    f.write(f"BERTScore Evaluation Report - CHINESE VERSION - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"Story File      : {latest_log}\n")
    f.write(f"Theme           : {theme}\n")
    f.write(f"Precision (P)   : {P.mean().item():.4f}\n")
    f.write(f"Recall (R)      : {R.mean().item():.4f}\n")
    f.write(f"F1 Score        : {F1.mean().item():.4f}\n")
    f.write(f"\nGold Standard Used: {gold_filename}\n")

print(f"\nChinese report saved to: {report_path}")