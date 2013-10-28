# Natural Language Processing with Python

O'Reilly, 2009.

## Chapter 1: Language Processing and Python

        # get access to "text1", "text2", ...
        from nltk.book import *

-   With texts you can do:

        # in what context does a word appear?
        text1.concordance("monstrous")

        # what words appears in similar contexts?
        text1.similar("monstrous")

-   Of course the context of given words varies depending on the author! (compare `text1.similar()` to `text2.similar()`).

        # context shared by two or more words
        text1.common_contexts(["monstrous", "very"])

        # generate words in the style of a text
        # uses n-gram language model
        text1.generate()

-   p44: frequency distributions of terms
-   p56: NLP resources

## Chapter 2: Accessing Text Corpora and Lexical Resources

-   p68: table 2-2: some corpora included with NLTK.
-   p72, table 2-3: basic corpus functions, e.g. words, sentences.
-   p73: loading your own corpus
    -   `PlaintextCorpusReader` is first start maybe.
-   p77: generating text with bigrams

        sent = ['In', 'the', 'beginning', ...]
        nltk.bigrams(sent) # calculates bigrams
        
        # or
        nltk.trigrams(sent)

        # or
        nltk.ngrams(sent, 4)

-   p81: **lexical resource** is collection of words and/or phrases with associated information, like part-of-speech (POS) tagging or sense definitions.
    -   A **lexical entry** has a **headword** (aka **lemma**) and other additional information.
-   p82: stopwords

        from nltk.corpus import stopwords
        stopwords.words('english')

-   p83: solving puzzles based on scrambled letters.
-   p84: CMU Pronouncing Dictionary
-   p89: WordNet, senses, synonyms, other word senses.

## Chapter 3: Processing Raw Text

-   **Tokenization**: break up a string into words *and* punctuation.

        # split into words and punctuation
        tokens = nltk.word_tokenize(raw)

-   **Normalized** text is usually lower cased, but also we go further and strip off affixes, a task known as **stemming**.
    -   Checking that a resulting stem is in a dictionary is a task called **lemmatization**.
-   Stemming:

        # Choose a stemmer; not well-defined, try them all.
        porter = nltk.PorterStemmer()
        lancaster = nltk.LancasterStemmer()

        # Use a stemmer.
        [porter.stem(t) for t in tokens)]

-   Lemmatization (remove affixes only if resulting form is in a dictionary)

        wnl = nltk.WordNetLemmatizer()
        [wnl.lemmatize(t) for t in tokens]

-   Another normalization task is identifying **non-standard words** (numbers, abbreviations, dates), and mapping them to a special token (0.0, AAA, etc.)
    -   Keeps the vocabulary small, improves accuracy for many language modelling tasks.

-   p133: NLTK's regular expression tokenizer. Similar to `re.findall()`.

-   Sentence **segmentation**; uses the Punkt sentence segmenter (Kiss & Strunk 2006).

        # split into sentences, which then can be split
        # with nltk.word_tokenize()
        sents = nltk.sent_tokenize(raw)

## Chapter 4: Writing Structured Programs

skipped

## Chapter 5: Categorizing and Tagging Words

-   A **POS tagger** processes a sequence of words and attaches a POS **tag** to each word.

        words = nltk.word_tokenize(text)
        nltk.pos_tag(words)

-   You can get help of what the tags mean using regular expressions:

        nltk.help.upenn_tagset('NN.*')
        nltk.help.brown_tagset('NN.*')

-   NLTK can convert from standard POS tag convention to 2-tuple:

        nltk.tag.str2tuple('fly/NN')

-   p205: different corpora use different tagsets. table 5-1 shows the simplified POS tagset that NLTK can map them to.
-   p220: automatic tagging.
    -   evaluate different tagging schemes, and see how they perform on the gold standard corpus.
-   p225: how to train a `nltk.UnigramTagger`.
    -   how to split into training and testing data.
    -   p227: NLTK taggers are designed to work with lists of sentences.
-   p227: combining taggers
    -   try bigram, but if no instance try unigram, but if no instances use default:

        t0 = nltk.DefaultTagger('NN')
        t1 = nltk.UnigramTagger(train_sents, backoff=t0)
        t2 = nltk.BigramTagger(train_sents, backoff=t1)
        t3 = nltk.TrigramTagger(train_sents, backoff=t2)
        t3.evaluate(test_sents)

        # this tagger will disgard contexts it has only
        # seen once or twice.
        nltk.BigramTagger(sents, cutoff=2, backoff=t1)

