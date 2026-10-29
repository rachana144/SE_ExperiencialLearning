\# Lab 5: Static Code Analysis — Reflection



\## 1. What issues did the static analysis tools identify?



Pylint gave the original program a score of 5.37/10, indicating that the code needed improvement. Bandit reported five potential security issues, including the use of `os.system()`, MD5 hashing, `eval()`, a bare exception handler, and a standard random-number generator for booking PINs. Flake8 reported seven style and code-quality findings, including an unused import, an overly long line, unused variables, an incorrect comparison to `None`, and a missing final newline.



\## 2. Which issue was the most important to fix, and why?



The potential shell-command injection issue involving `os.system()` was a priority because shell commands can be dangerous when constructed using untrusted input. The use of `eval()` was also important because evaluating arbitrary expressions can execute unintended code. These issues should be addressed carefully and tested after the changes.



\## 3. How did the tools complement each other?



Pylint assessed overall Python code quality and maintainability. Bandit focused on potential security weaknesses. Flake8 identified style violations and common coding mistakes. Using all three provided a broader review than relying on just one tool.



\## 4. What did I learn from this lab?



I learned that static analysis tools can identify potential security problems, unused code, and style issues before software is deployed. I also learned that findings should be checked against the source code, fixed carefully, and verified by rerunning the tools and testing the program. Comparing before-and-after reports helps demonstrate whether the changes improved the code.



\## Final Results



The original Pylint score was 5.37/10. Final results will be added after all fixes have been implemented, the program has been tested, and all three analysis tools have been run again.

