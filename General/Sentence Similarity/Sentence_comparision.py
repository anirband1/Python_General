import sys


# removes extra spaces
def normalize(sentence):
    sentence = sentence.strip()
    sentence = sentence.replace("  ", " ")
    if sentence == '':
        print("Invalid. Sentence cannot be blank")
        sys.exit()
    if ("  " in sentence):
        normalize(sentence)
    else:
        return sentence


def sentence_in_sentence(sentence1, sentence2):
    if len(sentence1) <= len(sentence2):
        if sentence1 in sentence2:
            print("The sentences are 100% similar")
            sys.exit()
        else:
            return stopwords_and_case(sentence1), stopwords_and_case(sentence2)
    elif sentence2 in sentence1:
        print("The sentences are 100% similar")
        sys.exit()
    else:
        return stopwords_and_case(sentence2), stopwords_and_case(sentence1)


# removes stopwords from sentences and converts them to lowercase
def stopwords_and_case(sentence):
    l_new_sentence = []
    l_sentence = sentence.split(" ")
    for word in l_sentence:
        if word.lower() not in l_stopwords:
            l_new_sentence.append(word.lower())
    return l_new_sentence


# function to cut off decimal points
def cutoff(num, places):
    temp = num * (10**places)
    temp = int(temp)
    return temp / (10**places)


def compare_lists(list1, list2):
    maximum = 0
    total = 0
    similarity = 0

    for word1 in list1:
        maximum = 0
        for word2 in list2:
            temp_sim = compare_words(word1, word2)
            word_similarity = max(maximum, temp_sim)
            maximum = word_similarity
        similarity += word_similarity
        total += 100

    try:
        return ((similarity / total) * 100)
    except (ZeroDivisionError):
        return (0)


def compare_words(word1, word2):
    similarity = 0

    # pass, pass
    if len(word1) == len(word2) and (word1 in word2 or word2 in word1):
        similarity = 90

    elif len(word1) < len(word2) and word1 in word2:
        suffix = word2[len(word1):]
        # pass, passed
        if suffix in l_suffixes:
            similarity = 80
        # pass, passthrough
        else:
            similarity = 50
    elif len(word2) < len(word1) and word2 in word1:
        suffix = word1[len(word2):]
        # passed, pass
        if suffix in l_suffixes:
            similarity = 80
        # passthrough, pass
        else:
            similarity = 50
    # pass, encompass
    else:
        similarity = 0

    return (similarity)


# making a list of stopwords from Stopwords.txt file
l_stopwords = []
with open("Stopwords.txt", "r") as f:
    for word in f:
        word = word.split("\n")[0]
        l_stopwords.append(word)

# making a list of suffixes from Suffixes.txt file
l_suffixes = []
with open("Suffixes.txt", "r") as f:
    for word in f:
        word = word.split("\n")[0]
        l_suffixes.append(word)

# main
sentence1 = normalize(input("First sentence:  "))
sentence2 = normalize(input("Second sentence:  "))

# removing stopwords and changing case for the 2 sentences
l_words1, l_words2 = sentence_in_sentence(sentence1, sentence2)

# to see the list of words without stopwords
# print(f"first list: {l_words1}\nsecond list: {l_words2}")

# comparing every word in each sentence
similarity_in_words = compare_lists(l_words1, l_words2)

print(
    f"The first sentence is {cutoff(similarity_in_words, 3)}% similar to the second one"
)

# TO DO:
# Suffixes logic
# [] , ['hello', 'chair'] total += 200