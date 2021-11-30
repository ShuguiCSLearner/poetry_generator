import nltk
import pronouncing
import random

my_corpus = nltk.corpus.gutenberg.words('shakespeare-hamlet.txt')
bigrams = nltk.bigrams(my_corpus)
cfd = nltk.ConditionalFreqDist(bigrams)

# This function takes two inputs:
# source - a word represented as a string
# num - an integer
# The function will generate num random related words using
# the CFD based on the bigrams in our corpus, starting from
# source. So, the first word will be generated from the CFD
# using source as the key, the second word will be generated
# using the first word as the key, and so on.
# If the CFD list of a word is empty, then a random word is
# chosen from the entire corpus.
# The function returns a num-length list of words.
def random_word_generator(source = None, num = 1):
    result = []
    while source == None or not source[0].isalpha():
        source = random.choice(my_corpus)
    word = source
    result.append(word)
    while len(result) < num:
        if word in cfd:
            init_list = list(cfd[word].keys())
            choice_list = [x for x in init_list if x[0].isalpha()]
            if len(choice_list) > 0:
                newword = random.choice(choice_list)
                result.append(newword)
                word = newword
            else:
                word = None
                newword = None
        else:
            while newword == None or not newword[0].isalpha():
                newword = random.choice(my_corpus)
            result.append(newword)
            word = newword
    return result

# This function takes a single input:
# word - a string representing a word
# The function returns the number of syllables in word as an
# integer.
# If the return value is 0, then word is not available in the CMU
# dictionary.
def count_syllables(word):
    phones = pronouncing.phones_for_word(word)
    count_list = [pronouncing.syllable_count(x) for x in phones]
    if len(count_list) > 0:
        result = max(count_list)
    else:
        result = 0
    return result

# This function takes a single input:
# word - a string representing a word
# The function returns a list of words that rhyme with
# the input word.
def get_rhymes(word):
    result = pronouncing.rhymes(word)
    return result

# This function takes a single input:
# word - a string representing a word
# The function returns a list of strings. Each string in the list
# is a sequence of numbers. Each number corresponds to a syllable
# in the word and describes the stress placed on that syllable
# when the word is pronounced.
# A '1' indicates primary stress on the syllable
# A '2' indicates secondary stress on the syllable
# A '0' indicates the syllable is unstressed.
# Each element of the list indicates a different way to pronounce
# the input word.
def get_stresses(word):
    result = pronouncing.stresses_for_word(word)
    return result

# Use this function to generate each line of your poem.
# This is where you will implement the rules that govern
# the construction of each line.
# For example:
#     -number of words or syllables in line
#     -stress pattern for line (meter)
#     -last word choice constrained by rhyming pattern
# Add any parameters to this function you need to bring in
# information about how a particular line should be constructed.
def generate_line(minimum_word, max_words = 15, min_ratio = 0.8, max_ratio = 1.2):
    line = []
    previous = None
    num_words = 0
    num_syllables = 0
    prev_syllables_num = 0
    new_word = ""
    ratio = 0                         
    while len(line) < minimum_word:
        new_word = random_word_generator(previous, 3)[1]
        previous = new_word
        num_words += 1
        prev_syllables_num = count_syllables(new_word)
        num_syllables += prev_syllables_num
        line.append(new_word)
        ratio = num_syllables / num_words
        #print("Current word:", new_word)
        #print("Current words in line:", line)
        #print("Number of words:", num_words)
        #print("Current number of syllables for current word:", prev_syllables_num)
        #print("Total number of syllables:", num_syllables)
        #print("Ratio (#of syllable/#of words)", ratio)

    if ratio >= max_ratio or ratio <= min_ratio:
        final = " ".join(line)
    else:
        while ratio < max_ratio or ratio > min_ratio:
            new_word = random_word_generator(previous, 3)[1]
            previous = new_word
            num_words += 1
            prev_syllables_num = count_syllables(new_word)
            num_syllables += prev_syllables_num
            line.append(new_word)
            ratio = num_syllables / num_words
            #print("Current word:", new_word)
            #print("Current words in line:", line)
            #print("Number of words:", num_words)
            #print("Current number of syllables for current word:", prev_syllables_num)
            #print("Total number of syllables:", num_syllables)
            #print("Ratio (#of syllable/#of words)", ratio)
            if num_words == max_words:
                break
        final = " ".join(line)
    return final

# Use this function to construct your poem, line by line.
# This is where you will implement the rules that govern
# the structure of your poem.
# For example:
#     -The total number of lines
#     -How the lines relate to each other (rhyming, syllable counts, etc)
def generate_poem():
    lines = []
    lines.append("")
    lines.append(generate_line(10, 20))
    lines.append(generate_line(10, 20))
    lines.append(generate_line(10, 20))
    lines.append(generate_line(10, 20))
    lines.append("")
    lines.append(generate_line(10, 20, 0.85, 1.15))
    lines.append(generate_line(10, 20, 0.9, 1.1))
    lines.append(generate_line(10, 20, 0.85, 1.15))
    lines.append(generate_line(10, 20, 0.9, 1.1))
    poem = "\n".join(lines)
    return poem

def test():
    keep_going = True
    while keep_going:
        word = input("Please enter a word (Enter '0' to quit): ")
        if word == '0':
            keep_going = False
        elif word == "":
            pass
        else:
            print(cfd[word].keys(), cfd[word].values())
            print()
            print("Random 5 words following", word)
            print(random_word_generator(word, 5))
            print()
            print("Pronunciations of", word)
            print(pronouncing.phones_for_word(word))
            print()
            print("Syllables in", word)
            print(count_syllables(word))
            print()
            print("Rhymes for", word)
            print(get_rhymes(word))
            print()
            print("Stresses for", word)
            print(get_stresses(word))
            print()

if __name__ == "__main__":
    #test 1
    my_poem = generate_poem()
    print(my_poem)
