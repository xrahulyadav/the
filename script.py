#!/usr/bin/env python3
"""
Instagram Threads Auto-Posting Engine (Pure GitHub Actions Automation)
======================================================================
- Style: Line-by-line modern founder / biohacker aesthetic (Marc Lou style)
- Engine: Google Gemini AI (gemini-2.5-flash with gemini-3.8-flash fallback)
- Hard constraint: STRICTLY between 300 and 350 total characters with emojis
- Publishing: 2-step Meta Threads Graph API container creation & publishing
- Target: Threads User ID 29410042778679242
- Persistence: Updates posts_log.json for GitHub Pages static dashboard consumption
"""

import datetime
import json
import os
import random
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests

# Ensure UTF-8 stdout encoding on all platforms (prevents Windows cp1252 emoji crash)
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Try loading .env for local testing if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Paths
BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = BASE_DIR / "posts_log.json"

# Credentials from Environment (injected by GitHub Repository Secrets or local .env)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
THREADS_ACCESS_TOKEN = os.getenv("THREADS_ACCESS_TOKEN", "").strip()
THREADS_USER_ID = os.getenv("THREADS_USER_ID", "29410042778679242").strip()

# Curated High-Converting Line-by-Line Founder Posts (Marc Lou Style)
# All strictly between 300 and 350 characters total
CURATED_FOUNDER_POSTS = [
    (
        "✨ Daily Biohacking Protocol ✨\n\n"
        "What 90 days of science-backed habits did:\n"
        "🩺 Deep Sleep: +38 mins slow-wave recovery\n"
        "🧠 Focus: Zero afternoon brain fog crashes\n"
        "🏃 Zone 2: Mitochondrial density doubled\n"
        "🥑 Gut Health: 30+ diverse plant fibers weekly\n\n"
        "Your biology reflects what you do daily. Prioritize vitality 🧬."
    ),
    (
        "⚡ My 5 Non-Negotiable Longevity Rules ⚡\n\n"
        "How I keep my biological age 7 years younger:\n"
        "☀️ Morning: 15 mins direct solar photons\n"
        "💧 Hydration: Sodium + potassium cellular pump\n"
        "🏃 Cardio: 150 mins weekly conversational Zone 2\n"
        "💤 Evening: Zero blue photons 90m before bed\n\n"
        "Consistency compounds into extraordinary vitality 🧬."
    ),
    (
        "✨ The High-Performance Health Stack ✨\n\n"
        "What I track daily to stay sharp at 100%:\n"
        "🧠 Brain: Magnesium L-threonate for NMDA clarity\n"
        "🥑 Nutrition: 40g protein pulses every 4 hours\n"
        "⚡ Energy: Heat shock proteins via 20m sauna\n"
        "💤 Recovery: 8.2 hours slow-wave sleep score\n\n"
        "Take care of your cells, mind handles the rest 🧬."
    ),
    (
        "🩺 Rebuilding My Baseline Vitality 🩺\n\n"
        "The routine that transformed my biomarkers:\n"
        "☀️ 07:00 AM: Retinal solar photons + hydration 💧\n"
        "🏃 12:00 PM: 30m resistance training & GLUT4\n"
        "🧠 03:00 PM: Cold thermogenesis dopamine spike\n"
        "💤 10:30 PM: Glymphatic fluid clearance mode\n\n"
        "Small biological inputs create massive life leverage ⚡."
    ),
    (
        "✨ How I Optimized My Energy Engine ✨\n\n"
        "My daily physiological biomarkers checklist:\n"
        "⚡ Cellular ATP: 5g creatine monohydrate\n"
        "💧 Electrolytes: 500mg sodium in morning water\n"
        "🏃 Mitochondria: 45m conversational Zone 2 cardio\n"
        "💤 Recovery: 65°F cool room for deep REM sleep\n\n"
        "Daily micro-habits yield exponential vitality 🧬."
    ),
    (
        "🧠 Upgrading Cerebral Metabolism 🧠\n\n"
        "How I eliminated mental fatigue completely:\n"
        "☀️ Sunlight: Cortisol awakening pulse at 7 AM\n"
        "💧 Hydration: Celtic sea salt + magnesium glycinate\n"
        "🏃 Movement: 10m post-meal glucose walking\n"
        "💤 Sleep: Consistent circadian sleep architecture\n\n"
        "Protect your cognitive hardware every single day ⚡."
    ),
    (
        "✨ The Founder Cellular Longevity Stack ✨\n\n"
        "How I maintain peak stamina building daily:\n"
        "🩺 Recovery: HRV tracking & vagus nerve stimulation\n"
        "🥑 Fuel: Whole foods & polyphenol diversity\n"
        "🏃 Training: Heavy compound lifts & Zone 2 cardio\n"
        "💤 Rest: 8 hours restorative deep sleep cycles\n\n"
        "Your health is your greatest compounding asset 🧬."
    )
]

