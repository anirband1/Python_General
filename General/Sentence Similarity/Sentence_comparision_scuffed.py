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


# finding how similar are 2 words in a list
# ex. "pass" and "passed"; since "pass" is in "passed", they are 98% similar (number 98 is arbitrary)
def compare_in_words(list1, list2):
    word_similarity = 0
    total = 0
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
            elif word1 in word2:
                word_similarity += 100
                total += 100
    try:
        return (word_similarity / total * 100)
    except (ZeroDivisionError):
        return float(word_similarity * 100)


def compare_sets(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    intersection = set1 & set2
    union = set1 | set2
    try:
        jaccard_percent = (len(intersection) / len(union)) * 100
        return jaccard_percent
    except:
        # print("The sentences are 100% similar")
        pass


# making a list of stopwords from Stopwords.txt file
l_stopwords = []
with open("Stopwords.txt", "r") as f:
    for word in f:
        word = word.split("\n")[0]
        l_stopwords.append(word)

sentence1 = normalize(input("First sentence:  "))
sentence2 = normalize(input("Second sentence: "))

# removing stopwords and changing case for the 2 sentences
l_words1 = stopwords_and_case(sentence1)
l_words2 = stopwords_and_case(sentence2)

# to see the list of words without stopwords
# print(f"first list: {l_words1}\nsecond list: {l_words2}")

# comparing every word in each sentence
similarity_in_words = compare_in_words(l_words1, l_words2)
jaccard_percent = compare_sets(l_words1, l_words2)

print(
    f"The sentences are {(similarity_in_words * jaccard_percent)/100}% similar"
)
