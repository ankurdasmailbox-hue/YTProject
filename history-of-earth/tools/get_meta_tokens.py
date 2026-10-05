"""
Meta Token Generator & Permanent Token Exchanger for History of Earth.
Converts a short-lived Graph API Explorer token into a permanent (never-expiring)
Facebook Page Access Token, and auto-detects your connected IG_USER_ID.
"""

import os
import sys
import requests
import json

GRAPH_API_VERSION = "v19.0"
GRAPH_BASE = f"https://graph.facebook.com/{GRAPH_API_VERSION}"
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(PROJECT_ROOT, ".env")


def exchange_for_permanent_page_token(app_id: str, app_secret: str, short_lived_token: str, page_id: str = "61595168183529"):
    """
    Step 1: Exchange short-lived token for long-lived user token (valid 60 days).
    Step 2: Request Page token using the long-lived user token -> Yields a PERMANENT Page token (Never expires).
    Step 3: Fetches the connected Instagram Business Account ID.
    """
    print(f"\n[1/3] Exchanging token with Meta Graph API ({GRAPH_API_VERSION})...")
    
    # Exchange short-lived user token for long-lived user token
    exchange_url = f"{GRAPH_BASE}/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": short_lived_token
    }
    r = requests.get(exchange_url, params=params).json()
    if "access_token" not in r:
        print("[Error] Failed to exchange token:", r)
        return False
    long_lived_user_token = r["access_token"]
    print("    -> Long-lived user token obtained successfully.")

    # Fetch Page Token (Permanent)
    print(f"\n[2/3] Fetching permanent Page Access Token for Page ID: {page_id}...")
    accounts_url = f"{GRAPH_BASE}/me/accounts"
    acc_res = requests.get(accounts_url, params={"access_token": long_lived_user_token}).json()
    
    page_token = None
    if "data" in acc_res:
        for p in acc_res["data"]:
            if str(p.get("id")) == str(page_id):
                page_token = p.get("access_token")
                break
        if not page_token and len(acc_res["data"]) > 0:
            page_token = acc_res["data"][0].get("access_token")
            page_id = acc_res["data"][0].get("id")

    if not page_token:
        print("[Error] Could not find Page token in /me/accounts. Response:", acc_res)
        return False
    print("    -> Permanent Facebook Page Access Token obtained!")

    # Fetch Instagram Business Account ID
    print(f"\n[3/3] Fetching connected Instagram Business Account ID...")
    ig_url = f"{GRAPH_BASE}/{page_id}"
    ig_res = requests.get(ig_url, params={
        "fields": "instagram_business_account",
        "access_token": page_token
    }).json()
    
    ig_user_id = ""
    if "instagram_business_account" in ig_res:
        ig_user_id = ig_res["instagram_business_account"].get("id", "")
        print(f"    -> Found Instagram Business Account ID: {ig_user_id}")
    else:
        print("    -> Note: Instagram account not linked to Page in Meta Business Suite yet.")

    # Update .env file automatically
    update_env(page_id=page_id, page_token=page_token, ig_user_id=ig_user_id)
    return True


def update_env(page_id: str, page_token: str, ig_user_id: str):
    """Writes the permanent tokens directly into .env."""
    lines = []
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()

    new_lines = []
    keys_updated = set()
    for line in lines:
        if line.startswith("FB_PAGE_ID="):
            new_lines.append(f"FB_PAGE_ID={page_id}\n")
            keys_updated.add("FB_PAGE_ID")
        elif line.startswith("FB_PAGE_ACCESS_TOKEN="):
            new_lines.append(f"FB_PAGE_ACCESS_TOKEN={page_token}\n")
            keys_updated.add("FB_PAGE_ACCESS_TOKEN")
        elif line.startswith("IG_USER_ID="):
            new_lines.append(f"IG_USER_ID={ig_user_id}\n")
            keys_updated.add("IG_USER_ID")
        else:
            new_lines.append(line)

    if "FB_PAGE_ID" not in keys_updated:
        new_lines.append(f"FB_PAGE_ID={page_id}\n")
    if "FB_PAGE_ACCESS_TOKEN" not in keys_updated:
        new_lines.append(f"FB_PAGE_ACCESS_TOKEN={page_token}\n")
    if "IG_USER_ID" not in keys_updated:
        new_lines.append(f"IG_USER_ID={ig_user_id}\n")

    with open(ENV_FILE, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print("\n" + "=" * 70)
    print("SUCCESS: Permanent tokens saved to history-of-earth/.env!")
    print(f"FB_PAGE_ID:           {page_id}")
    print(f"FB_PAGE_ACCESS_TOKEN: {page_token[:15]}...{page_token[-6:]} (Permanent)")
    if ig_user_id:
        print(f"IG_USER_ID:           {ig_user_id}")
    print("=" * 70)


if __name__ == "__main__":
    print("=" * 70)
    print("META PERMANENT TOKEN EXCHANGER")
    print("=" * 70)
    app_id = input("Enter Meta App ID: ").strip()
    app_secret = input("Enter Meta App Secret: ").strip()
    token = input("Enter Token from Graph API Explorer: ").strip()
    page_id = input("Enter Facebook Page ID [Default: 61595168183529]: ").strip() or "61595168183529"
    exchange_for_permanent_page_token(app_id, app_secret, token, page_id)
