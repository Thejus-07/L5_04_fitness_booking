# Issues Found and Fixed

Line numbers refer to the original file (see the `*_before.txt` reports).

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| os.system with string concatenation (Bandit B605, High) | Security | 36 | Shell command built from a variable, so shell injection is possible. It also fails on Windows (`rm` not recognized). | Replaced with `glob.glob()` and `os.remove()`, so no shell is involved |
| Mutable default argument (Pylint W0102) | Bug | 8 | `attendance_log=[]` is created once and shared across every call | Default to `None` and create a new list inside the function |
| Bare `except:` (Pylint W0702, Flake8 E722) | Bug | 21 | Catches and hides every error, including unrelated ones | Catch only `KeyError` and `ValueError` |
| File opened without closing (Pylint R1732, W1514) | Resource leak | 32 | `open()` never closed, and no encoding given | Used `with open(..., encoding="utf-8")` |
| Off-by-one capacity check | Logic | 11 | `>` lets one extra person in (Yoga with capacity 3 held 4) | Changed to `>=` |
| Unknown classes accepted | Logic | 9-10 | "Pilates" got a roster and a booking despite having no capacity | Reject any class not in `class_capacity` |
| Negative capacity accepted | Logic | 25 | `set_capacity("Spin", -2)` made every Spin booking fail | Reject seats below 0 |
| Unvalidated input | Bug | 53 | `int(n)` crashes on text like `abc` | Wrapped in `try/except ValueError` |
| Inconsistent member ID types | Logic | 47 | `55` (int) mixed with string IDs like `"M1"` | Convert every ID with `str()` |
| Duplicate guest IDs | Logic | 29 | `GUEST-0` was reused on every call | Generate unique IDs starting at `GUEST-1` and skip existing ones |
| Function name not snake_case (Pylint C0103) | Style | 27 | `addMembers` | Renamed to `add_members` |
| Missing docstrings (Pylint C0114, C0116) | Style | 1, 8, 18, 24, 27, 31, 35, 38, 42 | Module and functions undocumented | Added docstrings |
| String formatting (Pylint C0209) | Style | 15 | `%` formatting | Used an f-string |
| Dictionary iteration (Pylint C0206) | Style | 39 | Looped over keys and indexed | Used `.items()` |
| Missing blank lines (Flake8 E302, E305) | Style | 8, 18, 24, 27, 31, 35, 38, 42, 58 | Fewer than 2 blank lines around functions | Added blank lines (autopep8) |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 6.60/10 | 10.00/10 |
| Bandit | 1 High issue | No issues identified |
| Flake8 | 10 issues | 0 issues |