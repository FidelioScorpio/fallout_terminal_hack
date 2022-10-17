#!/usr/local/bin/python3
import enchant

# printDebug - only prints if the DEBUG flag is true
# inputWordsFromFile - reads in words from the file - one word per line; ignores all blank lines and lines starting with '#'; ignores all characters after the first whitespace in a line (allowing inline comments)
# verifyWordList - performs checks on the words  - including length, dictionary correctness, and the existance of any duplicates
# formatWords - formats a list of words/wordIndices with index numbers and commas
# compareWords - returns the number of matching characters in two words
# getPartialWordChoiceScore - given a word-choice and a correct-word, calculates and returns how many words would be eliminated (partial score of the word-choice)
# getWordChoiceScore - given a word-choice, uses ^ to calculate and return how many words would be eliminated with each other word being correct (score of the word-choice)
# getBestWordChoice - uses ^ to calcuate and return which word-choice is the best selection - i.e. choose the word that would narrow the remaining choices the most
# reduceWordList - uses user-input to reduce the set of words by those eliminated by the new information; returns the new word list and if the puzzle is solved
# main - inputs and verifies initial word list; manages prints and calculations in the main loop

DEBUG = False
DEBUG_CALC_DICT = True
en_US = enchant.Dict("en_US")

# Only prints if the DEBUG flag is true
def printDebug(s):
    if DEBUG:
        print("DEBUG: {}".format(s))

# Reads in words from the file - one word per line; ignores all blank lines and lines starting with '#'; ignores all characters after the first whitespace in a line (allowing inline comments)
def inputWordsFromFile():
    words = []
    with open("_fallout_terminal_hack_list.txt", "r") as f:
        wordlen = 0
        for line in f:
            l = line.strip().upper()
            if len(l) == 0 or l[0] == "#":
                continue
            separated = l.split(maxsplit=1)
            if len(separated) > 1:
                # Assume that any space separation is a comment and just take the first portion
                l = separated[0]
            if wordlen > 0 and len(l) != wordlen:
                print("Warning in wordlist - not all words are the same length - ignoring different length words")
                continue
            if wordlen == 0:
                wordlen = len(l)
            words.append(l)
    return words

# Performs checks on the words  - including length, dictionary correctness, and the existance of any duplicates
def verifyWordlist(words):
    # 1. Check against dictionary for typos
    # 2. Check for dupes
    # 3. Show count
    unique_words = []
    dupes = []
    for i in range(len(words)):
        w = words[i]
        if not en_US.check(w):
            s = en_US.suggest(w)
            print("'{}' is not in the dictionary, suggestions: {}".format(w, s))

        dupe = False
        for uw in unique_words:
            if w == uw:
                dupes.append(i)
                dupe = True
        if not dupe:
            unique_words.append(w)
    if len(dupes) > 0:
        ds = formatWords(dupes, words)
        print("There are duplicates: {}\nRemove dupes?".format(ds))
        res = input().upper()
        if res[0] == "Y":
            new_words = []
            for i in range(len(words)):
                if i not in dupes:
                    new_words.append(words[i])
            words = new_words
    print("There are {} words to choose from and the length of the words is {}\n".format(len(words), len(words[0])))
    return words

# Formats a list of words/wordIndices with index numbers and commas
def formatWords(w, words, alternateIndexer = None):
    words_string = ""
    for word in w:
        ai_text = None
        if type(word) == int:
            sword = words[word]
            iword = word
        if type(word) == str:
            sword = word
            iword = words.index(word)
        if alternateIndexer is not None:
            ai_text = "({})".format(alternateIndexer.index(sword))
        if words_string != "": words_string += ", "
        words_string += "{}{} {}".format(iword, ai_text if ai_text is not None else "", sword)
    return words_string

# Returns the number of matching characters in two words
def compareWords(a, b):
    counter = 0
    for letter in range(len(a)):
        if a[letter] == b[letter]: counter += 1
    printDebug("comparing {} to {}, count is {}".format(a, b, counter))
    return counter

# Given a word-choice and a correct-word, calculates and returns how many words would be eliminated (partial score of the word-choice)
def getPartialWordChoiceScore(selectedCorrectWord, selectedChoiceWord, words):
    if selectedCorrectWord == selectedChoiceWord:
        return 0
    words_eliminated = 0
    target = compareWords(words[selectedCorrectWord], words[selectedChoiceWord])
    for i in range(len(words)):
        if i == selectedCorrectWord or i == selectedChoiceWord:
            continue
        comp = compareWords(words[i], words[selectedChoiceWord])
        if comp != target:
            words_eliminated += 1
    printDebug("If {} is correct and {} is chosen, {} words are eliminated".format(words[selectedCorrectWord], words[selectedChoiceWord], words_eliminated))
    return words_eliminated

