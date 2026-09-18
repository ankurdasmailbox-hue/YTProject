"""
Fact Checker Agent for History of Earth.
Validates each claim to ensure it has a real, resolvable citation.
Strict rule: A claim with source_url=None or an unreachable URL goes to rejected, always.
"""

import requests
from typing import Dict, List, Any, Optional

USER_AGENT = "HistoryOfEarthFactChecker/1.0 (compliance verification bot; contact@historyofearth.local)"


def check_url_reachable(url: str, timeout: int = 8) -> tuple[bool, Optional[int], Optional[str]]:
    """
    Checks if a URL is reachable by performing a HEAD request (falling back to streaming GET).
    Returns: (is_reachable: bool, status_code: Optional[int], error_message: Optional[str])
    """
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    try:
        # First attempt HEAD request to minimize bandwidth
        resp = requests.head(url, headers=headers, timeout=timeout, allow_redirects=True)
        if resp.status_code in (403, 405):
            # Some servers block HEAD or return 405 Method Not Allowed; fall back to GET
            resp = requests.get(url, headers=headers, timeout=timeout, stream=True, allow_redirects=True)

        if 200 <= resp.status_code < 400:
            return True, resp.status_code, None
        else:
            return False, resp.status_code, f"HTTP status code {resp.status_code}"
    except requests.RequestException as exc:
        return False, None, str(exc)


def check_claims(claims: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Checks a list of claims.
    Returns:
        {"approved": [...], "rejected": [...]}
    A claim with source_url=None or an unreachable URL goes to rejected, always.
    """
    approved: List[Dict[str, Any]] = []
    rejected: List[Dict[str, Any]] = []

    for claim in claims:
        text = claim.get("text", "")
        source_url = claim.get("source_url")

        # Check for missing / None source_url
        if source_url is None or not isinstance(source_url, str) or not source_url.strip():
            rejected.append({
                "text": text,
                "source_url": None,
                "reason": "Missing citation (source_url is None / unresolved)"
            })
            continue

        url = source_url.strip()
        is_reachable, status_code, err_msg = check_url_reachable(url)

        if is_reachable:
            approved.append({
                "text": text,
                "source_url": url,
                "status_code": status_code,
                "verification": "VERIFIED_200_OK"
            })
        else:
            rejected.append({
                "text": text,
                "source_url": url,
                "status_code": status_code,
                "reason": f"Unreachable source URL: {err_msg}"
            })

    return {
        "approved": approved,
        "rejected": rejected
    }


if __name__ == "__main__":
    sample_claims = [
        {"text": "Earth formed ~4.54 billion years ago.", "source_url": "https://en.wikipedia.org/wiki/Hadean"},
        {"text": "Speculative claim without citation.", "source_url": None},
        {"text": "Claim with dead link.", "source_url": "https://this-domain-does-not-exist-12345.org/deadlink"}
    ]
    results = check_claims(sample_claims)
    print(f"Approved ({len(results['approved'])}):")
    for a in results["approved"]:
        print(f"  [PASS] {a['text']} -> {a['source_url']} (HTTP {a['status_code']})")
    print(f"\nRejected ({len(results['rejected'])}):")
    for r in results["rejected"]:
        print(f"  [REJECT] {r['text']} -> {r['source_url']} (Reason: {r['reason']})")
