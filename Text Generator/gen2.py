import random
import math
import nltk
from nltk.corpus import opinion_lexicon

directory = "gen"#"Text/PG61_text.txt (Communist Manifesto)"
reports = ["sr15_spm_final",
           "ST1.5_OCE_LR",
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

    return tokens + list(tokens[0]) + list(tokens[1])

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
    for x in range(len(tokens) - 2):
        key = (tokens[x], tokens[x + 1])
        if 'A' <= key[0][0] <= 'Z' and key[1][len(key[1]) - 1] not in ".!?”'":
            startWords.append(key)

        if key in dict and tokens[x + 2] not in dict[key]:
            dict[key].append(tokens[x + 2])
        else:
            dict[key] = [tokens[x + 2]]

def genText():
    start = random.choice(startWords)
    out = ""
    out += start[0] + " " + start[1] + " "

    seed = start
    sent = 0
    counter = 0
    while sent <= 2:
        pr = random.choice(dict[seed])
        out += pr + " "
        counter += 1
        if counter >= 10:
            out += "\n"
            counter = 0
        if pr[len(pr) - 1] in ".!?":
            sent += 1

        temp = list(seed)
        temp[0] = temp[1]
        temp[1] = pr
        seed = tuple(temp)

    print(out)
    # f = open("out.txt", "a+")
    # f.write(out)
    # f.write("\n\n\n")
    # f.close()

def main():
    for report in reports:
        makeDict(read("Text/" + report))
#        makeDict(biasRead("Text/" + report, 'pos'))
#        makeDict(biasRead("Text/" + report, 'neg'))

    genText()

if __name__ == "__main__":
    main()

# STUFF TO WORK ON
# start can not have a period --> DONE
# FIX QUOTES, parentheses, brackets, etc. everything that comes in pairs --> DONE
#   read through array, find quote to next quote then mash together all indices
#   in between to create quote as one seed, same for parenthese etc.
# separate reports by introdution, header, evidence, etc. --> manually done
# use ntlk positive sentiments to make BIASED reports yum yum --> IN PROGRESS
# add weights?
# every sentence must have a subject / verb

# HOW TO FOOL ROLAND 101
# - want big words paragraph --> one real, one generated + editing
# - have him read side by side to compare
# - go multiple times, with multiple paragraphs
# - time how long it takes to recognize, or forfeit time if he gets it wrong
# OWO WE DID IT
