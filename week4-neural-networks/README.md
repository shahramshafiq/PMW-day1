# youthxAI: Neural Networks

**Shahram Shafiq | Week 4, Module 17 | youthxAI Session 4 of 4**

---

## What this is

Trained a neural network to classify handwritten digits (MNIST), matching the session plan's stated aim: "build a handwritten-digit image classifier (MNIST-style) and watch it learn across training epochs." Two deliverables, as required:

- Notebook: [`youthxai_neural_networks.ipynb`](youthxai_neural_networks.ipynb) (plain-text source at [`notebook_source.py`](notebook_source.py), a [jupytext](https://jupytext.readthedocs.io/) "percent format" file, easier to diff/read than raw notebook JSON)
- Visualisation deck: [`visualisation_deck.html`](visualisation_deck.html), a self-contained single HTML file (all images embedded, opens directly in any browser, no server needed)

## Why Keras, not from-scratch

The earlier youthxAI notebooks in this repo (linear regression, logistic regression) were built from scratch with numpy on purpose, this internship's own guidance flags plagiarism checks and wants unconventional, personally-written logic. This module is different: the actual session plan (`youthxai-session-plans.pdf`, Session 4) specifies the platform as "Google Colab (TensorFlow / Keras)" and its learning objectives use Keras-specific language directly, "build, compile and train a model," and explicitly say to "understand backpropagation at a high level," not implement it. Matching that, the main notebook uses `tf.keras.Sequential` the way the session taught it.

To still genuinely satisfy "understand backpropagation," not just nod along, the notebook has a bonus section afterward: the identical 784-128-64-10 architecture rebuilt from raw numpy, forward pass and backpropagation written out by hand, trained on a 12,000-image subset for speed. Both land in the same neighborhood on the same real test set (97.18% vs 93.73%), which is the actual proof the from-scratch version is doing the same thing the library is, not just producing plausible-looking numbers.

## The data

The real MNIST dataset, loaded in the notebook via `tf.keras.datasets.mnist.load_data()` (the standard way, matches what Colab would do). 70,000 total images, 28x28 pixels, 60,000 train / 10,000 test, verified in the notebook itself against the well-published per-class label counts for standard MNIST (5,923 zeros, 6,742 ones, etc.) before doing anything else with it.

## Architecture

Matches the layer diagram shown on the session's last slide before the coding portion started: 784 input pixels (the flattened 28x28 image) into two hidden layers, then 10 output classes.

```
Input (28x28) -> Flatten (784) -> Dense(128, relu) -> Dense(64, relu) -> Dense(10, softmax)
```

109,386 trainable parameters. Optimizer: Adam. Loss: sparse categorical cross-entropy.

## Results (from the actual executed notebook, not estimated)

| | Keras model | From-scratch numpy model |
|---|---|---|
| Training data | 60,000 images (full set) | 12,000 images (subset, for speed) |
| Epochs | 8 | 6 |
| Test accuracy | **97.18%** | 93.73% |
| Test loss | 0.094 | (cross-entropy, see notebook) |
| Misclassified | 282 / 10,000 (2.82%) | — |

## Verification

Checked directly, not assumed from a clean run:

- Ran the whole notebook end to end with `jupyter nbconvert --execute` (not hand-typed cell outputs), so every printed number and every chart in it is real, not authored to look plausible.
- Verified the loaded data against MNIST's published per-class counts before training anything, inside the notebook itself (visible as its own cell).
- **Caught and fixed a real bug during verification**: the first executed pass showed zero embedded charts, `matplotlib.use('Agg')` (correct for a headless script, wrong for a notebook meant to display inline) was silently swallowing every `plt.show()`. Caught by programmatically checking the saved `.ipynb` for actual `image/png` output data rather than trusting that six plotting cells running without an error meant six charts existed. Removed the Agg backend, added `%matplotlib inline`, re-executed, and confirmed all 5 expected images are genuinely embedded (checked their base64 payload sizes, not just their presence).
- Cross-checked two independent implementations (Keras and from-scratch numpy) against each other on the same real test set as a sanity check, consistent with the approach used in the earlier logistic-regression notebook (checked against scikit-learn there).
- The visualisation deck's images and stated numbers were extracted directly from this specific executed notebook run, not regenerated separately, so the deck and the notebook can't drift out of sync with each other.

## Note on `data/`

`data/` (the downloaded MNIST CSV mirror used for my own local pre-verification before Colab, plus scratch training/plotting scripts) is gitignored, roughly 125MB of reproducible, non-original data. The actual notebook doesn't depend on it, it loads MNIST itself via `tf.keras.datasets.mnist.load_data()`.
