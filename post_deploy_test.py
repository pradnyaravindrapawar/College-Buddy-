"""Post-Deployment Automated Verification Script.

Tests a live deployment (Render or local backend):
1. Health check (GET /api/health)
2. Live chat inquiry (POST /api/chat)
3. User satisfaction feedback (POST /api/feedback)
4. Admin authorization & unanswered queries fetch (GET /api/admin/unanswered)

Usage:
  python scripts/post_deploy_test.py [BASE_URL] [ADMIN_TOKEN]
Example:
  python scripts/post_deploy_test.py https://my-college-faq.onrender.com college-admin-supersecret-2026
"""

import sys
import time
import requests

DEFAULT_URL = "http://127.0.0.1:8000"
DEFAULT_TOKEN = "college-admin-supersecret-2026"


def run_post_deploy_tests(base_url: str, admin_token: str):
    base_url = base_url.rstrip("/")
    print("=" * 70)
    print(f"POST-DEPLOYMENT LIVE TEST RUNNER")
    print(f"Target URL: {base_url}")
    print("=" * 70)

    success_count = 0
    total_checks = 4

    # 1. Health check
    print("\n[Check 1/4] Testing Health Endpoint (GET /api/health)...")
    start = time.time()
    try:
        r = requests.get(f"{base_url}/api/health", timeout=60)
        latency = round((time.time() - start) * 1000, 1)
        if r.status_code == 200:
            data = r.json()
            print(f"  [PASS] Status: {data.get('status')} | FAQs Indexed: {data.get('faqs_count')} | Latency: {latency}ms")
            success_count += 1
        else:
            print(f"  [FAIL] HTTP {r.status_code}: {r.text}")
    except Exception as e:
        print(f"  [FAIL] Connection failed: {e}")

    # 2. Chat query test
    print("\n[Check 2/4] Testing Chat Inquiry (POST /api/chat)...")
    chat_payload = {
        "message": "What is the annual tuition fee for BTech?",
        "category": "Fees",
        "history": []
    }
    start = time.time()
    log_id = None
    try:
        r = requests.post(f"{base_url}/api/chat", json=chat_payload, timeout=30)
        latency = round((time.time() - start) * 1000, 1)
        if r.status_code == 200:
            data = r.json()
            log_id = data.get("log_id")
            print(f"  [PASS] Source: {data.get('source')} | Confidence: {data.get('confidence')} | Latency: {latency}ms")
            print(f"  Answer Snippet: {data.get('answer')[:80]}...")
            success_count += 1
        else:
            print(f"  [FAIL] HTTP {r.status_code}: {r.text}")
    except Exception as e:
        print(f"  [FAIL] Chat query failed: {e}")

    # 3. User feedback rating test
    print("\n[Check 3/4] Testing Feedback Submission (POST /api/feedback)...")
    if log_id:
        fb_payload = {"log_id": log_id, "helpful": True}
        start = time.time()
        try:
            r = requests.post(f"{base_url}/api/feedback", json=fb_payload, timeout=15)
            latency = round((time.time() - start) * 1000, 1)
            if r.status_code == 200:
                print(f"  [PASS] Thumbs Up recorded successfully for log_id={log_id} | Latency: {latency}ms")
                success_count += 1
            else:
                print(f"  [FAIL] HTTP {r.status_code}: {r.text}")
        except Exception as e:
            print(f"  [FAIL] Feedback call failed: {e}")
    else:
        print("  [SKIP] Skipped because Check 2 did not return a log_id.")

    # 4. Admin authentication test
    print("\n[Check 4/4] Testing Admin Authorization (GET /api/admin/unanswered)...")
    headers = {"Authorization": f"Bearer {admin_token}"}
    start = time.time()
    try:
        r = requests.get(f"{base_url}/api/admin/unanswered", headers=headers, timeout=20)
        latency = round((time.time() - start) * 1000, 1)
        if r.status_code == 200:
            data = r.json()
            stats = data.get("feedback_stats", {})
            print(f"  [PASS] Admin authenticated | Satisfaction Rate: {stats.get('satisfaction_rate_percent')}% | Latency: {latency}ms")
            success_count += 1
        else:
            print(f"  [FAIL] HTTP {r.status_code}: {r.text}")
    except Exception as e:
        print(f"  [FAIL] Admin call failed: {e}")

    print("\n" + "=" * 70)
    print(f"SUMMARY: {success_count}/{total_checks} checks passed.")
    if success_count == total_checks:
        print("Live deployment is healthy and verified!")
    else:
        print("Some checks failed. Inspect error logs above.")
    print("=" * 70)
    return success_count == total_checks


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    token = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_TOKEN
    ok = run_post_deploy_tests(url, token)
    sys.exit(0 if ok else 1)
