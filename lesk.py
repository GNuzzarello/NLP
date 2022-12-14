import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords


def lesk(word, sentence):
    """
    Lesk's algoritm implementation. Given a word and a sentence in which it appears,
    it returns the best sense of the word.

    :param word: word to disabiguate
    :param sentence: sentence to compare
    :return: best sense of word in context (sentence)
    """

    # Calculating the synset of the given word inside WN
    word_senses = wn.synsets(word)
    best_sense = word_senses[0] #most frequent sense for word
    max_overlap = 0

    # I choose the bag of words approach # a feature vector to extract useful feature from a context window
    # bow = an unordered set of words, ignoring their exact position
    # The simplest bag-of-words approach represents the context of a target word by a vector of features,
    # each binary feature indicating whether a vocabulary word w does or doesn’t occur in the context.
    context = bag_of_word(sentence) # set of words in sentence

    for sense in word_senses:
        # set of words in the gloss
        signature = bag_of_word(sense.definition())

        # and examples of the given sense
        examples = sense.examples()
        for ex in examples:
            # after this line, signature will contain for all the words, their
            # bag of words of (sense definition + sense examples)
            signature = signature.union(bag_of_word(ex))

        overlap = compute_overlap(signature, context)
        if overlap > max_overlap:
            max_overlap = overlap
            best_sense = sense

    return best_sense


def bag_of_word(sent):
    """
    Auxiliary function for the Lesk algorithm. Transforms the given sentence
    according to the bag of words approach, apply lemmatization, stop words
    and punctuation removal.

    :param sent: sentence
    :return: bag of words
    """

    stop_words = set(stopwords.words('english'))
    punct = {',', ';', '(', ')', '{', '}', ':', '?', '!'}
    wnl = nltk.WordNetLemmatizer()
    tokens = nltk.word_tokenize(sent)
    tokens = list(filter(lambda x: x not in stop_words and x not in punct, tokens))
    return set(wnl.lemmatize(t) for t in tokens)


def compute_overlap(signature, context):
    """
    Auxiliary function for the Lesk algorithm. Computes the number of words in
    common between signature and context.

    :param signature: bag of words of the signature (e.g. definition/gloss + examples)
    :param context: bag of words of the context (e.g. sentence)
    :return: number of elements in commons
    """

    return len(signature & context)


def get_sense_index(word, sense):
    """
    Given a ambiguous word and a sense of that word, it returns the
    corresponding index of the sense in the synsets list associated with the
    word indices, that starts with 1.

    :param word: ambiguous word (with more that 1 sense)
    :param sense: sense of the word
    :return: index of the sense in the synsets list of the word
    """

    senses = wn.synsets(word)
    return senses.index(sense) + 1

