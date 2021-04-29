sentence1 = "hello from the other side"

l_stopwords = []

# making a list of stopwords from Stopwords.txt file
with open("Stopwords.txt", "r") as f:
    for word in f:
        word = word.split("\n")[0]
        l_stopwords.append(word)

print(l_stopwords)
