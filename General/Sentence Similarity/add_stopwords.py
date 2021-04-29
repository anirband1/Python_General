from nltk.corpus import stopwords

# list of stopwords (from stopwords library)
l_stopwords = sorted(stopwords.words("english"))

# add stopwords to Stopwords.txt
with open("Stopwords.txt", "w") as f:
    for word in l_stopwords:
        f.write(f"{word}\n")
