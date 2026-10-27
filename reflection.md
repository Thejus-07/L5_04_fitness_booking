# Reflection

## 1. Which tool found the most serious problem, and why did it matter?

Bandit found the most serious problem. It reported a single issue, B605 (start_process_with_a_shell), with High severity and High confidence, on line 36 of the original file: `os.system("rm -f " + prefix + "*.json")`. The command is built by joining pieces of text and is then handed to the system shell. If `prefix` ever came from user input or a config file, someone could add shell characters such as `;` and run any command they liked. This kind of flaw is called command injection (CWE-78).

The line also had a practical problem. `rm` does not exist in Windows PowerShell, so when I ran the program it printed "'rm' is not recognized" and cleaned up nothing. I fixed it by using `glob.glob()` to find the matching files and `os.remove()` to delete them. No shell is involved any more, and Bandit now reports "No issues identified". I fixed this first because a security flaw can cause harm outside the program, while a style problem cannot.

## 2. Which bugs did the tools miss, and how did I find them?

None of the tools flagged the logic bugs, and I found them by running the program and reading its output. (1) Yoga has a capacity of 3 but the roster showed four people, M1 to M4, because the check used `>` instead of `>=`. (2) "Pilates" is not a real class, yet M5 was booked into it, because the code created a new roster for any unknown name. (3) `set_capacity("Spin", -2)` was accepted, so all three Spin bookings printed "Class full: Spin" and Spin ended up empty. (4) Typing `abc` at the prompt crashed the program with a ValueError traceback. (5) The member ID `55` was an int while the others were strings, and `GUEST-0` was reused on every call.

The tools missed these because they look for patterns, not intent. Pylint cannot know that Yoga should hold 3 people, and a negative number is perfectly valid Python. I fixed them by changing `>` to `>=`, rejecting unknown classes and negative seats, converting IDs with `str()`, generating unique guest IDs, and wrapping `int()` in a `try/except ValueError`.

## 3. How do Pylint, Flake8 and Bandit differ, and where do they overlap?

Each tool has a different job. Pylint is the code reviewer: it checks quality and design, such as the dangerous default argument (W0102), the bare except (W0702), the `addMembers` name (C0103), missing docstrings and the unclosed file (R1732). It gives a score out of 10, and mine went from 6.60 to 10.00. Flake8 is the style checker for PEP 8: it reported eight E302 blank-line errors, one E305 and one E722. It has no score; an empty output means it passed. Bandit is the security guard: it looks for dangerous calls and reports severity and confidence, which is how it found the shell call.

They overlap in places. The bare `except:` was reported by both Pylint (W0702) and Flake8 (E722), and the missing final newline was reported by Pylint (C0304) and Flake8 (W292). Because of this overlap and the differences, running all three gives better coverage than any one of them alone.

## 4. Does a 10/10 Pylint score mean the code is correct?

No. After my three tool commits Pylint showed 10.00/10, Bandit showed no issues and Flake8 printed nothing, but the program still let four people into a three-seat Yoga class, accepted a negative capacity and crashed on bad input. Static analysis checks how the code is written, not whether it does what it is supposed to do. It is necessary but not sufficient.

A high score can even create false confidence, which is why I made a separate commit for the logic bugs after the tool fixes. To catch this kind of bug I would also run the program with different inputs, add unit tests (for example, a test that booking a fourth person into Yoga returns False), and have another person review the code. Static analysis is one layer of quality assurance, not the whole of it.