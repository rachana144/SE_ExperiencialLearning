\# Lab 5: Static Code Analysis — Issues Found



\## Baseline Results



\- \*\*Pylint score:\*\* 5.37/10

\- \*\*Bandit findings:\*\* 5 (2 High, 1 Medium, 2 Low)

\- \*\*Flake8 findings:\*\* 7



\## Issues Identified



| Tool | Line | Issue | Severity / Type | Fix |

|---|---:|---|---|---|

| Bandit | 58 | `os.system()` executes a shell command | High — B605 | Remove shell execution and use a safe Python output method |

| Bandit | 47 | MD5 used for ticket hashing | High — B324 | Replace MD5 with SHA-256 |

| Bandit | 42 | `eval()` evaluates an expression supplied as text | Medium — B307 | Replace dynamic evaluation with validated arithmetic |

| Bandit | 26 | Bare `except` with `pass` | Low — B110 | Handle the missing-seat case explicitly |

| Bandit | 51 | `random.randint()` generates the booking PIN | Low — B311 | Use the cryptographically secure `secrets` module |

| Flake8 | 6 | Unused `math` import | F401 | Remove the unused import |

| Flake8 | 19 | Line exceeds 79 characters | E501 | Wrap the line across multiple lines |

| Flake8 | 26 | Bare `except` statement | E722 | Replace it with an explicit condition or appropriate exception handling |

| Flake8 | 31 | Unused `booking\_fee` variable | F841 | Remove the unused variable |

| Flake8 | 32 | Incorrect comparison to `None` | E711 | Use `is None` |

| Flake8 | 41 | Unused `base\_price` variable | F841 | Use the variable in the price calculation or remove it if unnecessary |

| Flake8 | 82 | Missing newline at end of file | W292 | Add a final newline |



\## Pylint



The original code received a score of \*\*5.37/10\*\*. The code was refactored to improve naming, documentation, exception handling, and maintainability.



After the fixes were applied, the final Pylint score improved to \*\*10.00/10\*\*.



\## Final Verification



All three static analysis tools were rerun on the corrected `ticket\_booking\_system.py` file.



| Tool | Baseline Result | Final Result |

|---|---|---|

| Pylint | 5.37/10 | 10.00/10 |

| Bandit | 5 findings | 0 findings |

| Flake8 | 7 findings | 0 findings |



\### Evidence Files



\- `pylint\_before.txt` — Original Pylint results.

\- `bandit\_before.txt` — Original Bandit findings.

\- `flake8\_before.txt` — Original Flake8 findings.

\- `pylint\_after.txt` — Final Pylint score.

\- `bandit\_after.txt` — Final Bandit results.

\- `flake8\_after.txt` — Final Flake8 results.



\## Conclusion



The static analysis process identified code-quality problems, style violations, and security vulnerabilities in the original program. After correcting these issues, the code achieved a Pylint score of 10.00/10, zero Flake8 findings, and zero Bandit findings.



These results demonstrate improved code quality and address the vulnerabilities detected by the configured tools. Static analysis alone does not guarantee that the program is entirely free of bugs or security risks.

