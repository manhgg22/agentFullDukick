import shutil
import os

# Multi-agent shared library distribution script
# Run from any source agent to copy shared/ to all other agents

SOURCE_AGENT = r"C:\DuKickAgent\agents\dukick-truyenthong-8768"
TARGET_AGENTS = [
    r"C:\DuKickAgent\agents\dukick-ketoan-8771",
    r"C:\DuKickAgent\agents\dukick-pm-8769",
    r"C:\DuKickAgent\agents\dukick-pmcreative-8770",
    r"C:\DuKickAgent\agents\dukick-tong-8767",
    r"C:\DuKickAgent\agents\hermes-hr-8772",
]

FILES = [
    "gauth.py",
    "gauth_tokens.json",
    "upload_to_drive.py",
    "docs_ops.py",
    "sheets_ops.py",
    "drive_config.py",
    "__init__.py",
    "client_secret.json",
]

def distribute():
    source_shared = os.path.join(SOURCE_AGENT, "shared")
    for agent in TARGET_AGENTS:
        shared_dir = os.path.join(agent, "shared")
        os.makedirs(shared_dir, exist_ok=True)
        for fname in FILES:
            src = os.path.join(source_shared, fname)
            dst = os.path.join(shared_dir, fname)
            if os.path.exists(src):
                shutil.copy2(src, dst)
                print(f"  {fname} -> {os.path.basename(agent)}")
            else:
                print(f"  MISSING {fname} in source")
        # Ensure __init__.py exists even if not in source
        init_path = os.path.join(shared_dir, "__init__.py")
        if not os.path.exists(init_path):
            with open(init_path, "w") as f:
                pass
            print(f"  Created __init__.py -> {os.path.basename(agent)}")
    print("\nDistribution complete!")

if __name__ == "__main__":
    distribute()
