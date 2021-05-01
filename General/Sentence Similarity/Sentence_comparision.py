# removes extra spaces
def normalize(sentence):
    sentence = sentence.strip()
    sentence = sentence.replace("  ", " ")
    return sentence


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


# main processing
def compare_in_words(list1, list2):
    word_similarity = 0
    total = 0
    # remove same words in both lists
    for word in list1[::-1]:
        if word in list2:
            list1.remove(word)
            list2.remove(word)
            word_similarity += 100
            total += 100

    # finding how similar are 2 words in a list
    # ex. "pass" and "passed"; since "pass" is in "passed", they are 98% similar (number 98 is arbitrary)
    for word1 in list1:
        for word2 in list2:
            if len(word1) < len(word2):
                if word1 in word2:
                    word_similarity += 98
                total += 100
            elif len(word2) < len(word1):
                if word2 in word1:
                    word_similarity += 98
                total += 100
    try:
        print(f"{word_similarity}/{total}")
        print(word_similarity / total * 100)
        return (word_similarity / total * 100)
    except (ZeroDivisionError):
        return float(word_similarity)


# making a list of stopwords from Stopwords.txt file
l_stopwords = []
with open("Stopwords.txt", "r") as f:
    for word in f:
        word = word.split("\n")[0]
        l_stopwords.append(word)

# main
sentence1 = normalize(input("First sentence:  "))
sentence2 = normalize(input("Second sentence:  "))

# removing stopwords and changing case for the 2 sentences
l_words1 = stopwords_and_case(sentence1)
l_words2 = stopwords_and_case(sentence2)

# to see the list of words without stopwords
print(f"first list: {l_words1}\nsecond list: {l_words2}")

# comparing every word in each sentence
similarity_in_words = compare_in_words(l_words1, l_words2)

print(f"The sentences are {cutoff(similarity_in_words, 3)}% similar")

# TO DO:
# [] , ['hello', 'chair'] total += 200