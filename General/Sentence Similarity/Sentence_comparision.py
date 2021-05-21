import sys

__BREAK_SAME_WORD = 90
__ENDING_SUFFIX = 80
__ENDING_NOT_SUFFIX = 50
__CUTOFF = 5


# public function, called by main program
def compare(sentence1, sentence2):

    sentence1 = __normalize(sentence1)
    sentence2 = __normalize(sentence2)

    # removing stopwords and changing case for the 2 sentences
    # returns None if word in description
    try:
        l_words1, l_words2 = __sentence_in_sentence(sentence1, sentence2)
    except:
        return (100.0)

    # comparing every word in each sentence
    similarity_in_words = __compare_lists(l_words1, l_words2)

    return __cutoff(similarity_in_words, __CUTOFF)


# removes extra spaces
def __normalize(sentence):
    sentence = sentence.strip()
    while ("  " in sentence):
        sentence = sentence.replace("  ", " ")

    return sentence


# if smaller sentence is a part of bigger sentence, returns 100% similar
# if it isn't, makes the smaller sentence the main sentence to compare with
def __sentence_in_sentence(sentence1, sentence2):
    if len(sentence1) <= len(sentence2):
        if sentence1 in sentence2:
            return  # return None error resolved in compare(); try-except
        else:
            return __create_list(sentence1), __create_list(sentence2)
    elif sentence2 in sentence1:
        return  # return None error resolved in compare(); try-except
    else:
        return __create_list(sentence2), __create_list(sentence1)


# removes stopwords from sentences and converts them to lowercase
def __create_list(sentence):

    # making a list of stopwords from Stopwords.txt file
    l_stopwords = []
    with open("lib/Stopwords.txt", "r") as f:
        for word in f:
            word = word.split("\n")[0]
            l_stopwords.append(word)

    # making a list of special characters from Special_chars.txt file
    l_special = []
    with open("lib/Special_chars.txt", "r") as f:
        for word in f:
            word = word.split("\n")[0]
            l_special.append(word)

    # returns a list of non-stopwords
    l_new_sentence = []
    l_sentence = sentence.split(" ")
    for word in l_sentence:
        for char in l_special:
            if char in word:
                word = word.replace(char, "")
        if word.lower() not in l_stopwords:
            l_new_sentence.append(word.lower())

    l_new_sentence = [i for i in l_new_sentence if i != '']

    return l_new_sentence


# function to cut off decimal points
def __cutoff(num, places):
    temp = num * (10**places)
    temp = int(temp)
    return temp / (10**places)


# compare every word in first sentence with second sentence
def __compare_lists(list1, list2):
    maximum = 0
    total = 0
    similarity = 0

    for word1 in list1:
        maximum = 0
        for word2 in list2:
            temp_sim = __compare_words(word1, word2)
            word_similarity = max(maximum, temp_sim)
            maximum = word_similarity
        similarity += word_similarity
        total += 100

    try:
        return (similarity / total) * 100
    except (ZeroDivisionError):
        return 0


# if program enters this function, max value is changed from 100 to 90
# return similarity between 2 words (value arbitrary)
def __compare_words(word1, word2):

    # making a list of suffixes from Suffixes.txt file
    l_suffixes = []
    with open("lib/Suffixes.txt", "r") as f:
        for word in f:
            word = word.split("\n")[0]
            l_suffixes.append(word)

    similarity = 0

    # pass, pass
    if len(word1) == len(word2) and (word1 in word2 or word2 in word1):
        similarity = __BREAK_SAME_WORD

    elif len(word1) < len(word2) and word1 in word2:
        suffix = word2[len(word1):]
        # ring , spring
        if word2[:len(word1)] != word1:
            similarity = 0
        # pass, passed
        elif suffix in l_suffixes:
            similarity = __ENDING_SUFFIX
        # pass, passthrough
        else:
            similarity = __ENDING_NOT_SUFFIX

    elif len(word2) < len(word1) and word2 in word1:
        suffix = word1[len(word2):]
        # spring , ring
        if word1[:len(word2)] != word2:
            similarity = 0
        # passed, pass
        elif suffix in l_suffixes:
            similarity = __ENDING_SUFFIX
        # passthrough, pass
        else:
            similarity = __ENDING_NOT_SUFFIX

    # pass, encompass
    else:
        similarity = 0

    return (similarity)
