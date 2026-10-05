"""
Meta (Facebook & Instagram) Publisher Agent for History of Earth.
Enables 1-click publishing of cinematic master episodes and vertical shorts (Reels)
to Facebook Pages and Instagram Professional accounts via Meta Graph API v19.0+.

Channel Details:
- Facebook Page ID: 61595168183529 (https://www.facebook.com/profile.php?id=61595168183529)
- Instagram: @earthhistoryanimated (https://www.instagram.com/earthhistoryanimated/)
- 100% Zero Subscription / Official Free Meta Graph API
"""

import os
import sys
import json
import time
import requests
from typing import Dict, List, Any, Optional

DEFAULT_FB_PAGE_ID = "1279963101878153"
DEFAULT_IG_USERNAME = "earthhistoryanimated"
GRAPH_API_VERSION = "v19.0"
GRAPH_API_BASE = f"https://graph.facebook.com/{GRAPH_API_VERSION}"


class MetaPublisher:
    """
    Handles multi-platform publishing to Facebook Page and Instagram Account.
    Provides dry-run mode for local review and live Graph API publishing when tokens are present.
    """

    def __init__(
        self,
        fb_page_id: Optional[str] = None,
        fb_page_token: Optional[str] = None,
        ig_user_id: Optional[str] = None,
        env_file: Optional[str] = None
    ):
        self.fb_page_id = fb_page_id or os.environ.get("FB_PAGE_ID", DEFAULT_FB_PAGE_ID)
        self.fb_page_token = fb_page_token or os.environ.get("FB_PAGE_ACCESS_TOKEN", "")
        self.ig_user_id = ig_user_id or os.environ.get("IG_USER_ID", "")
        self.ig_username = os.environ.get("INSTAGRAM_USERNAME", DEFAULT_IG_USERNAME)

        # Attempt to load from .env if empty
        if not self.fb_page_token and env_file and os.path.exists(env_file):
            self._load_from_env(env_file)

    def _load_from_env(self, env_path: str) -> None:
        """Parses .env file for Meta tokens."""
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip('"').strip("'")
                        if k == "FB_PAGE_ID" and not self.fb_page_id:
                            self.fb_page_id = v
                        elif k == "FB_PAGE_ACCESS_TOKEN" and not self.fb_page_token:
                            self.fb_page_token = v
                        elif k == "IG_USER_ID" and not self.ig_user_id:
                            self.ig_user_id = v
        except Exception:
            pass

    def check_credentials_status(self) -> Dict[str, Any]:
        """Audits credential readiness for Facebook and Instagram publishing."""
        return {
            "facebook": {
                "page_id": self.fb_page_id,
                "token_configured": bool(self.fb_page_token and len(self.fb_page_token) > 20),
                "ready": bool(self.fb_page_id and self.fb_page_token),
                "url": f"https://www.facebook.com/profile.php?id={self.fb_page_id}"
            },
            "instagram": {
                "ig_user_id": self.ig_user_id or "Pending Meta App linkage",
                "username": self.ig_username,
                "token_configured": bool(self.fb_page_token and len(self.fb_page_token) > 20),
                "ready": bool(self.ig_user_id and self.fb_page_token),
                "url": f"https://www.instagram.com/{self.ig_username}/"
            }
        }

    def publish_facebook_video(
        self,
        video_path: str,
        title: str,
        description: str,
        is_reel: bool = False
    ) -> Dict[str, Any]:
        """
        Publishes a video or Reel to the Facebook Page.
        If FB_PAGE_ACCESS_TOKEN is not yet set, performs simulated verification.
        """
        if not os.path.exists(video_path):
            return {"status": "error", "message": f"Video file not found: {video_path}"}

        file_size_mb = round(os.path.getsize(video_path) / (1024 * 1024), 2)

        # Simulation / Dry Run if token not configured
        if not self.fb_page_token:
            return {
                "status": "simulated_success",
                "platform": "facebook",
                "page_id": self.fb_page_id,
                "post_type": "Reel" if is_reel else "Page Video",
                "title": title,
                "file": os.path.basename(video_path),
                "file_size_mb": file_size_mb,
                "message": (
                    f"Facebook post simulated successfully for Page {self.fb_page_id}. "
                    "To enable live automated uploads to your Facebook Page, add FB_PAGE_ACCESS_TOKEN "
                    "to your .env file in history-of-earth/.env."
                ),
                "page_url": f"https://www.facebook.com/profile.php?id={self.fb_page_id}"
            }

        # Live Meta Graph API Video Upload
        endpoint = f"{GRAPH_API_BASE}/{self.fb_page_id}/videos"
        data = {
            "title": title,
            "description": description,
            "access_token": self.fb_page_token
        }
        if is_reel:
            data["video_state"] = "PUBLISHED"

        try:
            with open(video_path, "rb") as video_file:
                files = {"source": video_file}
                resp = requests.post(endpoint, data=data, files=files, timeout=300)
                result = resp.json()

            if resp.status_code == 200 and "id" in result:
                return {
                    "status": "published",
                    "platform": "facebook",
                    "video_id": result["id"],
                    "url": f"https://www.facebook.com/{result['id']}",
                    "file_size_mb": file_size_mb
                }
            else:
                return {
                    "status": "error",
                    "platform": "facebook",
                    "error_details": result,
                    "http_code": resp.status_code
                }
        except Exception as e:
            return {"status": "error", "platform": "facebook", "message": str(e)}

    def publish_instagram_reel(
        self,
        video_url_or_path: str,
        caption: str
    ) -> Dict[str, Any]:
        """
        Publishes a 9:16 vertical Short as an Instagram Reel.
        Instagram Graph API requires a two-step process:
        1. Create media container (media_type=REELS)
        2. Publish media container after processing
        """
        if not self.fb_page_token or not self.ig_user_id:
            return {
                "status": "simulated_success",
                "platform": "instagram",
                "username": self.ig_username,
                "caption": caption[:120] + "...",
                "file": os.path.basename(video_url_or_path),
                "message": (
                    f"Instagram Reel simulated successfully for @{self.ig_username}. "
                    "To enable live uploads, add IG_USER_ID and FB_PAGE_ACCESS_TOKEN to .env."
                ),
                "instagram_url": f"https://www.instagram.com/{self.ig_username}/"
            }

        # Live Instagram Container Flow
        container_endpoint = f"{GRAPH_API_BASE}/{self.ig_user_id}/media"
        params = {
            "media_type": "REELS",
            "caption": caption,
            "access_token": self.fb_page_token
        }

        # Handle Local File via Meta Resumable Upload Flow
        if os.path.exists(video_url_or_path):
            file_size = os.path.getsize(video_url_or_path)
            # Step 1: Create Resumable Upload Session
            init_params = {
                "media_type": "REELS",
                "upload_type": "resumable",
                "caption": caption,
                "access_token": self.fb_page_token
            }
            try:
                init_res = requests.post(container_endpoint, data=init_params, timeout=60).json()
                if "uri" not in init_res or "id" not in init_res:
                    return {"status": "error", "stage": "resumable_init", "details": init_res}
                upload_uri = init_res["uri"]
                container_id = init_res["id"]

                # Step 2: Upload Binary Bytes to Meta Endpoint
                with open(video_url_or_path, "rb") as f:
                    video_bytes = f.read()

                headers = {
                    "Authorization": f"OAuth {self.fb_page_token}",
                    "offset": "0",
                    "file_size": str(file_size)
                }
                up_res = requests.post(upload_uri, headers=headers, data=video_bytes, timeout=300).json()
                if not up_res.get("success", False) and "id" not in up_res:
                    return {"status": "error", "stage": "binary_upload", "details": up_res}

                # Step 3: Wait for Meta Video Ingestion & Processing
                for _ in range(12):
                    time.sleep(5)
                    status_url = f"{GRAPH_API_BASE}/{container_id}"
                    status_res = requests.get(status_url, params={
                        "fields": "status_code",
                        "access_token": self.fb_page_token
                    }).json()
                    sc = status_res.get("status_code")
                    if sc == "FINISHED":
                        break
                    elif sc == "ERROR":
                        return {"status": "error", "stage": "processing_failed", "details": status_res}

                # Step 4: Publish Container
                pub_endpoint = f"{GRAPH_API_BASE}/{self.ig_user_id}/media_publish"
                p_resp = requests.post(pub_endpoint, data={
                    "creation_id": container_id,
                    "access_token": self.fb_page_token
                }, timeout=60).json()

                if "id" in p_resp:
                    return {
                        "status": "published",
                        "platform": "instagram",
                        "media_id": p_resp["id"],
                        "url": f"https://www.instagram.com/{self.ig_username}/"
                    }
                else:
                    return {"status": "error", "stage": "publishing", "details": p_resp}
            except Exception as e:
                return {"status": "error", "platform": "instagram", "message": str(e)}

        return {
            "status": "error",
            "platform": "instagram",
            "message": f"Video source not found or unreachable: {video_url_or_path}"
        }


if __name__ == "__main__":
    pub = MetaPublisher()
    status = pub.check_credentials_status()
    print("Meta Publisher Status Check:")
    print(json.dumps(status, indent=2))
