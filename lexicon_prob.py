import pickle


word_dict = dict()


def isword(string):
    """
    This function checks if the given string is a word.
    @params: string 
    @return: boolean
    """

    if(string[0].isupper() or string[0].islower()):
        return True
    return False

############## Reading training file and preprocessing ##########
f = open(input('Enter the full path of training file: '), 'r')

corpus = f.readlines()

tmp_len = len(corpus)

for i in range(tmp_len):
    corpus[i] = corpus[i].replace('\n', '').split('@')


############# Calculating Lexicon Probabilities #############    
for i in corpus:
    for j in i:
        tmp = j.split('#')
        tmp[0] = tmp[0].lower()
        if(word_dict.get(tmp[0], -1) == -1):
            x = {'count':1, tmp[1]:1}
            word_dict[tmp[0]] = x

        else:
            x = word_dict[tmp[0]]
            x['count'] += 1
            if (x.get(tmp[1], -1) == -1):
                x[tmp[1]] = 1

            else:
                x[tmp[1]] += 1

list_keys = word_dict.keys()


for i in list_keys:
    x = word_dict[i]
    count = x.pop('count')
    list_x_keys = x.keys()
    for j in list_x_keys:
        x[j] /= count

###### Saving calculated probabilities ###########
pickle.dump(word_dict, open('word_dict', 'wb'))