import re
import subprocess
from datetime import datetime, timezone

date = datetime.now(timezone.utc).strftime("%d %b %Y")
time_str = datetime.now(timezone.utc).strftime("%H:%M UTC")

changed = subprocess.run(
    ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
    capture_output=True, text=True
).stdout.strip().split("\n")

files = [f for f in changed if f and "README" not in f][:5]
files_str = "\n".join(f"- `{f}`" for f in files) if files else "- *(no note files changed)*"

total = subprocess.run(
    ["git", "rev-list", "--count", "HEAD"],
    capture_output=True, text=True
).stdout.strip()

section = f"""<!-- CHECKIN_START -->
| | |
|---|---|
| Last check-in | {date} at {time_str} |
| Total commits | {total} |

**Files pushed:**
{files_str}
<!-- CHECKIN_END -->"""

with open("README.md", "r") as f:
    content = f.read()

updated = re.sub(
    r"<!-- CHECKIN_START -->.*?<!-- CHECKIN_END -->",
    section,
    content,
    flags=re.DOTALL
)

with open("README.md", "w") as f:
    f.write(updated)

print("README updated")
