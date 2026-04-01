"""
inject.py — replaces the JS block inside dashboard.py with dqn_debugged.js

Usage:
    python3 inject.py dashboard.py dqn_debugged.js

Output:
    dashboard_fixed.py  (new file, your original is untouched)
"""

import sys, os

if len(sys.argv) != 3:
    print("Usage: python3 inject.py dashboard.py dqn_debugged.js")
    sys.exit(1)

dashboard_path = sys.argv[1]
js_path        = sys.argv[2]

# ── Read dashboard.py ──
with open(dashboard_path, 'r', encoding='utf-8') as f:
    dashboard = f.read()

# ── Read dqn_debugged.js, skip the top comment block ──
with open(js_path, 'r', encoding='utf-8') as f:
    js_lines = f.readlines()

# Find the line that starts with 'use strict'
start_idx = next(i for i, l in enumerate(js_lines) if l.strip().startswith("'use strict'"))
new_js = ''.join(js_lines[start_idx:])

# ── Find <script> ... </script> in the dashboard HTML ──
script_open  = "<script>\n'use strict';"
script_close = "</script>"

idx_open = dashboard.find("<script>")
if idx_open == -1:
    print("ERROR: Could not find <script> tag in dashboard.py")
    sys.exit(1)

# Find the JS content start (after <script>\n)
js_start = dashboard.find("\n", idx_open) + 1

# Find </script>
idx_close = dashboard.find(script_close, idx_open)
if idx_close == -1:
    print("ERROR: Could not find </script> tag in dashboard.py")
    sys.exit(1)

# Replace old JS with new JS
before = dashboard[:js_start]
after  = dashboard[idx_close:]

fixed = before + new_js + "\n" + after

# ── Write output ──
out_name = os.path.splitext(dashboard_path)[0] + "_fixed.py"
with open(out_name, 'w', encoding='utf-8') as f:
    f.write(fixed)

print(f"✅ Done! Output: {out_name}")
print(f"   Old JS: {idx_close - js_start} chars")
print(f"   New JS: {len(new_js)} chars")
