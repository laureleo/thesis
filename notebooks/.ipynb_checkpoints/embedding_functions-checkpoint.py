import numpy as np 
import torch
from tqdm import tqdm, trange

#Load model
from transformers import AutoModel
#model = AutoModel.from_pretrained('KB/bert-base-swedish-cased')
model = AutoModel.from_pretrained('KB/albert-base-swedish-cased-alpha')


"""
This function takes a single input sentence and mask and generates an embedding for all the tokens in the sentence, using the cpu
"""
def get_embeddings_with_cpu(data_tensor, mask_tensor):
    embeddings = model.forward(input_ids=data_tensor,
        attention_mask=mask_tensor,
        head_mask=None)
    print(embeddings[0].shape)

    return embeddings[0]

"""
For dealing with large amounts of data, a GPU is much faster

The resulting embedding matrix is a three-dimensional tensor corresponding to [Sentence][Words][Embeddings]
embeddings[5][4][:] is thus the embedding of the fourth word in the fifth sentence
"""

def get_embeddings_with_gpu(data_matrix, mask_matrix):
    # Load the device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    #print(f"Using device: {torch.cuda.get_device_name(0)}")

    # Set the model to use the device
    model.cuda()

    # Move the data onto the GPU
    data_matrix = data_matrix.to(device)
    mask_matrix = mask_matrix.to(device)

    # Generate embeddings
    matrix_embedding = model.forward(input_ids=data_matrix,
        attention_mask=mask_matrix,
        head_mask=None)[0]
    #print(f"Embedding generated with shape {batch_embedding.shape}")

    # Make it an ordinary np array instead of a torch
    matrix_embedding = np.array(matrix_embedding.tolist())

    return matrix_embedding

#embedding_matrix = get_embeddings_with_gpu(data_matrix[:10], mask_matrix[:10])

"""
Most people won't be able to load all the data onto the GPU at once however, so it's better to do it in batches.
(50 input sentences take 2803MB on my computer, for example).

This method batchifies and stitches together the batches
"""
def get_embeddings_with_gpu_batch(data_matrix, mask_matrix, batch_size):
    num_items = data_matrix.shape[0]
    num_loops = int(np.ceil(num_items/batch_size))

    start = 0
    end = batch_size
    data_holder = []

    for i in trange(num_loops):
        # Split the data into batches
        data_batch = data_matrix[start:end]
        mask_batch = mask_matrix[start:end]

        #Get the embedding for the batch
        batch_embedding = get_embeddings_with_gpu(data_batch, mask_batch)

        data_holder.append(batch_embedding)

        #Move to next batch
        start += batch_size
        end += batch_size

    # Merge the batches we've generated
    embedding_matrix = np.vstack(data_holder)

    print(f"Final embedding generated with shape {embedding_matrix.shape}")

    return embedding_matrix


#embedding_matrix = get_embeddings_with_gpu_batch(data_tensor_matrix, mask_tensor_matrix, 50)

