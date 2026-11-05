#!/usr/bin/env python3
"""
Instagram Threads Auto-Posting Engine (Pure GitHub Actions Automation)
======================================================================
- Repository: xrahulyadav/the
- Engine: Google Gemini AI (gemini-2.5-flash with gemini-3.8-flash fallback)
- Hard constraint: STRICTLY between 300 and 350 total characters with emojis
- Publishing: 2-step Meta Threads Graph API container creation & publishing
- Target: Threads User ID 29410042778679242
- Persistence: Updates posts_log.json for GitHub Pages static dashboard consumption
- Triggered automatically via GitHub Actions Cron (every 1 hour) or manual dispatch
"""

import datetime
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests

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
GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    "AQ.Ab8RN6I59zPQiFLybXc1VYlQxoMy0BLl2zASfKMoEVakXgzzwQ"
).strip()

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()

THREADS_ACCESS_TOKEN = os.getenv(
    "THREADS_ACCESS_TOKEN",
    "THAAUSRZBZAQCjhBYmFpWVYxcTIyR05SYXBYNktPcUcwSkhVTzZAndFdBOWJ4Y0NoT3lUU1ctV2ZAzeU5PSHNtTXducFhXdExETWNYbVAzTEtxMHlJNEc1VVN1VVBaakVuRzJaZAnVsLVFVcEUxU0I5SXQzUVJROGtwMHB0NFg5dEgxOWNBd1UwbWR1b3FUWGxFTERZANk5lQy1COXNaekJhM3FsOVpvaEdUMzgZD"
).strip()

THREADS_USER_ID = os.getenv("THREADS_USER_ID", "29410042778679242").strip()

# Evidence-based Health, Longevity & Wellness Topics
WELLNESS_TOPICS = [
    "Zone 2 cardiovascular training, mitochondrial biogenesis, and metabolic flexibility",
    "Circadian biology, morning solar photon exposure, and cortisol awakening rhythm",
    "Creatine monohydrate beyond muscle: neuroprotection and cerebral ATP recycling",
    "Slow-wave sleep architecture, glymphatic fluid brain clearance, and growth hormone release",
    "Gut microbiota diversity, short-chain fatty acids (SCFAs), and intestinal mucosal barrier",
    "Magnesium L-threonate vs Glycinate for NMDA receptor modulation and deep nervous system recovery",
    "Resistance training as metabolic medicine: GLUT4 translocation and insulin sensitivity",
    "Cellular hydration: the sodium-potassium ATPase pump beyond pure tap water volume",
    "Heat shock proteins (HSP70) from infrared sauna therapy and cardiovascular longevity markers",
    "Cold water immersion: dopamine receptor density and noradrenaline release kinetics",
    "Omega-3 fatty acids (EPA/DHA), membrane fluidity, and systemic endothelial health",
    "Chronic low-grade stress: the cortisol-DHEA ratio and neuroplasticity preservation",
    "Intermittent fasting autophagy triggers and cellular senescent clearance benchmarks",
    "VO2 Max as the single strongest functional biomarker for longevity and biological age",
    "Vagus nerve stimulation, heart rate variability (HRV), and parasympathetic recovery",
    "Phytonutrient diversity: polyphenols, sulforaphane Nrf2 activation, and oxidative resilience",
    "Deep REM sleep cycles, memory consolidation, and prefrontal amygdala emotional calibration",
    "Postprandial glucose blunting: soleus pushups and 10-minute light walking kinetics"
]

SYSTEM_PROMPT = """You are an elite health scientist, longevity physician, and wellness researcher writing for Instagram Threads.
Your objective is to produce insightful, science-backed micro-insights on Health, Fitness, Nutrition, or Mental Wellness.

EMOJI STYLE:
Include 2 to 4 tasteful, engaging, and relevant emojis (e.g. 🧬, ⚡, 🥑, 🧠, 🏃, 💤, ☀️, 💧) naturally placed within the post to maximize engagement on Threads.

CRITICAL HARD CONSTRAINT (NON-NEGOTIABLE):
The total length of the entire output MUST BE STRICTLY BETWEEN 300 AND 350 TOTAL CHARACTERS.
Every single letter, number, space, emoji, and punctuation mark is counted.
- NEVER output less than 300 characters.
- NEVER output more than 350 characters.
- Return ONLY the exact post text with emojis. Zero hashtags. Zero surrounding quotes. Zero conversational preamble.
"""


