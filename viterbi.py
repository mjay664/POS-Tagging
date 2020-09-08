import pickle


symbols = ['"', '!', '.', ',', '?', ':', ';', '^', '`', '\'', '-', '_', '(', ')', '{', '}', '[', ']', '#']
digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def isword(string):
    if((string[0] in ['\'', '-'] and string[1] not in symbols) or string[0] not in symbols ):
        return True
    return False


def isnum(string):
    f = string[0]
    l = string[-1]
    if((f in symbols and l in digits) or (f in digits and l in digits)) or ():
        return True
    return False


def preprocess(text):
    data = []
    tags = []
    for i in text:
        tmp_1 = i.split('#')
        data.append(tmp_1[0].lower())
        tags.append(tmp_1[1])
    return data, tags


def backtrack(prev_tags, curr_tags):
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


word_prob = pickle.load(open('word_dict', 'rb'))
bigram_prob = pickle.load(open('bigram_dict', 'rb'))
tags = pickle.load(open('tags', 'rb'))

org = tags
for i in range(len(org)):
    org[i] = [org[i], [0, 0]]
org = org[1:]

f = open(input("Enter file name: "), 'r')

corpus = f.readlines()
# corpus = ['My#PRON@name#NOUN@is#VERB@Jay#NOUN@.#.\n']

tmp_len = len(corpus)

for i in range(tmp_len):
    corpus[i] = corpus[i].replace('\n', '').split('@')
    if isword(corpus[i][-1]) == False:
        pass

precision = dict(org)
recall = dict(org)

total = 0
count = 0
print(word_prob['^'])

exit(0)
xx = []
for i in corpus:
    text, target_tags = preprocess(i)
    actual_tags = []
    pre_list = []
    curr_list = []
    pre = []
    indiff = -1
    new_word = []
    for j in text:
        indiff += 1
        if word_prob.get(j, -1) == -1:
            continue
            # if j in symbols:
            #     word_prob[j] = {'.':1.0}
            # elif isnum(j):
            #     word_prob[j] = {'NUM':1.0}
            # else:
            #     xx.append([j, i])
            #     word_prob[j.lower()] = {'NOUN':1.0}

        # if isword(j) or 1:
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

    # print(actual_tags)
    # for i in range(len(target_tags)):
    #     precision[target_tags[i]][1] += 1
    #     recall[actual_tags[i]][1] += 1
    #     if target_tags[i] == actual_tags[i]:
    #         precision[target_tags[i]][0] += 1
    #         recall[actual_tags[i]][0] += 1


    for i in range(len(target_tags)):
        total += 1
        if target_tags[i] == actual_tags[i]:
            count += 1

print(count)
print(total)
print(count/total)
print(xx, file=open('fir.txt', 'w'))



