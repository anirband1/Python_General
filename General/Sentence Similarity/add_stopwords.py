from nltk.corpus import stopwords

l_stopwords = sorted(stopwords.words("english"))

with open("Stopwords.txt", "w") as filename:
    for word in l_stopwords:
        filename.write(f"{word}\n")
