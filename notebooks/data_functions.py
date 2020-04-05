
import pandas as pd
import numpy as np
from keras.preprocessing.sequence import pad_sequences
from transformers import AutoTokenizer
import torch

"""
The input needs to be on the form of a dataframe with a column named 'Sentence'
Where each row consists of one sentence

One can also pass an ordinary string, this method formats it for use with the model
"""
def check_input_format(input_data):
    print("Checking input...")
    if isinstance(input_data, pd.DataFrame):
        if 'Sentence' in input_data:
            print("PASS")
            return input_data
        else:
            print("FAIL")
    elif isinstance(input_data, str):
        print("Converting sentence to DataFrame Object")
        sentence_df = pd.DataFrame()
        sentence_df['Sentence'] = [input_data]
        return sentence_df
    else:
        print("FAIL")

"""
Prepares the sentences for use with BERT-type models.
"""
def format_sentences_for_BERT(input_df):
    #Ensure the input is on the expected format
    input_df = check_input_format(input_df)

    #Load swedish tokenizer
    tokenizer = AutoTokenizer.from_pretrained("KB/bert-base-swedish-cased-ner")
    
    # Use WORDPIECE tokenization
    #input_df['Tokenized'] = input_df[['Sentence']].apply(lambda x: tokenizer.tokenize(x[0]), axis=1)
    # Ensure no named entities have been split apart

    # use WORD tokenization
    input_df['Tokenized'] = input_df[['Sentence']].apply(lambda x: x[0], axis=1)

    # Replace words with integers, add the special [CLS] and [SEP] tokens
    input_df['Integerized'] = input_df[['Tokenized']].apply(lambda x: tokenizer.encode(x[0], add_special_tokens=True), axis=1)

    # Pad and truncate all sentences so they are the same length
    length = 50
    input_df['Input'] = input_df[['Integerized']].apply(lambda x: pad_sequences(x, maxlen=length, dtype="long", truncating="post", padding="post")[0], axis=1)

    # Create attention mask. Attention is 0 for padding, else 1
    input_df['Attention_Mask'] = input_df[['Input']].apply(lambda x: (x[0] != 0).astype(int), axis=1)
    
    #Convert input data to tensors
    data_matrix = torch.tensor([x[0] for x in input_df[['Input']].values])
    mask_matrix = torch.tensor([x[0] for x in input_df[['Attention_Mask']].values])
    return data_matrix, mask_matrix


"""
Prepares the labels for use with BERT-type models.
"""
def format_labels_for_BERT(label_df):
    #Load swedish tokenizer
    tokenizer = AutoTokenizer.from_pretrained("KB/bert-base-swedish-cased-ner")

    # use WORD tokenization
    label_df['Tokenized'] = label_df[['Labels']].apply(lambda x: x[0], axis=1)

    # Replace labels with integers, add the special [CLS] and [SEP] tokens
    label_df['Integerized'] = label_df[['Tokenized']].apply(lambda x: tokenizer.encode(x[0], add_special_tokens=True), axis=1)

    # Pad and truncate all labels so they are the same length
    length = 50
    label_df['Output_Class'] = label_df[['Integerized']].apply(lambda x: pad_sequences(x, maxlen=length, dtype="long", truncating="post", padding="post")[0], axis=1)

    #Create the output_class matrix. Doesn't need to be a tensor, since it won't go into BERT
    label_matrix = np.array([x[0] for x in label_df[['Output_Class']].values])

    return label_matrix
    



"""
The embeddings generated by the BERT model is grouped by sentence.
Since we will classify tokens, not sentences, 
"""
def format_input_for_NER(embedding_matrix):
    #Reshape the embeddings so it's a list of tokens and their embeddings
    input_data = embedding_matrix.reshape(embedding_matrix.shape[0]*embedding_matrix.shape[1],-1)
    
    # Add some informative output
    print(f"Generated INPUT with shape {input_data.shape}")
    return input_data



"""
The embeddings generated by the BERT model is grouped by sentence.
Since we will classify tokens, not sentences, 

Also outputs a dict of index, integer_label, text_label

Also outputs a list of all the labels
"""
def format_output_for_NER(label_matrix):
    tokenizer = AutoTokenizer.from_pretrained("KB/bert-base-swedish-cased-ner")

    #Since we are dealing with token-level classification, break, unravel the sentence grouping we have
    token_labels = label_matrix.reshape(-1,1)
    token_labels = pd.DataFrame(token_labels)

    #Since we are dealing with a multiclass problem, switch to one-hot encoding
    one_hot_token_labels = pd.get_dummies(token_labels[0])

    #Create a dictionary key for the one-hot-encoding indices and labels
    label_dict = {}
    for i in range(one_hot_token_labels.shape[1]):
        integer = int(one_hot_token_labels.columns[i])
        label = tokenizer.decode(integer)
        label_dict.update({i:label})

    # Add some informative output
    print(f"Generated LABELS with shape {one_hot_token_labels.shape}")
    print(f"Generated DICT {label_dict}")
    print(f"Generated LIST of token labels")
    return one_hot_token_labels, label_dict, token_labels

"""
Split data into train and test sets by the given ratio.
Validation sets are not needed, those we get for free with keras models
"""
def split_data(percentage_to_train_on, input_data, output_data):
    ratio = percentage_to_train_on

    split = int(np.ceil(ratio*input_data.shape[0]))

    train_x = input_data[:split]
    train_y = output_data[:split]

    test_x = input_data[split:]
    test_y = output_data[split:]

    return train_x, train_y, test_x, test_y
