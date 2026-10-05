"""
Meta Permanent Token Generator & Validator for History of Earth.

Automates the Meta token exchange hierarchy to generate a NEVER-EXPIRING
Facebook Page Access Token (which also manages linked Instagram publishing).

Hierarchy:
  Short-Lived User Token (~1 hour)
     + App ID & App Secret
     --> Long-Lived User Token (60 days)
     --> GET /me/accounts
     --> Permanent Page Access Token (NEVER EXPIRES)
"""

import os
import sys
import requests
from typing import Dict, Any, Optional

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(PROJECT_ROOT, ".env")
GRAPH_API_VERSION = "v19.0"
GRAPH_BASE = f"https://graph.facebook.com/{GRAPH_API_VERSION}"


def inspect_token(access_token: str, app_id: str, app_secret: str) -> Dict[str, Any]:
    """Inspects a token to verify its validity and expiration timestamp."""
    app_token = f"{app_id}|{app_secret}"
    url = f"{GRAPH_BASE}/debug_token"
    params = {
        "input_token": access_token,
        "access_token": app_token
    }
    r = requests.get(url, params=params)
    return r.json().get("data", {})


def exchange_for_permanent_page_token(
    app_id: str,
    app_secret: str,
    short_lived_user_token: str,
    target_page_id: Optional[str] = "1279963101878153"
) -> Dict[str, Any]:
    """
    Exchanges a short-lived user token for a permanent Page access token.
    """
    print("\n[STEP 1/3] Exchanging Short-Lived Token for Long-Lived User Token (60 Days)...")
    exchange_url = f"{GRAPH_BASE}/oauth/access_token"
    exchange_params = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": short_lived_user_token
    }
    r = requests.get(exchange_url, params=exchange_params)
    data = r.json()
    if "error" in data:
        raise RuntimeError(f"Failed to exchange token: {data['error'].get('message')}")

    long_lived_user_token = data.get("access_token")
    print("  [OK] Successfully retrieved 60-Day Long-Lived User Token.")

    print("\n[STEP 2/3] Querying /me/accounts for Permanent Page Access Token...")
    accounts_url = f"{GRAPH_BASE}/me/accounts"
    accounts_params = {
        "access_token": long_lived_user_token,
        "limit": 100
    }
    r = requests.get(accounts_url, params=accounts_params)
    acc_data = r.json()
    if "error" in acc_data:
        raise RuntimeError(f"Failed to fetch accounts: {acc_data['error'].get('message')}")

    pages = acc_data.get("data", [])
    if not pages and target_page_id:
        print(f"  [NOTICE] /me/accounts returned 0 pages. Attempting direct lookup for Page ID {target_page_id}...")
        direct_url = f"{GRAPH_BASE}/{target_page_id}"
        direct_r = requests.get(direct_url, params={"fields": "access_token,name", "access_token": long_lived_user_token})
        direct_data = direct_r.json()
        if "access_token" in direct_data:
            pages = [direct_data]
            print(f"  [OK] Successfully retrieved Page Token via direct query for '{direct_data.get('name')}'!")
        else:
            # Query granted permissions to diagnose
            perm_r = requests.get(f"{GRAPH_BASE}/me/permissions", params={"access_token": long_lived_user_token})
            granted = [p["permission"] for p in perm_r.json().get("data", []) if p.get("status") == "granted"]
            print(f"  [DEBUG] Granted permissions on this token: {granted}")
            if "pages_show_list" not in granted:
                raise RuntimeError(
                    "Missing 'pages_show_list' permission! In Graph API Explorer, make sure to add "
                    "'pages_show_list' under Permissions, AND in the Facebook popup check the box for your Page."
                )
            else:
                err_msg = direct_data.get("error", {}).get("message", "User account is not recognized as an Admin on this Page.")
                raise RuntimeError(f"Could not access Page ID {target_page_id}: {err_msg}")

    selected_page = None
    if target_page_id:
        for p in pages:
            if p.get("id") == target_page_id:
                selected_page = p
                break

    if not selected_page:
        selected_page = pages[0]

    page_id = selected_page.get("id")
    page_name = selected_page.get("name")
    permanent_page_token = selected_page.get("access_token")
    print(f"  [OK] Found Page: '{page_name}' (ID: {page_id})")

    # Step 2B: Query Instagram Business Account ID linked to this page
    print("\n[STEP 2B] Querying Linked Instagram Professional Account...")
    page_info_url = f"{GRAPH_BASE}/{page_id}"
    ig_params = {
        "fields": "instagram_business_account{id,username}",
        "access_token": permanent_page_token
    }
    r_ig = requests.get(page_info_url, params=ig_params)
    ig_data = r_ig.json().get("instagram_business_account", {})
    ig_user_id = ig_data.get("id", "")
    ig_username = ig_data.get("username", "earthhistoryanimated")

    if ig_user_id:
        print(f"  [OK] Found Instagram Account: @{ig_username} (ID: {ig_user_id})")
    else:
        print("  [NOTICE] No Instagram Business Account automatically linked in response.")

    print("\n[STEP 3/3] Inspecting Page Token Expiration Status...")
    debug_info = inspect_token(permanent_page_token, app_id, app_secret)
    expires_at = debug_info.get("expires_at", -1)
    is_valid = debug_info.get("is_valid", False)

    expiry_desc = "NEVER (Permanent)" if expires_at == 0 else f"Expires at timestamp: {expires_at}"
    print(f"  --> Token Valid: {is_valid}")
    print(f"  --> Expiration: {expiry_desc}")
    print(f"  --> Token Type: {debug_info.get('type')}")
    print(f"  --> Scopes: {', '.join(debug_info.get('scopes', []))}")

    return {
        "page_id": page_id,
        "page_name": page_name,
        "permanent_token": permanent_page_token,
        "expires_at": expires_at,
        "expiry_desc": expiry_desc,
        "ig_user_id": ig_user_id,
        "ig_username": ig_username,
        "scopes": debug_info.get("scopes", [])
    }


