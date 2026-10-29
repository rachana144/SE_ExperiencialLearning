\# Lab 5: Static Code Analysis — Issues Found



\## Baseline Results



\- \*\*Pylint score:\*\* 5.37/10

\- \*\*Bandit findings:\*\* 5 (2 High, 1 Medium, 2 Low)

\- \*\*Flake8 findings:\*\* 7



\## Issues Identified



| Tool | Line | Issue | Severity / Type | Fix |

|---|---:|---|---|---|

| Bandit | 58 | `os.system()` starts a shell command | High — B605 | Remove shell execution and use a safe output method |

| Bandit | 47 | MD5 used for ticket hashing | High — B324 | Replace MD5 with SHA-256 |

| Bandit | 42 | `eval()` evaluates a supplied expression | Medium — B307 | Replace dynamic evaluation with validated arithmetic |

| Bandit | 26 | Bare `except` with `pass` | Low — B110 | Handle expected exceptions explicitly |

| Bandit | 51 | `random.randint()` generates booking PIN | Low — B311 | Use a cryptographically secure random generator |

| Flake8 | 6 | Unused `math` import | F401 | Remove the unused import |

| Flake8 | 19 | Line exceeds 79 characters | E501 | Wrap the line |

| Flake8 | 26 | Bare `except` | E722 | Catch the appropriate exception |

| Flake8 | 31 | Unused `booking\_fee` variable | F841 | Remove it or use it appropriately |

| Flake8 | 32 | Incorrect comparison to `None` | E711 | Use `is None` |

| Flake8 | 41 | Unused `base\_price` variable | F841 | Remove it or use it appropriately |

| Flake8 | 82 | Missing newline at end of file | W292 | Add a final newline |



\## Pylint



The original code received a score of 5.37/10. The code will be refactored to improve naming, exception handling, documentation, and maintainability. The final score will be recorded after rerunning Pylint.



\## Verification



After applying fixes, the program will be executed again and Pylint, Bandit, and Flake8 will be rerun. The final reports and scores will be compared with the baseline results.

