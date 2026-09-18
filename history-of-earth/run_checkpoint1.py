"""
Checkpoint 1 End-to-End Test: Modules 1 to 4
Runs the state machine, researcher agent, and fact checker agent on Hadean/Landscape.
"""

import os
import sys
import json

# Ensure project root is in python path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from pipeline.state_machine import init_db, create_episode, transition, get_episodes_by_state
from agents.researcher import research_episode
from agents.fact_checker import check_claims

def main():
    print("=" * 80)
    print("HISTORY OF EARTH - CHECKPOINT 1 VERIFICATION RUN")
    print("Target: Modules 1-4 End-to-End Execution")
    print("Parameters: Era = 'Hadean', Pillar = 'Landscape'")
    print("=" * 80)

    episode_id = "hadean_landscape_01"
    era = "Hadean"
    pillar = "Landscape"
    db_path = os.path.join(PROJECT_ROOT, "state.db")

    # Step 1: Initialize Database & State Machine (Modules 1 & 2)
    print("\n[STEP 1] Initializing SQLite State Database (db_schema.sql)...")
    init_db(db_path)
    episode = create_episode(episode_id, era, pillar, initial_state="idea", db_path=db_path)
    print(f"  --> Episode registered: ID={episode['id']}, Era={episode['era']}, Pillar={episode['pillar']}, State={episode['state']}")
    assert episode["state"] == "idea"

    # Step 2: Researcher Agent (Module 3)
    print("\n[STEP 2] Running Researcher Agent (agents/researcher.py)...")
    research_data = research_episode(era, pillar)
    claims = research_data.get("claims", [])
    print(f"  --> Researched {len(claims)} candidate claims for {era} / {pillar}:")
    for idx, c in enumerate(claims, 1):
        print(f"      [{idx}] Text: {c['text']}")
        print(f"          Source URL: {c['source_url']}")

    # Transition to 'researched' state
    transition(episode_id, "researched", note=f"Harvested {len(claims)} claims via researcher agent", db_path=db_path)
    current_researched = get_episodes_by_state("researched", db_path=db_path)
    print(f"\n  --> State Machine updated: episode is now in 'researched' state (Count: {len(current_researched)})")

    # Step 3: Fact-Checker Agent (Module 4)
    print("\n[STEP 3] Running Fact-Checker Agent (agents/fact_checker.py)...")
    print("  --> Performing live HTTP reachability checks on source citations...")
    check_results = check_claims(claims)
    approved = check_results.get("approved", [])
    rejected = check_results.get("rejected", [])

    print(f"\n  [FACT CHECK RESULTS] Total Claims: {len(claims)} | Approved: {len(approved)} | Rejected: {len(rejected)}")

    print("\n  >>> APPROVED CLAIMS (Verified Real URLs):")
    for idx, a in enumerate(approved, 1):
        print(f"    {idx}. [PASS - HTTP {a.get('status_code')}]")
        print(f"       Claim: {a['text']}")
        print(f"       Citation: {a['source_url']}")

    print("\n  >>> REJECTED CLAIMS (Unresolvable / Missing / Dead URLs):")
    for idx, r in enumerate(rejected, 1):
        print(f"    {idx}. [FAIL - {r['reason']}]")
        print(f"       Claim: {r['text']}")
        print(f"       Citation: {r['source_url']}")

    # Transition to 'fact_checked' state
    fc_note = f"Fact check complete: {len(approved)} approved, {len(rejected)} rejected"
    transition(episode_id, "fact_checked", note=fc_note, db_path=db_path)

    # Step 4: Final Database Verification
    print("\n[STEP 4] Verifying Final Database State...")
    episodes_in_fc = get_episodes_by_state("fact_checked", db_path=db_path)
    assert len(episodes_in_fc) == 1
    fc_ep = episodes_in_fc[0]
    print(f"  --> Episode ID: {fc_ep['id']}")
    print(f"  --> Current State: {fc_ep['state']}")
    print(f"  --> Updated At: {fc_ep['updated_at']}")
    print(f"  --> Gate A Notes:\n{fc_ep['gate_a_notes']}")

    print("\n" + "=" * 80)
    print("CHECKPOINT 1 RUN COMPLETE: Modules 1-4 executed successfully!")
    print("=" * 80)

if __name__ == "__main__":
    main()
