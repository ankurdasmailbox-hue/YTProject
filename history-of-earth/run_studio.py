"""
History of Earth — Option 3 Web Studio Launcher.
Runs the hybrid local FastAPI Web Studio and establishes a zero-configuration
Cloudflare Quick Tunnel (trycloudflare.com) for 100% free global remote access.

Usage:
  python run_studio.py
  python run_studio.py --port 8000
  python run_studio.py --local-only
"""

import os
import sys
import time
import shutil
import urllib.request
import subprocess
import threading
import argparse

STUDIO_DIR = os.path.dirname(os.path.abspath(__file__))
CLOUDFLARED_EXE = os.path.join(STUDIO_DIR, "cloudflared.exe")
CLOUDFLARED_DOWNLOAD_URL = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"


def ensure_cloudflared() -> str:
    """Verifies or downloads cloudflared binary for zero-subscription tunneling."""
    # Check if in PATH
    which_path = shutil.which("cloudflared")
    if which_path:
        return which_path

    # Check local folder
    if os.path.exists(CLOUDFLARED_EXE):
        return CLOUDFLARED_EXE

    print("[Option 3 Setup] Cloudflare Tunnel CLI not found locally.")
    print(f"Downloading standalone cloudflared.exe from Cloudflare GitHub release...")
    try:
        urllib.request.urlretrieve(CLOUDFLARED_DOWNLOAD_URL, CLOUDFLARED_EXE)
        print("[Option 3 Setup] Download complete: cloudflared.exe ready!")
        return CLOUDFLARED_EXE
    except Exception as e:
        print(f"[Option 3 Setup Warning] Could not auto-download cloudflared: {e}")
        return ""


def start_tunnel(port: int = 8000) -> None:
    """Launches Cloudflare Quick Tunnel and logs public HTTPS URL."""
    cf_bin = ensure_cloudflared()
    if not cf_bin:
        print("\n[Tunnel Notice] Running in Local Mode only: http://localhost:8000")
        return

    cmd = [cf_bin, "tunnel", "--url", f"http://127.0.0.1:{port}"]
    print(f"\n[Cloudflare Tunnel] Starting tunnel to http://127.0.0.1:{port}...")

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    tunnel_url = None
    for line in iter(process.stdout.readline, ''):
        line = line.strip()
        if "trycloudflare.com" in line:
            parts = [w for w in line.split() if "trycloudflare.com" in w]
            if parts:
                tunnel_url = parts[0]
                if not tunnel_url.startswith("http"):
                    tunnel_url = "https://" + tunnel_url
                print("\n" + "=" * 70)
                print(">>> OPTION 3 CLOUD WEB STUDIO IS LIVE WORLDWIDE <<<")
                print(f"Global Public URL (Smartphone / Tablet): {tunnel_url}")
                print(f"Local URL (Your Laptop):                http://localhost:{port}")
                print("=" * 70 + "\n")
                break


def main():
    parser = argparse.ArgumentParser(description="History of Earth Web Studio (Option 3)")
    parser.add_argument("--port", type=int, default=8000, help="Web server port (default: 8000)")
    parser.add_argument("--local-only", action="store_true", help="Run without Cloudflare Tunnel")
    args = parser.parse_args()

    print("\n" + "=" * 70)
    print("HISTORY OF EARTH — ZERO-SUBSCRIPTION WEB STUDIO (OPTION 3)")
    print("Target: 100-Episode Catalog & Multi-Platform Publishing")
    print("Facebook Page: https://www.facebook.com/profile.php?id=61595168183529")
    print("Instagram:     https://www.instagram.com/earthhistoryanimated/")
    print("=" * 70)

    # Start Cloudflare Tunnel in background thread if not local-only
    if not args.local_only:
        t = threading.Thread(target=start_tunnel, args=(args.port,), daemon=True)
        t.start()

    # Launch FastAPI Server
    import uvicorn
    uvicorn.run("studio.app:app", host="0.0.0.0", port=args.port, reload=False)


if __name__ == "__main__":
    main()
