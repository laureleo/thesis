import numpy as np


sentence = ['I', 'sin', 'första', 'reaktion', 'på', 'Sovjetledarens', 'varningar', 'deklarerade', 'Litauens', 'president', 'Vytautas Landsbergis', 'att', '"', 'nu', 'avvisar', 'Gorbatjov', 'vår', 'utsträckta', 'hand', 'med', 'extremt', 'skarpa', 'och', 'hämndlystna', 'ord', '"', '.']

labels = ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'LOC', 'O', 'PRS', 'O', 'O', 'O', 'O', 'PRS', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']

tokens = ['I', 'sin', 'första', 'reaktion', 'på', 'Sovjet', '##ledaren', '##s', 'varningar', 'deklarerade', 'Litauen', '##s', 'president', 'V', '##yta', '##uta', '##s', 'Land', '##sberg', '##is', 'att', '"', 'nu', 'avvisar', 'Gorbatjov', 'vår', 'utsträck', '##ta', 'hand', 'med', 'extremt', 'skarpa', 'och', 'hämnd', '##lyst', '##na', 'ord', '"', '.']

def get_named_entity_indices(sentence, labels):
    ne_indices = []
    nes = []
    for index, label in enumerate(labels):
        if label != 'O':
            ne_index = index
            ne = sentence[index]
            ne_indices.append(ne_index)
            nes.append(ne)
    return ne_indices, nes

ne_indices, nes = get_named_entity_indices(sentence, labels)
print(ne_indices, nes)

UNVISITED_ENTITIES = ne_indices
UNVISITED_ENTITIES.reverse()
VISITED_ENTITES = []

for index, token in enumerate(tokens):
    if(len(UNVISITED_ENTITIES) > 0):
        print(f"Checking index {index}, token {token}, Next to check is {UNVISITED_ENTITIES[-1]}")
        if token.startswith('##'):
            #Increment the index where we would expect to find a NE, since we've found a split word in between
            UNVISITED_ENTITIES = [x + 1 for x in UNVISITED_ENTITIES]
            print(UNVISITED_ENTITIES)

        
        #We should have a NE if we've reached this index#
        if UNVISITED_ENTITIES[-1] == index:
            #Remove this named entity from the list
            new_index = UNVISITED_ENTITIES.pop()
            print(f"Reached entity, popping {new_index}")
            print(f"Remaining {UNVISITED_ENTITIES}")
            VISITED_ENTITES.append(new_index)
        

        #While the next word begins with ##, we've split the NE into multiple parts. BIO tag them accordingly.


print(VISITED_ENTITES)

def check_if_they_match(tokens, original_indices, adjusted_indices):
    print("Checking if tokens have correct labels")
    for index in range(len(original_indices)):
        original_index = original_indices[index]
        new_index = adjusted_indices[index]
        print(f"Original label {labels[original_index]}")
        print(f"Original word {sentence[original_index]}")
        print(f"Token at new index {tokens[new_index]}")

check_if_they_match(tokens, ne_indices, VISITED_ENTITES)

