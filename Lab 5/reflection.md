\# Lab 5: Static Code Analysis — Reflection



\## 1. Objective



The objective of this lab was to analyze Python code using Pylint, Bandit, and Flake8, identify code-quality and security issues, and improve the program based on the findings.



\## 2. Initial Analysis



The original `ticket\_booking\_system.py` file had several code-quality problems, formatting violations, and potential security vulnerabilities.



The initial results were:



| Tool | Initial Result |

|---|---|

| Pylint | 5.37/10 |

| Bandit | 5 findings |

| Flake8 | 7 findings |



\## 3. Improvements Made



The program was updated to address the issues found during static analysis.



\- Removed unused imports and variables.

\- Improved function names and documentation.

\- Corrected exception handling and comparisons with `None`.

\- Replaced `eval()` with direct arithmetic and discount validation.

\- Replaced MD5 with SHA-256.

\- Used the `secrets` module to generate booking PINs.

\- Removed unsafe shell execution.

\- Retrieved the box-office key from an environment variable rather than hardcoding it.

\- Corrected formatting and added the final newline.



\## 4. Final Results



After applying the changes, all three tools were run again.



| Tool | Initial Result | Final Result |

|---|---|---|

| Pylint | 5.37/10 | 10.00/10 |

| Bandit | 5 findings | 0 findings |

| Flake8 | 7 findings | 0 findings |



\## 5. What I Learned



This lab helped me understand the importance of static code analysis in software development.



Pylint helped me improve code quality and maintainability. Flake8 helped me identify formatting problems and common Python mistakes. Bandit helped me identify potentially unsafe coding practices, including dynamic expression evaluation, weak hashing, and shell command execution.



I also learned that removing hardcoded secrets, using secure random-number generation, and avoiding unsafe functions can improve the security of a program.



\## 6. Conclusion



The lab demonstrated how static analysis tools can identify issues before software is deployed. The final code achieved a Pylint score of 10.00/10, zero Flake8 findings, and zero Bandit findings.



Although the final static analysis results were clean, additional functional testing and security review would still be useful to verify the overall behavior and security of the application.