# Given a word-choice, uses getPartialWordChoiceScore to calculate and return how many words would be eliminated with each other word being correct (score of the word-choice)
def getWordChoiceScore(selectedChoiceWord, words):
    score = 0
    for i in range(len(words)):
        if i != selectedChoiceWord:
            score += getPartialWordChoiceScore(i, selectedChoiceWord, words)
    printDebug("{} has a score of {}".format(words[selectedChoiceWord], score))
    return score

# Uses getWordChoiceScore to calcuate and return which word-choice is the best selection - i.e. choose the word that would narrow the remaining choices the most
def getBestWordChoice(words):
    bestWords = []
    bestScore = 0
    for i in range(len(words)):
        score = getWordChoiceScore(i, words)
        if score == bestScore:
            bestWords.append(i)
        elif score > bestScore:
            bestScore = score
            bestWords = [i]
    return (bestWords, bestScore)

# Uses user-input to reduce the set of words by those eliminated by the new information; returns the new word list and if the puzzle is solved
def reduceWordlist(words):
    # Get the word that was tried
    tried_word = None
    num_matches = -1
    while tried_word == None and num_matches == -1:
        print("Input the word that was tried (string or index)")
        while tried_word == None:
            user_input = input().lower()
            print("I SAW '{}'".format(user_input), end=" ")
            if user_input == "" or user_input == "empty string":
                continue
            # do the error checking
            # i.e. if is number, is it 0<=i<len(words)
            #      if is string, is it in words
            number = -1
            try:
                number = int(user_input)
                if number < 0 or number >= len(words):
                    number = -1
                    print("index must be between 0 and " + str(len(words) - 1))
                    continue
            except ValueError:
                number = -1
            if number != -1:
                tried_word = number
                print("I UNDERSTOOD '" + words[number] + "'")
            else:
                # parse as a string
                if user_input in words:
                    tried_word = words.index(user_input)
                else:
                    print("That was not in the list of words")
    
        # Get the number of matches stated
        print("Input the number of letter matches that word had, empty string to reset")
        while num_matches == -1:
            user_input = input().lower()
            print("I SAW '{}'".format(user_input), end=" ")
            if user_input == "" or user_input == "empty string":
                tried_word = None
                break # fall back to the outer loop to re-get a tried_word
            #do the error checking
            #i.e. is it a number and is it 0<=i<len(words[0])
            number = -1
            try:
                number = int(user_input)
                if number < 0 or number > len(words[0]):
                    number = -1
            except ValueError:
                number = -1
            if number == -1:
                # Allow use of 'all', 'done', 'ok'
                if user_input == "all" or user_input == "done" or user_input == "ok":
                    number = len(words[0])
                else:
                    print("That doesn't make sense. There are " + str(len(words[0])) + " letters in the words. try again")
                    continue
            num_matches = number

    # Create a list of remaining words
    if num_matches == len(words[tried_word]):
        print("\nSolved!\n")
        return ([], True)
    new_words = []
    for w in words:
        # if w shares exactly num_matches characters with tried_word, append to new_words
        if compareWords(words[tried_word], w) == num_matches:
            new_words.append(w)

    return (new_words, False)


# Inputs and verifies initial word list; manages prints and calculations in the main loop
def main():
    words = inputWordsFromFile()

    if len(words) == 0:
        print("Input words into the file called '_fallout_terminal_hack_list.txt'")
        return

    words = verifyWordlist(words)

    words_original = words.copy()

    solved = False
    while not solved:    
        # print("Available words are [{}]".format(formatWords(words, words)))
        selection = getBestWordChoice(words)
        printDebug("selection is {}".format(selection))

        text = "s are"
        if len(selection[0]) == 1:
            text = " is"
        print("\nSuggested option{} [{}]".format(text, formatWords(selection[0], words, words_original)))

        if DEBUG_CALC_DICT:
            print("\nDEBUG_CALC_DICT (<WORD>: {<NUM_LETTERS> : <NUM_MATCHES>})")
            for word1 in words:
                inner_dic = dict()
                for word2 in words:
                    if word2 == word1: continue
                    count = compareWords(word1, word2)
                    if count in inner_dic:
                        inner_dic[count] += 1
                    else:
                        inner_dic[count] = 1
                print("{}: {}".format(word1, inner_dic))

        print("\nThe word list is: [ {} ]".format(formatWords(words, words, words_original)))
        words, solved = reduceWordlist(words)
        if not solved and len(words) == 0:
            print("ERROR: There are no possible words left")

if __name__ == "__main__":
    main()

