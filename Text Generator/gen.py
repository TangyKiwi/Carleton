# pdf to text https://pdftotext.com/
import random
import math
import nltk
from nltk.corpus import opinion_lexicon


# directory = "../../../../../CourseMaterials/gutenberg/data/text/PG"
# books = [1155, 61, 863]
reports = ["sr15_spm_final",
           "ST1.5_OCE_LR",
           "global_warming_free_state_report",
           "climate-change-2018"]
dict = {}
startWords = []

def fixPairs(tokens):
    for x in range(len(tokens)):
        if x < len(tokens) and '“' in tokens[x]:
            for y in range(x + 1, len(tokens)):
                if '”' in tokens[y]:
                    tokens[x] = " ".join(tokens[x : y + 1])
                    tokens = tokens[:x + 1] + tokens[y + 1:]
                    x = y + 1
                    break

    for x in range(len(tokens)):
        if x < len(tokens) and '(' in tokens[x] and ')' not in tokens[x]:
            for y in range(x + 1, len(tokens)):
                if ')' in tokens[y]:
                    tokens[x] = " ".join(tokens[x : y + 1])
                    tokens = tokens[:x + 1] + tokens[y + 1:]
                    x = y + 1
                    break

    return tokens

def read(file):
    f = open(file + ".txt", 'r').read()

    while "{" in f:
        f = f[:f.index("{")] + f[f.index("}") + 1:]

    while "[" in f:
        f = f[:f.index("[")] + f[f.index("]") + 1:]

    return fixPairs(f.split())

# filters the text so only biased / neutral sentences are kept
# 'pos' for positive, 'neu' for neutral, 'neg' for negative
def biasRead(file, bias):
    f = open(file + ".txt", 'r').read()

    while "{" in f:
        f = f[:f.index("{")] + f[f.index("}") + 1:]

    while "[" in f:
        f = f[:f.index("[")] + f[f.index("]") + 1:]

    sentences = nltk.sent_tokenize(f)
    for sent in sentences:
        pos_neg = sentiment(sent)
        # print(sent + " : " + pos_neg)
        if pos_neg != bias and pos_neg != 'neu':
            sentences.remove(sent)

    words = []
    for sent in sentences:
        tokens = nltk.word_tokenize(sent)
        for token in tokens:
            words.append(token)

    return fixPairs(words)

def sentiment(sentence):
    words = nltk.word_tokenize(sentence)
    pos_neg = 0
    for word in words:
        if word in opinion_lexicon.positive():
            pos_neg += 1
        elif word in opinion_lexicon.negative():
            pos_neg -= 1

    if pos_neg >= 1:
        return 'pos'
    elif pos_neg <= -1:
        return 'neg'
    return 'neu'

def makeDict(tokens):
    for x in range(len(tokens) - 3):
        key = tokens[x]
        if 'A' <= key[0] <= 'Z' and key[len(key) - 1] not in ".!?”'":
            startWords.append(key + " " + tokens[x + 1])

        if key + " " + tokens[x + 1] in dict and tokens[x + 2] not in dict[key + " " + tokens[x + 1]]:
            dict[key + " " + tokens[x + 1]].append(tokens[x + 2] + " " + tokens[x + 3])
        else:
            dict[key + " " + tokens[x + 1]] = [tokens[x + 2] + " " + tokens[x + 3]]

def genText():
    start = random.choice(startWords)
    out = ""
    out += start + " "

    seed = start
    sent = 0
    while sent <= 10:
        seed = random.choice(dict[seed])
        out += seed + " "
        if seed[len(seed) - 1] in ".!?":
            sent += 1

    print(out)
    # f = open("out.txt", "a+")
    # f.write(out)
    # f.close()

def main():
    # for book in books:
    #     makeDict(read(book))
    for report in reports:
        makeDict(read(report))

    genText()

if __name__ == "__main__":
    main()

# STUFF TO WORK ON
# start can not have a period --> DONE
# FIX QUOTES, parentheses, brackets, etc. everything that comes in pairs --> NEEDS TESTING
#   read through array, find quote to next quote then mash together all indices
#   in between to create quote as one seed, same for parenthese etc.
# separate reports by introdution, header, evidence, etc.
# use ntlk positive sentiments to make BIASED reports yum yum --> IN PROGRESS
# add weights?
# every sentence must have a subject / verb
