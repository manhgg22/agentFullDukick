"""
shared/drive_config.py — Folder IDs cho từng agent trên Google Drive.

Usage:
    from shared.drive_config import AGENT_FOLDER_ID
    result = upload_file(path, folder_id=AGENT_FOLDER_ID)
"""

AGENT_FOLDER_ID = "FALLBACK_ID"

# Map: agent name → folder_id
FOLDER_MAP = {
    "dukick-truyenthong-8768": "1tDfaVW9a3zqACLgyGa1n1YZMHo4GYRZD",
    "dukick-ketoan-8771": "18NUJCy1XraNWJkn_iIcT8qyC4CEaCF6r",
    "dukick-pm-8769": "10PuVkvshc5jo-fK8wow9QVJ0T5T8qOGi",
    "dukick-pmcreative-8770": "10rT0BK4K6N6vwVP641ezJE9w75TeLKlL",
    "dukick-tong-8767": "17kl9Nzas4rUvQybFLzhPjFmhWAhS9USk",
    "hermes-hr-8772": "1v1dJH_JKTBb2cSnmLCRLbqVe0nWGvcXN",
}

def get_folder_id(agent_name):
    return FOLDER_MAP.get(agent_name, AGENT_FOLDER_ID)
