sentence1 = "hello from the other side"

similarity = 0

words_in_sentence1 = sentence.split(" ")


def letter_comparision(word1, word2):
    if len(word1) < len(word2):
        if word1 in word2:
            similarity += 1
    elif word2 in word1:
        similarity += 1

    return similarity
