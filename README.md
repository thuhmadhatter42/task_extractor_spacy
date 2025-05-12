README.txt – Task Extractor (Multiprocessing, spaCy)
-------------------------------------------------------

🧠 Overview
-----------
This Python script extracts to-do style tasks from a plain text file using pattern matching with spaCy + multiprocessing.
It’s designed for large documents, e.g. years of notes or exported text messages.

✅ Features
-----------
- Fast processing with multiprocessing & ProcessPoolExecutor
- Uses spaCy's Matcher to find imperative verbs and "need to"-style tasks
- Outputs results into a CSV

🖥 Requirements
---------------
- macOS 12.7.4+
- Python 3.10
- Basic command-line knowledge
- Your input file should be named `tasks.txt` and live in the root project folder

⚙️ Setup Instructions (For Dummies)
-----------------------------------
1. Install Python 3.10 (separate from macOS default)
   Recommended: use `pyenv`
   brew install pyenv
   pyenv install 3.10.13
   pyenv global 3.10.13

2. Verify Python version
   python3 --version
   # Should return Python 3.10.x

3. Clone the repo or copy your script into a new folder
   mkdir task-extractor && cd task-extractor

4. Create and activate virtual environment
   python3 -m venv venv
   source venv/bin/activate

5. Install dependencies
   pip install -U pip
   pip install spacy pandas tqdm
   python -m spacy download en_core_web_sm

6. Prepare your input file
   Rename or place your file as:
   tasks.txt

7. Run the script
   python task_extractor_mp.py

8. Check output
   The results will be in:
   extracted_tasks.csv
