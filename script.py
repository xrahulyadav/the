#!/usr/bin/env python3
"""
Instagram Threads Auto-Posting Engine (Pure GitHub Actions Automation)
======================================================================
- Style: Exact Marc Lou Builder & Health Biohacking Line-by-Line Aesthetic
- Model: Google Gemini Flash (gemini-2.5-flash / gemini-3.5 / gemini-3.8-flash)
- Hard constraint: STRICTLY between 300 and 350 total characters with emojis
- Structure:
    ✨ Header line with sparkles ✨
    It now tracks:
    🩺 Health/Sleep bullet
    🧠 Focus/Brain bullet
    🏃 Movement/Cardio bullet
    🥑 Nutrition bullet
    💧 Hydration bullet

    Reflective founder takeaway question or rule
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
QUEUE_FILE = BASE_DIR / "upcoming_queue.json"

# Credentials from Environment (injected by GitHub Repository Secrets or local .env)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
THREADS_ACCESS_TOKEN = os.getenv("THREADS_ACCESS_TOKEN", "").strip()
THREADS_USER_ID = os.getenv("THREADS_USER_ID", "29410042778679242").strip()

# Curated Line-by-Line Marc Lou Style Masterpieces (300 - 350 chars verified)
CURATED_MARC_LOU_POSTS = [
    (
        "✨ I rebuilt my personal health dashboard ✨\n"
        "It now tracks:\n"
        "🩺 My sleep: 8h restorative slow-wave cycles\n"
        "🧠 Brain focus: zero afternoon crash periods\n"
        "🏃 Zone 2: 150m conversational cardio weekly\n"
        "🥑 Nutrition: 30+ gut microbiome plants\n"
        "💧 Hydration: cellular electrolyte balance\n\n"
        "If you don't take care of your body, where will you live?"
    ),
    (
        "✨ I automated my entire health system ✨\n"
        "It now monitors:\n"
        "🩺 Biomarkers: HRV, VO2 Max, & cellular recovery\n"
        "☀️ Sunlight: 15m morning retinal photons\n"
        "⚡ Energy: 5g creatine monohydrate daily\n"
        "🏃 Training: heavy compound lifts + Zone 2\n"
        "💤 Sleep: zero blue photons before bed\n\n"
        "Treat your biology like production code: optimize daily inputs 🧬."
    ),
    (
        "✨ I turned my daily health into an operating system ✨\n"
        "It now tracks:\n"
        "🩺 Recovery: 8.4h deep slow-wave sleep\n"
        "🧠 Focus: zero afternoon energy crashes\n"
        "🏃 Movement: 150m weekly Zone 2 cardio\n"
        "🥑 Fuel: 40g protein pulses & polyphenols\n"
        "💧 Hydration: cellular electrolyte balance\n\n"
        "Small daily commits compound into superhuman vitality ⚡."
    ),
    (
        "✨ I rebuilt my morning routine from scratch ✨\n"
        "Here is what changed:\n"
        "☀️ 07:00 AM: 15m direct sunlight for cortisol rhythm\n"
        "💧 07:15 AM: 500ml water + Celtic sea salt\n"
        "🏃 12:00 PM: 30m Zone 2 cardio & GLUT4\n"
        "🧠 03:00 PM: cold shower dopamine reset\n"
        "💤 10:30 PM: 65°F cool room for REM sleep\n\n"
        "Your daily habits build your future biology 🧬."
    ),
    (
        "✨ Why I track my health biomarkers daily ✨\n"
        "My baseline metrics dashboard:\n"
        "🩺 Sleep score: 88+ via slow-wave glymphatic cycles\n"
        "🏃 VO2 Max: top 5% functional longevity marker\n"
        "🧠 Deep work: 4h uninterrupted morning flow\n"
        "🥑 Nutrition: 30+ diverse plant fibers weekly\n\n"
        "What gets measured gets optimized. Take care of your body ⚡."
    ),
    (
        "✨ Upgraded my personal biological hardware ✨\n"
        "My daily tracking stack:\n"
        "🩺 Heart rate: 48 bpm resting baseline\n"
        "⚡ Cellular ATP: 5g creatine + mitochondrial Zone 2\n"
        "🧠 Neuroplasticity: morning solar exposure + cold plunge\n"
        "🥑 Cellular gut: prebiotic fibers + polyphenols\n\n"
        "Your health is your highest-leverage investment. Guard it 🧬."
    )
]

SYSTEM_PROMPT = """You are Marc Lou writing an iconic, viral health & builder post for Instagram Threads.
You must follow this exact line-by-line format:

