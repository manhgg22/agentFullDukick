import json, sys, os
sys.path.insert(0, r"C:\DuKickAgent\agents\dukick-ketoan-8771")
from shared.gauth import test_connection

result = test_connection()
print(json.dumps(result, indent=2, ensure_ascii=False))