def update_env_file(page_id: str, permanent_token: str, ig_user_id: str = "", ig_username: str = "") -> None:
    """Updates .env file with the permanent token and page configuration."""
    lines = []
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()

    keys_to_update = {
        "FB_PAGE_ID": page_id,
        "FB_PAGE_ACCESS_TOKEN": permanent_token
    }
    if ig_user_id:
        keys_to_update["IG_USER_ID"] = ig_user_id
    if ig_username:
        keys_to_update["INSTAGRAM_USERNAME"] = ig_username

    new_lines = []
    seen = set()

    for line in lines:
        matched = False
        for k, v in keys_to_update.items():
            if line.strip().startswith(f"{k}="):
                new_lines.append(f"{k}={v}\n")
                seen.add(k)
                matched = True
                break
        if not matched:
            new_lines.append(line)

    for k, v in keys_to_update.items():
        if k not in seen:
            new_lines.append(f"{k}={v}\n")

    with open(ENV_FILE, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print(f"\n[SUCCESS] Updated '{ENV_FILE}' with the Permanent Page Access Token!")


def main():
    print("=" * 80)
    print("META PERMANENT PAGE ACCESS TOKEN GENERATOR")
    print("=" * 80)
    print("This utility converts a short-lived user token from Graph API Explorer into")
    print("a 100% NEVER-EXPIRING Page Access Token for Facebook & Instagram automation.\n")

    app_id = input("Enter your Meta App ID: ").strip()
    if not app_id:
        print("[ERROR] App ID is required.")
        return

    app_secret = input("Enter your Meta App Secret: ").strip()
    if not app_secret:
        print("[ERROR] App Secret is required.")
        return

    short_token = input("Enter Short-Lived User Token (from Graph API Explorer): ").strip()
    if not short_token:
        print("[ERROR] Short-lived token is required.")
        return

    target_page = input("Enter Facebook Page ID [default: 1279963101878153]: ").strip() or "1279963101878153"

    try:
        res = exchange_for_permanent_page_token(
            app_id=app_id,
            app_secret=app_secret,
            short_lived_user_token=short_token,
            target_page_id=target_page
        )

        print("\n" + "=" * 80)
        print("PERMANENT TOKEN GENERATED SUCCESSFULLY!")
        print(f"Page Name:     {res['page_name']}")
        print(f"Page ID:       {res['page_id']}")
        print(f"Expiration:    {res['expiry_desc']}")
        print(f"Instagram ID:  {res['ig_user_id']}")
        print("=" * 80)

        confirm = input("\nSave this permanent token directly to history-of-earth/.env? (y/n) [default: y]: ").strip().lower()
        if confirm in ("", "y", "yes"):
            update_env_file(
                page_id=res["page_id"],
                permanent_token=res["permanent_token"],
                ig_user_id=res["ig_user_id"],
                ig_username=res["ig_username"]
            )
            print("\nSetup complete! You can now run 'python history-of-earth/publish_episode7_all.py' anytime.")
        else:
            print("\nToken not saved to .env. Here is your token string:")
            print(res["permanent_token"])

    except Exception as e:
        print(f"\n[ERROR] {e}")


if __name__ == "__main__":
    main()