✨ [Personal action or milestone hook] ✨
It now tracks:
🩺 [Sleep/Health metric]: [details]
🧠 [Focus/Brain metric]: [details]
🏃 [Cardio/Workout metric]: [details]
🥑 [Nutrition/Diet metric]: [details]
💧 [Hydration/Recovery metric]: [details]

[Short reflective founder question or takeaway about daily compounding habits]

CRITICAL HARD CONSTRAINT (NON-NEGOTIABLE):
The total length of the entire output MUST BE STRICTLY BETWEEN 300 AND 350 TOTAL CHARACTERS (including spaces, newlines, and emojis). Target ~325 characters.
- Line-by-line structure with clean newlines.
- Zero hashtags. Zero surrounding quotes. Zero conversational preamble.
"""


def enforce_exact_char_range(text: str, min_chars: int = 300, max_chars: int = 350) -> str:
    """
    Guarantees line-by-line formatting strictly satisfies 300 <= len <= 350.
    Maintains clean Marc Lou line-by-line structure.
    """
    cleaned = text.strip().strip('"\'“”')
    length = len(cleaned)

    if min_chars <= length <= max_chars:
        return cleaned

    # If exceeding max_chars, trim gracefully at lines
    if length > max_chars:
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

    # If out of range or trimmed structure broke, pick from our curated Marc Lou master library
    return random.choice(CURATED_MARC_LOU_POSTS)


def generate_wellness_insight() -> str:
    """Generate high-impact health micro-article in exact Marc Lou line-by-line style."""
    if not GEMINI_API_KEY or not GEMINI_API_KEY.startswith("AIzaSy"):
        print("[AI CORE] Using curated Marc Lou line-by-line post (Gemini key unconfigured or awaiting AI Studio key).")
        return random.choice(CURATED_MARC_LOU_POSTS)

    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"[AI CORE ERROR] Client init error: {e}. Using curated Marc Lou post.")
        return random.choice(CURATED_MARC_LOU_POSTS)

    user_prompt = (
        "Write an exact Marc Lou style line-by-line post for Instagram Threads.\n"
        "Structure:\n"
        "✨ I rebuilt my personal health system ✨\n"
        "It now tracks:\n"
        "🩺 My sleep: [details]\n"
        "🧠 Brain focus: [details]\n"
        "🏃 Zone 2: [details]\n"
        "🥑 Nutrition: [details]\n\n"
        "[Reflective founder question or rule]\n\n"
        "MANDATORY: Total length MUST BE STRICTLY BETWEEN 300 AND 350 TOTAL CHARACTERS."
    )

    # Model hierarchy: try configured model, then 2.5-flash, 3.8-flash, 1.5-flash
    model_candidates = [
        GEMINI_MODEL,
        "gemini-2.5-flash",
        "gemini-3.8-flash",
        "gemini-1.5-flash"
    ]
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
                print(f"[AI CORE SUCCESS] Valid Marc Lou style post generated with {model_name} ({len(raw)} chars).")
                return raw

            print(f"[AI CORE] Output from {model_name} is {len(raw)} chars. Validating bounds.")
            candidate = enforce_exact_char_range(raw)
            if 300 <= len(candidate) <= 350:
                return candidate
        except Exception as e:
            print(f"[AI CORE WARN] Model {model_name} error: {e}")
            continue

    return random.choice(CURATED_MARC_LOU_POSTS)


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


def load_queue() -> List[Dict[str, Any]]:
    """Load upcoming scheduled posts queue."""
    if not QUEUE_FILE.exists():
        return []
    try:
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            content = json.load(f)
            if isinstance(content, list):
                return content
            elif isinstance(content, dict):
                return content.get("queue", [])
            return []
    except Exception as e:
        print(f"[QUEUE LOAD WARN] Failed reading upcoming_queue.json ({e}).")
        return []


def save_queue(queue: List[Dict[str, Any]]):
    """Write updated queue array to upcoming_queue.json atomically."""
    temp_file = BASE_DIR / "upcoming_queue.tmp.json"
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2, ensure_ascii=False)
    temp_file.replace(QUEUE_FILE)
    print(f"[DATA PERSISTENCE] Successfully updated {QUEUE_FILE} ({len(queue)} upcoming items).")


def parse_iso_datetime(dt_str: Optional[str]) -> Optional[datetime.datetime]:
    """Parse ISO datetime string into UTC datetime object safely."""
    if not dt_str:
        return None
    try:
        clean_str = dt_str.replace("Z", "+00:00")
        dt = datetime.datetime.fromisoformat(clean_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.timezone.utc)
        return dt.astimezone(datetime.timezone.utc)
    except Exception:
        return None


def main():
    print("=" * 65)
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    print(f" [GITHUB ACTIONS DISPATCH] Threads Auto-Poster Execution")
    print(f" Target User ID: {THREADS_USER_ID}")
    print(f" Time: {utc_now.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 65)

    # 1. Process Upcoming Scheduled Queue
    queue = load_queue()
    scheduled_item = None
    target_index = -1
    scheduled_for_info = None

    # Step A: Check for user-scheduled posts with explicit scheduled_at that are DUE (<= utc_now)
    due_custom_items = []
    for idx, item in enumerate(queue):
        sched_str = item.get("scheduled_at")
        if sched_str:
            dt = parse_iso_datetime(sched_str)
            if dt and dt <= utc_now:
                due_custom_items.append((idx, item, dt))

    if due_custom_items:
        # Sort by earliest scheduled date/time and pick the most urgent due item
        due_custom_items.sort(key=lambda x: x[2])
        target_index, scheduled_item, due_dt = due_custom_items[0]
        scheduled_for_info = scheduled_item.get("scheduled_display") or scheduled_item.get("scheduled_at")
        print(f"[QUEUE ENGINE] Processing DUE custom-scheduled post: {scheduled_item.get('id')} (Scheduled for: {scheduled_for_info})")
        queue.pop(target_index)
    else:
        # Step B: Pick the first queued item that is NOT time-locked to a future date
        for idx, item in enumerate(queue):
            sched_str = item.get("scheduled_at")
            if not sched_str:
                # Immediate next available run
                target_index = idx
                scheduled_item = queue.pop(target_index)
                scheduled_for_info = "Next Available Run"
                print(f"[QUEUE ENGINE] Dispatched immediate queue item: {scheduled_item.get('id')}")
                break
            else:
                dt = parse_iso_datetime(sched_str)
                if dt and dt > utc_now:
                    print(f"[QUEUE ENGINE] Post {item.get('id')} is scheduled for future date ({sched_str}). Preserving in queue.")
                    continue

    if scheduled_item:
        post_text = scheduled_item.get("text", "").strip()
        was_customized = scheduled_item.get("customized", False)
        queue_id = scheduled_item.get("id", "queue_item")

        # Validate content exists
        if not post_text:
            print("[QUEUE ENGINE WARN] Empty text in queue item, generating fresh post.")
            post_text = generate_wellness_insight()
            was_customized = False
        elif not (300 <= len(post_text) <= 350) and not was_customized:
            # If not customized by user and slightly outside bounds, format it
            post_text = enforce_exact_char_range(post_text)
    else:
        print("[QUEUE ENGINE] No pending or due queue item for this hour. Generating fresh AI insight.")
        post_text = generate_wellness_insight()
        was_customized = False
        scheduled_for_info = "Autonomous Hourly Cycle"

    char_len = len(post_text)
    print(f"[DISPATCH CONTENT] Target post ({char_len} chars):")
    print("-" * 55)
    print(post_text)
    print("-" * 55)

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
        "error": error_msg,
        "customized": was_customized,
        "scheduled_time": scheduled_for_info
    }

    # 4. Save to posts_log.json
    logs = load_logs()
    logs.insert(0, entry)
    save_logs(logs)

    # 5. Top up upcoming_queue.json so at least 3 upcoming posts are ready
    while len(queue) < 3:
        fresh_draft = generate_wellness_insight()
        new_slot_idx = len(queue) + 1
        queue.append({
            "id": f"queue_{int(utc_now.timestamp())}_{new_slot_idx}",
            "text": fresh_draft,
            "char_count": len(fresh_draft),
            "customized": False,
            "scheduled_at": None,
            "slot": f"SLOT_{new_slot_idx}",
            "scheduled_label": "Next Run (Upcoming Top of the Hour)" if new_slot_idx == 1 else f"Run +{new_slot_idx - 1} Hour{'s' if new_slot_idx > 2 else ''}",
            "created_at": utc_now.strftime("%Y-%m-%d %H:%M:%S UTC")
        })

    # Standardize slot labels for auto items (leave explicit user schedules untouched)
    slot_labels = [
        "Next Run (Upcoming Top of the Hour)",
        "Run +1 Hour",
        "Run +2 Hours",
        "Run +3 Hours",
        "Run +4 Hours"
    ]
    auto_count = 0
    for item in queue:
        if not item.get("scheduled_at"):
            item["slot"] = f"SLOT_{auto_count + 1}"
            item["scheduled_label"] = slot_labels[auto_count] if auto_count < len(slot_labels) else f"Run +{auto_count} Hours"
            auto_count += 1
        item["char_count"] = len(item.get("text", ""))

    save_queue(queue)

    print("=" * 65)
    print(f" [COMPLETED] Status: {status} | Post ID: {entry['id']} | Queue Maintained ({len(queue)} items ready)")
    print("=" * 65)


if __name__ == "__main__":
    main()
