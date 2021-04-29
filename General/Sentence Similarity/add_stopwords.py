from nltk.corpus import stopwords

l_stopwords = sorted(stopwords.words("english"))

with open("Stopwords.txt", "w") as f:
    for word in l_stopwords:
        f.write(f"{word}\n")
