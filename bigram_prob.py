import pickle


symbols = ['"', '!', '.', ',', '?', ':', ';', '^', '`', '\'', '-', '_', '(', ')', '{', '}', '[', ']', '#']

bigram_dict = dict()
tags = dict()

def isword(string):
    """
    This function checks if the given string is a word.
    @params: string 
    @return: boolean
    """
    if((string[0] in ['\'', '-'] and string[1] not in symbols) or string[0] not in symbols ):
        return True
    return False

############## Reading training text file and preprocessing #################
f = open(input('Enter the full path of training file: '), 'r')

corpus = f.readlines()

tmp_len = len(corpus)

for i in range(tmp_len):
    corpus[i] = ['^#^'] + corpus[i].replace('\n', '').split('@')
    if(isword(corpus[i][-1]) == False):
        corpus[i].pop()
    corpus[i] += ['`#.']
    

############## Calculating Bigram Probabilities ###################
tags['^'] = 0   
for i in corpus:
    tags['^'] += 1
    for j in range(len(i)-1):

        tmp_1 = i[j].split('#')[1]
        if tmp_1 == '.':
            pass
        if tags.get(tmp_1, -1) == -1:
            tags[tmp_1] = 1
        else:
            tags[tmp_1] += 1

        tmp_2 = i[j+1].split('#')[1]
        if tags.get(tmp_2, -1) == -1:
            tags[tmp_2] = 1
        else:
            tags[tmp_2] += 1
        
        if(bigram_dict.get(tmp_1, -1) == -1):
            x = {tmp_2:1}
            bigram_dict[tmp_1] = x

        else:
            x = bigram_dict[tmp_1]
            if (x.get(tmp_2, -1) == -1):
                x[tmp_2] = 1
            else:
                x[tmp_2] += 1

tag_keys = tags.keys()
for i in tag_keys:
    x = bigram_dict[i]
    count = tags[i]
    list_x_keys = x.keys()
    for j in list_x_keys:
        x[j] /= count

######## Saving Calculated Probabilities #############
pickle.dump(bigram_dict, open('bigram_dict', 'wb'))
pickle.dump(list(tag_keys), open('tags', 'wb'))