SYSTEM_PROMPT = """You are an elite health founder and biohacking researcher writing high-engagement posts for Instagram Threads in the viral style of Marc Lou and Andrew Huberman.

FORMAT REQUIREMENTS (LINE-BY-LINE AESTHETIC):
Structure the post cleanly across multiple lines:
Line 1: Punchy, curiosity-driven header with emojis (e.g. ✨ The Daily Longevity Protocol ✨)
Line 2: Blank line
Line 3: Short context line (e.g. What tracking my health biomarkers revealed:)
Lines 4-7: Crisp, bulleted takeaways with emoji bullets (🩺, 🧠, 🏃, 🥑, ⚡, 💤, ☀️, 💧)
Line 8: Blank line
Line 9: Punchy concluding takeaway on daily compounding biological habits.

CRITICAL HARD CONSTRAINT (NON-NEGOTIABLE):
The total length of the entire output MUST BE STRICTLY BETWEEN 300 AND 350 TOTAL CHARACTERS (including letters, spaces, emojis, and newlines).
- NEVER output less than 300 characters.
- NEVER output more than 350 characters.
- Zero hashtags. Zero surrounding quotes. Zero conversational preamble.
"""


def enforce_exact_char_range(text: str, min_chars: int = 300, max_chars: int = 350) -> str:
    """
    Guarantees line-by-line formatting strictly satisfies 300 <= len <= 350.
    Never resorts to repetitive emoji spam.
    """
    cleaned = text.strip().strip('"\'“”')
    length = len(cleaned)

    if min_chars <= length <= max_chars:
        return cleaned

    # If exceeding max_chars, trim at last sentence boundary or select curated post
    if length > max_chars:
        # Try trimming trailing text to fit
        lines = cleaned.split("\n")
        trimmed = ""
        for line in lines:
            candidate = (trimmed + "\n" + line).strip() if trimmed else line
            if len(candidate) <= max_chars:
                trimmed = candidate
            else:
                break
        if min_chars <= len(trimmed) <= max_chars:
            return trimmed

    # If below min_chars or trimming broke structure, return one of our curated line-by-line posts
    return random.choice(CURATED_FOUNDER_POSTS)


def generate_wellness_insight() -> str:
    """Generate high-impact health micro-article in line-by-line founder format."""
    if not GEMINI_API_KEY or not GEMINI_API_KEY.startswith("AIzaSy"):
        print("[AI CORE] Gemini API Key unconfigured or non-AIStudio format. Using curated Marc Lou line-by-line post.")
        return random.choice(CURATED_FOUNDER_POSTS)

    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"[AI CORE ERROR] Client init error: {e}. Using curated line-by-line post.")
        return random.choice(CURATED_FOUNDER_POSTS)

    user_prompt = (
        "Write a line-by-line founder biohacking post for Instagram Threads.\n"
        "Include a header with emojis, 4 bullet lines (🩺, 🧠, 🏃, 🥑), and a closing takeaway.\n"
        "MANDATORY: Total length MUST BE STRICTLY BETWEEN 300 AND 350 CHARACTERS."
    )

    model_candidates = [GEMINI_MODEL, "gemini-2.5-flash", "gemini-3.8-flash", "gemini-1.5-flash"]
    seen = set()
    model_candidates = [m for m in model_candidates if m and not (m in seen or seen.add(m))]

    for model_name in model_candidates:
        try:
            print(f"[AI CORE] Querying Gemini model: {model_name}...")
            response = client.models.generate_content(
                model=model_name,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.7,
                    max_output_tokens=180
                )
            )
            raw = (response.text or "").strip().strip('"\'“”')
            raw = re.sub(r'#\w+', '', raw).strip()

            if 300 <= len(raw) <= 350:
                print(f"[AI CORE SUCCESS] Valid line-by-line post generated ({len(raw)} chars).")
                return raw

            print(f"[AI CORE] Output from {model_name} is {len(raw)} chars. Validating bounds.")
            candidate = enforce_exact_char_range(raw)
            if 300 <= len(candidate) <= 350:
                return candidate
        except Exception as e:
            print(f"[AI CORE WARN] Model {model_name} error: {e}")
            continue

    return random.choice(CURATED_FOUNDER_POSTS)


