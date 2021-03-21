import pandas as pd
import numpy as np

REPRESENTATION_DIM = 20
NUM_ROWS = 10
OUTPUT_FILE_NAME = "model2_test_control.tsv"
LABELS_ONLY = True

if LABELS_ONLY:
    df = pd.DataFrame(np.random.randint(0, 2, size=(NUM_ROWS)))
else:
    data = np.random.uniform(-1000.0, 1000.0, size=(NUM_ROWS, REPRESENTATION_DIM))
    df = pd.DataFrame(data)
    df["labels"] = np.random.randint(0, 2, size=(NUM_ROWS))
df.to_csv(OUTPUT_FILE_NAME, index=False, sep="\t", header=False)