def enforce_exact_char_range(text: str, min_chars: int = 300, max_chars: int = 350) -> str:
    """
    Guarantees text strictly satisfies min_chars <= len <= max_chars.
    Employs smart boundary trimming or complementary scientific takeaways.
    """
    cleaned = text.strip().strip('"\'“”')
    cleaned = re.sub(r'\s+', ' ', cleaned)
    length = len(cleaned)

    if min_chars <= length <= max_chars:
        return cleaned

    # Exceeding max_chars (350): Smart trim at sentence or word boundary
    if length > max_chars:
        sentences = re.split(r'([.!?]\s+)', cleaned)
        reconstructed = ""
        for i in range(0, len(sentences), 2):
            sentence = sentences[i]
            punct = sentences[i+1] if i+1 < len(sentences) else ""
            candidate = (reconstructed + sentence + punct).strip()
            if min_chars <= len(candidate) <= max_chars:
                return candidate
            if len(candidate) > max_chars:
                break
            reconstructed = candidate + " "

        words = cleaned.split()
        trimmed = ""
        for w in words:
            candidate = (trimmed + " " + w).strip() if trimmed else w
            if len(candidate) > (max_chars - 5):
                break
            trimmed = candidate

        trimmed = trimmed.rstrip(" ,;:-") + ". 🧬"
        if len(trimmed) > max_chars:
            trimmed = trimmed[:max_chars - 3].rstrip() + "..."
        if len(trimmed) < min_chars:
            pad = " Prioritize vitality and daily consistency ⚡."
            trimmed = (trimmed + pad)[:max_chars]
        return trimmed

    # Below min_chars (300): Complement with evidence-backed health takeaways
    takeaways = [
        " Daily micro-habits compound into extraordinary vitality 🧬. Prioritize recovery, hydration, and movement every day.",
        " Sustainable longevity is forged through consistent daily biological rhythms and intentional cellular rest ⚡.",
        " Small daily health interventions yield exponential cellular protection and mental clarity over time 🧠.",
        " Optimize your daily physiological inputs: deep hydration, sunlight, and restorative sleep architecture 💤.",
        " Consistent physical movement primes cerebral circulation and sustains cellular metabolic flexibility 🏃."
    ]

    for take in takeaways:
        candidate = (cleaned.rstrip('.') + '.' + take).strip()
        if min_chars <= len(candidate) <= max_chars:
            return candidate

    candidate = cleaned + " Maintain consistency and optimal vitality 🧬."
    if len(candidate) > max_chars:
        candidate = candidate[:max_chars]
    while len(candidate) < min_chars:
        candidate += " ⚡"
    return candidate[:max_chars]


def generate_wellness_insight() -> str:
    """Generate high-impact health micro-article using Gemini AI."""
    import random
    topic = random.choice(WELLNESS_TOPICS)

    user_prompt = (
        f"Generate an insightful, science-backed post on: {topic}.\n"
        f"Include 2 to 3 engaging, relevant emojis (e.g. 🧬, ⚡, 🥑, 🧠, 🏃, 💤, ☀️, 💧).\n"
        f"MANDATORY RULE: The total text length (including letters, spaces, emojis) "
        f"MUST BE STRICTLY BETWEEN 300 AND 350 CHARACTERS. Target ~325 characters."
    )

    if not GEMINI_API_KEY:
        print("[AI CORE WARN] GEMINI_API_KEY secret not found in environment. Using curated benchmark insight.")
        return enforce_exact_char_range(
            "Zone 2 cardio trains mitochondrial density and metabolic flexibility 🏃. By maintaining a conversational pace (60-70% max heart rate), muscle cells optimize fatty acid oxidation over glycogen reliance ⚡. 150 minutes weekly reduces all-cause mortality and bolsters daily endurance 🧬. Consistency compounds your cellular health."
        )

    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"[AI CORE ERROR] Could not initialize google-genai client: {e}")
        return enforce_exact_char_range(
            "Consistent physical movement and daily sunlight regulate your master biological clock ☀️. By aligning circadian rhythms, your brain optimizes neurogenesis, deep slow-wave sleep cycles, and cellular repair pathways 🧠. Small daily interventions create lasting systemic resilience and functional vitality 🧬."
        )

    model_candidates = [GEMINI_MODEL, "gemini-2.5-flash", "gemini-3.8-flash", "gemini-1.5-flash"]
    seen = set()
    model_candidates = [m for m in model_candidates if m and not (m in seen or seen.add(m))]

    candidate = ""
    for model_name in model_candidates:
        try:
            print(f"[AI CORE] Querying Gemini model: {model_name}...")
            response = client.models.generate_content(
                model=model_name,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.7,
                    max_output_tokens=160
                )
            )
            raw = (response.text or "").strip().strip('"\'“”')
            raw = re.sub(r'#\w+', '', raw).strip()

            if 300 <= len(raw) <= 350:
                print(f"[AI CORE SUCCESS] Valid post generated with {model_name} ({len(raw)} chars).")
                return raw

            candidate = raw
            print(f"[AI CORE] Output from {model_name} is {len(raw)} chars. Enforcing bounds.")
            break
        except Exception as e:
            print(f"[AI CORE WARN] Model {model_name} returned: {e}. Trying next candidate...")
            continue

    return enforce_exact_char_range(candidate or f"{topic} is fundamental for human vitality and long-term metabolic health.")


def publish_to_threads(text: str) -> Tuple[str, Optional[str], Optional[str]]:
    """
    Publish content to Instagram Threads via 2-step Graph API:
      Step A: POST /{user_id}/threads (Creates Media Container)
      Step B: POST /{user_id}/threads_publish (Publishes Media Container)
    """
    if not THREADS_ACCESS_TOKEN or not THREADS_USER_ID:
        print("[THREADS API WARN] Missing THREADS_ACCESS_TOKEN or THREADS_USER_ID. Generating simulated record.")
        mock_id = f"mock_{int(datetime.datetime.now().timestamp())}"
        return "SUCCESS", mock_id, f"https://www.threads.net/post/{mock_id}"

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

    # 1. Generate micro-article via Gemini
    post_text = generate_wellness_insight()
    char_len = len(post_text)
    print(f"[AI GENERATOR] Generated post ({char_len} chars):")
    print(f"\"{post_text}\"")

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
