import sys, re, os, json
from datetime import datetime, timedelta
sys.stdout.reconfigure(encoding='utf-8')

agents = {
    'tong':     r'C:\DuKickAgent\dukick-tong-8767\logs\agent.log',
    'sales':    r'C:\DuKickAgent\dukick-truyenthong-8768\logs\agent.log',
    'account':  r'C:\DuKickAgent\dukick-pm-8769\logs\agent.log',
    'creative': r'C:\DuKickAgent\dukick-pmcreative-8770\logs\agent.log',
    'finance':  r'C:\DuKickAgent\dukick-ketoan-8771\logs\agent.log',
}

today = datetime.now().strftime('%Y-%m-%d')
result = {'date': today, 'agents': {}, 'total': {'in': 0, 'out': 0, 'calls': 0}}
tomorrow = (datetime.now() + timedelta(days=1)).replace(hour=0,minute=0,second=0)
h, rem = divmod(int((tomorrow-datetime.now()).total_seconds()), 3600)
result['reset_in'] = f'{h}h {rem//60}m'

for label, log_path in agents.items():
    total_in = total_out = calls = 0
    if os.path.exists(log_path):
        with open(log_path, encoding='utf-8', errors='ignore') as f:
            for line in f:
                if today not in line: continue
                m = re.search(r'in=(\d+)\s+out=(\d+)', line)
                if m:
                    total_in += int(m.group(1)); total_out += int(m.group(2)); calls += 1
    result['agents'][label] = {'in': total_in, 'out': total_out, 'calls': calls}
    result['total']['in'] += total_in; result['total']['out'] += total_out; result['total']['calls'] += calls

result['total']['total'] = result['total']['in'] + result['total']['out']
print(json.dumps(result, ensure_ascii=False))