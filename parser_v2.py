arts = ['a', 'an', 'the']
nouns = ['boy', 'telescope', 'football', 'jam', 'book', 'saw', 'play']
pronouns = ['i', 'we', 'you', 'they']
verbs = ['saw', 'play', 'eat', 'study', 'jam']
preps = ['with', 'for']
vp_flag = False
from_pp = 0
parse_count = 0


def tostring(parsing):
    string = ''
    for i in parsing:
        string += i

    return string


def test(parsing):
    x1 = parsing.count('(')
    x2 = parsing.count(')')
    if x1 == x2:
        return True
    return False


def S():
    global parse_count
    global pos
    pos = 0
    parsings.append([])
    parsings[parse_count].append('(S')
    NP()
    
    VP()
    if pos == len(sentence):
        parsings[parse_count].append(')')
    
    parse_count += 1


def NP():
    global pos, from_pp
    parsings[parse_count].append('(NP')
    try:
        if sentence[pos].lower() in arts and pos < len(sentence) and sentence[pos+1].lower() in nouns:

            parsings[parse_count].append('(ART '+sentence[pos]+')')
            pos += 1
            parsings[parse_count].append('(N '+sentence[pos]+')')
            pos += 1

            # if pos < len(sentence) and sentence[pos] in preps and (parse_count == 0 or from_pp == 1):
            #     PP()

        elif sentence[pos].lower() in nouns:
            parsings[parse_count].append('(N '+sentence[pos]+')')
            pos += 1
        elif sentence[pos].lower() in pronouns:
            parsings[parse_count].append('(PRON '+sentence[pos]+')')
            pos += 1
        else:
            parsings[parse_count].append('((')
        
        if pos < len(sentence) and sentence[pos].lower() in preps and (parse_count == 0 or from_pp == 1 or vp_flag==False):
                PP()

        if vp_flag == False:
            parsings[parse_count].append(')')
        else:
            parsings[parse_count].append(')')
    except:
        
        parsings[parse_count].append('(')


def PP():
    global pos
    try:
        if sentence[pos].lower() in preps:
            parsings[parse_count].append('(PP(P '+sentence[pos]+')')
            pos += 1
        else:
            parsings[parse_count].append('((')
        NP()
        parsings[parse_count].append(')')
    except:
        parsings[parse_count].append('((')


def VP():
    global pos, vp_flag, from_pp
    vp_flag = True
    
    if sentence[pos].lower() in verbs:
        parsings[parse_count].append('(VP(V '+sentence[pos]+')')
        pos += 1
    else:
        parsings[parse_count].append('((')
    NP()
    if parse_count > 0:
        from_pp = 1
        PP()

    parsings[parse_count].append(')')


s = input('Enter the sentence to be parsed: ').strip()
sentence = s.split(' ')
pos = 0
parsings = []

parse_tree = []
for i in range(2):
    pos = 0
    vp_flag = False
    S()
    tmp = tostring(parsings[i])
    # print(stmp)
    if test(tmp):
        parse_tree.append(tmp)

x = len(parse_tree)
if x:
    for i in parse_tree:
        print(i)
else:
    print('Cannot parse string...')