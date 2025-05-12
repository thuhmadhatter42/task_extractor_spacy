#!/usr/bin/env python3
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
import pandas as pd
from tqdm import tqdm

# ——— CONFIG —————————————
INPUT_FILE   = "tasks.txt"
OUTPUT_FILE  = "extracted_tasks.csv"
CHUNK_SIZE   = 1000
N_WORKERS    = 8

# placeholders; each worker will set these in init_worker()
nlp = None
matcher = None

def init_worker():
    """Initialize spaCy and the Matcher in each process."""
    import spacy
    from spacy.matcher import Matcher
    global nlp, matcher
    nlp = spacy.load("en_core_web_sm", disable=["ner","lemmatizer"])
    if "sentencizer" not in nlp.pipe_names:
        nlp.add_pipe("sentencizer", first=True)
    matcher = Matcher(nlp.vocab)
    matcher.add("TASK_NEED", [[
        {"LOWER": {"IN": ["need","needs","have","has","must","should"]}},
        {"LOWER": "to", "OP": "?"},
        {"POS": "VERB"}
    ]])
    matcher.add("TASK_IMPERATIVE", [[
        {"IS_SENT_START": True},
        {"POS": "VERB", "OP": "+"}
    ]])

def process_chunk(text_chunk: str):
    """Process one big text chunk, return list of task strings."""
    doc = nlp(text_chunk)
    tasks = []
    for _, start, end in matcher(doc):
        tasks.append(doc[start:end].sent.text.strip())
    return tasks

def main():
    # ensure safe forking on macOS
    mp.set_start_method("forkserver", force=True)

    # read & chunk lines
    with open(INPUT_FILE, encoding="utf-8") as f:
        lines = [L.strip() for L in f if L.strip()]
    chunks = [
        " ".join(lines[i : i + CHUNK_SIZE])
        for i in range(0, len(lines), CHUNK_SIZE)
    ]

    # parallel processing
    all_tasks = []
    with ProcessPoolExecutor(
        max_workers=N_WORKERS,
        initializer=init_worker
    ) as executor:
        for tasks in tqdm(
            executor.map(process_chunk, chunks),
            total=len(chunks),
            desc="Processing chunks"
        ):
            all_tasks.extend(tasks)

    # save results
    pd.DataFrame(all_tasks, columns=["Task"]) \
      .to_csv(OUTPUT_FILE, index=False)
    print(f"\n✅ Extracted {len(all_tasks)} tasks → {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