-   p228: how to handle **out-of-vocabulary** items?
    -   Useful to limit vocabulary to most frequent n words, then replace every other word with a special word "UNK".
-   p229: evaluating tags against gold standard using a **confusion matrix**.

-   p230: how to tag properly using sentence boundaries

-   p230: **transformation-based tagging**, i.e. Brill tagging.
    -   supervised learning.
    -   guess the tag of each word, then go back and fix the mistakes.

-   p232: how to determine the category of a word
    -   **morphological** clues; suffix, prefix.
    -   **syntatic** clues; adjectives usually immediately before nouns.
    -   **semantic** clues; use meaning of word, but hard to formalize.

## Chapter 6: Learning to Classify Text

-   p244: figure 6-1, diagram of supervised classification.
-   p246: features are dictionaries, and NLTK automatically does dimensionality reduction. 
    -   Throw the kitchen sink of features at it and it'll tell you which were useful.
    -   But use too many features and it might **overfit**.
-   p249: document classification into negative/positive based on whether it contains a word.
-   p251: using a decision tree classifier to construct a regular expression based part-of-speech tagger.
-   p253: POS classifier whose feature detector examines context of the word.
-   p254: **consecutive classification**, or **greedy sequence classification**.
-   p255: mention of **Hidden Markov Models**
    -   !!AI In IPython run "nltk.tag??" to see list of taggers, and how to call `tagger.tag(tokens)` on any tagger. One day might be fun to train/test HMM taggers etc.
-   p256: sentence segmentation using supervised classification.
-   p257: recognising **dialogue acts** (e.g. greting, question, answer, assertion, clarification, etc.) based on NPS Chat Corpus.
-   p257: **recognizing textual entailment** (RTE), whether a text T entails another.
-   p260: evaluation
    -   **test set**: held back from training set.
    -   **accuracy**: pecentage of inputs in test set that the classifier correctly labelled.
    -   **precision** vs. **recall**.
    -   **confusion matrix**
    -   p263: **N-folds cross-validation**.
        -   compare how much scors vary across N training sets. If too variable than evaluation score is suspect.
-   p264: **decision trees** and **information gain**
-   p268: **Naive Bayes** classifiers
-   p271: **smoothing** techniques, like **heldout estimation**.
-   p272: **maximum entropy** classifiers
-   p276: generative vs. conditional classifiers
    -   **generative** builds a model that predicts P(input, label), a joint probability. Strictly more powerful but has more "free parameters", so more difficult to train and less accurate.
    -   **conditional** predicts P(label|input). Can answer less questions but more accurate for what it does.
-   p279: referencs on machine learning and NLP.

## Chapter 7: Extracting Information from Text

-   p285: information extraction pipeline
    -   text -> sentence segmentation -> sentences
    -   sentences -> tokenization -> tokenized sentences
    -   tokenized sentences -> POS tagging -> POS-tagged sentences
    -   POS-tagged sentences -> entity recognition -> chunked sentences
    -   chunked sentences -> relation recognition -> relations

-   p287: **noun phrase chunking**, aka **NP-chunking**.
    -   NP-chunks that are groups using brackets.
    -   POS tagging is an important input to this.

-   p291: **IOB** tags (insides, outside, between) on each POS tag to indicate whether it is inside, between or outside of a particular chunk.
-   p295: unigram chunker (rather than assigning POS tags to words, we're assigning POS-tagged words to chunks).
-   p297: Noun phrase chunking with a consecutive classifier
-   p299: recursive cascaded chunkers

-   p305: **named-entity recognition**, and using classifiers to do this.

        sent = nltk.corpus.treebank.tagged_sents()[22]

        # set binary=True to identify whether or not it is
        # a named entity. Else it will sub-categorise, e.g.
        # PERSON, ORGANIZATION, etc.
        nltk.ne_chunk(sent, binary=True)

-   p306: relation extraction
-   p308: chapter references.

## Chapter 8: Analyzing Sentence Structure

-   Context-Free Grammrs, parsing.
-   p315: great example using `nltk.parse_cfg` to show ambiguity in the phrase "I shot an elephant in my pajamas".

