# Setup
* python -m venv .thesis 
* source .thesis/bin/activate
* (.thesis) $ pip install ipykernel
* (.thesis) $ ipython kernel install --user --name=.thesis
* (.thesis) $ pip install --upgrade pip
* (.thesis) $ pip install -r requirements.txt

* make sure you use the .thesis kernel when opening jupyter lab

# For progress bars
jupyter nbextension enable --py widgetsnbextension
jupyter labextension install @jupyter-widgets/jupyterlab-manager

# Dealing with GPU OOM
Simplest workaround seems to be closing down the notebook, then restarting it. You can check the held GPU with nvidia-smi

# Data 
suc3_dataframe: The converted xml filetree from SUC3.0 without any cleaning applied. One row for each word.
wordpiece_sentences_df: The wordpiece-segmented words. Each row is a sentence, each column is a wordpiece
wordpiece_labels_df: Same as above but for labels
sentence_ints.npy: The wordpiece-segmented, padded and tokenized input for ALBERT. One row per sentence, 100 cols for the tokens
attention_ints.npy: same as above but for masking
label_ints.npy: same as above but for labels
MMAP_MATRIX.dat: memory mapped embeddings for all wordpiece tokens in all sentences. More than 40GB.
ONE_HOT_LABELS.dat: memory mapped one-hot encoded wordpiece labels in all sentences. Just a few 100mb!

suc3_formatted: Deprecated, used for checking that all data manipulation operations were done properly. One row for each sentence, on colmn for the words, the token ids, the entities, the entity ids and the attention masks