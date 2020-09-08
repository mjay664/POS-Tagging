import pickle


symbols = ['"', '!', '.', ',', '?', ':', ';', '^', '`', '\'', '-', '_', '(', ')', '{', '}', '[', ']', '#']
digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def isword(string):
    """
    This function checks if the given string is a word.
    @params: string 
    @return: boolean
    """
    if((string[0] in ['\'', '-'] and string[1] not in symbols) or string[0] not in symbols ):
        return True
    return False


def isnum(string):
    """
    This function checks if the given string is a number.
    @params: string
    @return: boolean
    """
    f = string[0]
    l = string[-1]
    if((f in symbols and l in digits) or (f in digits and l in digits)) or ():
        return True
    return False


def preprocess(text):
    """
    This function convert given text to a specified format. 
    @params: text, a string 
    @return: data, a list which contains words of a sentence.
             tags, a list which contains real tags corresponding to the word in sentence.
    """
    data = []
    tags = []
    for i in text:
        tmp_1 = i.split('#')
        data.append(tmp_1[0].lower())
        tags.append(tmp_1[1])
    return data, tags


def backtrack(prev_tags, curr_tags):
    """
    This function extract tags from given data.
    @params: prev_tags, a list of lists which contains possible tags of previous words with calculated probability.
             curr_tags, a list of lists which contains possible tags of current words with calculated probability.
    @return: tags, a list of tags corresponding to words in sentence.
    """

    tags = []
    x = curr_tags[-1]
    max_l = -1
    arg = []
    for i in range(len(x)):
        if x[i][1] > max_l:
            arg = i
            max_l = x[i][1]
    
    tags.append(x[arg][0])
    
    # prev_pointer = prev_tags[i][arg][0]
    for i in range(len(prev_tags) - 1, 0, -1):
        tags.append(prev_tags[i][arg][1])
        arg = prev_tags[i][arg][0]         

    return tags[::-1]


########### Reading stored Lexicon and Bigram probabilities #############
word_prob = pickle.load(open('word_dict', 'rb'))
bigram_prob = pickle.load(open('bigram_dict', 'rb'))
tags = pickle.load(open('tags', 'rb'))


########## Preprocess for Precision, Recall and F Score calculations ##########
org = tags
for i in range(len(org)):
    org[i] = [org[i], [0, 0]]
org = org[1:]
precision = dict(org)
recall = dict(org)

for i in precision:
    precision[i] = [0, 0]
    recall[i] = [0, 0]


######### Reading text file and preprocessing text ##############
f = open(input("Enter file name: "), 'r')

corpus = f.readlines()

tmp_len = len(corpus)

for i in range(tmp_len):
    corpus[i] = corpus[i].replace('\n', '').split('@')
    if isword(corpus[i][-1]) == False:
        pass


############ Viterbi algorithm to assign tags to given sequence of words #########
for i in corpus:

    text, target_tags = preprocess(i)
    actual_tags = []
    pre_list = []
    curr_list = []
    pre = []
    new_word = []
    xx = []
    ind = -1


    for j in text:
        ind += 1
        if word_prob.get(j, -1) == -1:
            if j in symbols:
                word_prob[j] = {'.':1.0}
            elif isnum(j):
                word_prob[j] = {'NUM':1.0}
            else:
                new_word.append(ind)
                xx.append(j)
                word_prob[j.lower()] = {'NOUN':.4, "ADJ":0.1, "VERB":0.1, 'ADV':0.1, 'PRT':0.3}

        if len(pre) == 0:
            pre.append(['^', 1])

        w_p = word_prob[j]
       
        x = list(w_p.keys())
        tmp = []
        for k in range(len(x)):
            max_s = -1
            tmp.append(-1)
            rr = 0
            for l in pre:
                nnt = 0
                if bigram_prob[l[0]].get(x[k], -1) != -1:
                     nnt = bigram_prob[l[0]][x[k]]
                rr = w_p[x[k]] * nnt * l[1]
                
                if rr > max_s:
                    max_s = rr
                    tmp[k] = [pre.index(l), l[0], rr]
            x[k] = [x[k], rr]
        pre_list.append(tmp)
        curr_list.append(x)
        pre = x
    
    actual_tags = backtrack(pre_list, curr_list)

    for i in xx:
        word_prob.pop(i)

    for i in range(len(target_tags)):
        if i in new_word:
            continue
        precision[target_tags[i]][1] += 1
        recall[actual_tags[i]][1] += 1
        if target_tags[i] == actual_tags[i]:
            precision[target_tags[i]][0] += 1
            recall[actual_tags[i]][0] += 1


################ Writing Precision, Recall and F Score to output.txt file ###############
precision.pop('.')
f = open('output.txt', 'w')
for i in precision:
    print('Tag: ', i, file=f)
    prec = precision[i][0]/precision[i][1]
    rec = recall[i][0]/recall[i][1]
    print("Precision: ", prec, end='    ', file=f)
    print("Recall: ", rec, end='    ', file=f)
    f_score = (2 * prec * rec)/(prec + rec) 
    print('F Score: ', f_score, file=f)