def publish_to_threads(text: str) -> Tuple[str, Optional[str], Optional[str]]:
    """
    Publish content to Instagram Threads via 2-step Graph API:
      Step A: POST /{user_id}/threads (Creates Media Container)
      Step B: POST /{user_id}/threads_publish (Publishes Media Container)
    """
    if not THREADS_ACCESS_TOKEN or not THREADS_USER_ID:
        print("[THREADS API WARN] Missing THREADS_ACCESS_TOKEN or THREADS_USER_ID.")
        return "FAILED", None, "Missing THREADS_ACCESS_TOKEN or THREADS_USER_ID in GitHub Secrets."

    base_url = f"https://graph.threads.net/v1.0/{THREADS_USER_ID}"

    try:
        # Step A: Create Media Container
        container_payload = {
            "media_type": "TEXT",
            "text": text,
            "access_token": THREADS_ACCESS_TOKEN
        }

        print(f"[THREADS API] Step A: Creating container for user {THREADS_USER_ID} ({len(text)} chars)...")
        step_a_res = requests.post(f"{base_url}/threads", data=container_payload, timeout=30)
        res_a_json = step_a_res.json()

        if step_a_res.status_code != 200 or "id" not in res_a_json:
            err_msg = res_a_json.get("error", {}).get("message", step_a_res.text)
            print(f"[THREADS API ERROR - STEP A] {err_msg}", file=sys.stderr)
            return "FAILED", None, f"Container creation failed: {err_msg}"

        creation_id = res_a_json["id"]
        print(f"[THREADS API] Step A Succeeded. Container Creation ID: {creation_id}")

        # Step B: Publish Media Container
        publish_payload = {
            "creation_id": creation_id,
            "access_token": THREADS_ACCESS_TOKEN
        }

        print(f"[THREADS API] Step B: Publishing container {creation_id}...")
        step_b_res = requests.post(f"{base_url}/threads_publish", data=publish_payload, timeout=30)
        res_b_json = step_b_res.json()

        if step_b_res.status_code != 200 or "id" not in res_b_json:
            err_msg = res_b_json.get("error", {}).get("message", step_b_res.text)
            print(f"[THREADS API ERROR - STEP B] {err_msg}", file=sys.stderr)
            return "FAILED", None, f"Publishing failed: {err_msg}"

        published_post_id = res_b_json["id"]
        threads_url = f"https://www.threads.net/post/{published_post_id}"
        print(f"[THREADS API SUCCESS] Post live on Threads: {published_post_id}")
        print(f"[THREADS URL] {threads_url}")
        return "SUCCESS", published_post_id, threads_url

    except requests.exceptions.RequestException as e:
        print(f"[THREADS API EXCEPTION] Network error: {e}", file=sys.stderr)
        return "FAILED", None, f"Network exception: {str(e)}"


def load_logs() -> List[Dict[str, Any]]:
    """Load existing logs from posts_log.json supporting array or structured format."""
    if not LOG_FILE.exists():
        return []
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            content = json.load(f)
            if isinstance(content, list):
                return content
            elif isinstance(content, dict):
                return content.get("posts", [])
            return []
    except Exception as e:
        print(f"[LOG LOAD WARN] Failed reading posts_log.json ({e}). Starting fresh array.")
        return []


def save_logs(posts: List[Dict[str, Any]]):
    """Write updated logs array to posts_log.json atomically."""
    temp_file = BASE_DIR / "posts_log.tmp.json"
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
    temp_file.replace(LOG_FILE)
    print(f"[DATA PERSISTENCE] Successfully updated {LOG_FILE} ({len(posts)} total entries).")


def main():
    print("=" * 65)
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    print(f" [GITHUB ACTIONS DISPATCH] Threads Auto-Poster Execution")
    print(f" Target User ID: {THREADS_USER_ID}")
    print(f" Time: {utc_now.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 65)

    # 1. Generate line-by-line micro-article
    post_text = generate_wellness_insight()
    char_len = len(post_text)
    print(f"[AI GENERATOR] Generated post ({char_len} chars):")
    print("-" * 50)
    print(post_text)
    print("-" * 50)

    # 2. Publish to Instagram Threads Graph API
    status, post_id, detail = publish_to_threads(post_text)

    threads_url = detail if status == "SUCCESS" else None
    error_msg = detail if status == "FAILED" else None

    # 3. Create log record
    entry = {
        "id": post_id or f"err_{int(utc_now.timestamp())}",
        "text": post_text,
        "char_count": char_len,
        "status": status,
        "timestamp": utc_now.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "threads_url": threads_url or "https://www.threads.net",
        "error": error_msg
    }

    # 4. Save to posts_log.json
    logs = load_logs()
    logs.insert(0, entry)
    save_logs(logs)

    print("=" * 65)
    print(f" [COMPLETED] Status: {status} | Post ID: {entry['id']}")
    print("=" * 65)


if __name__ == "__main__":
    main()
