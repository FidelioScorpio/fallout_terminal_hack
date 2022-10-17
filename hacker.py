global_words = ["lighting", "gathered", "succeeds", "rightful", "boneyard", "maintain", "generate", "randomly"]

#Ctrl+Alt+P to run in N++ (created)

#succeeds = 0
#gathered = 1
#rightful = 4
#lighting = answer
#boneyard = 0
#maintain = 1
#generate = 0
#randomly = 0
##
#loyalist 1
#feverish 0
#citizens 0
#resulted 3
#supplied 2
#suddenly 0
#unwanted 8 ANS
#humanity 2
#conquest 0
#reptiles 1
#servants 0

#companions
#wastelords 8 ANS
#calculated
#scientific
#inspection
#throughout
#explosions 1
#sculptures 2
#television
#contenting 2
#recognizes
#knighthood

DEBUG = True

def printDebug(s):
    if DEBUG:
        print("DEBUG: {}".format(s))

def GetPrettyPrintWords(words):
    string = ""
    for i in range(len(words)):
        string += str(i) + " " + words[i] + ", "
    if len(string) > 2:
        return "[" + string[:-2] + "]"
    else:
        return "[]"

# Input words into words list
def ReceiveWords():
    global global_words
    #must check that all words are the same length
    print("Enter words (case ignored). Enter empty string when done. '<undo>' to remove previous word")
    new_word_list = []
    word_length = 0
    user_input = "x"
    while True:
        user_input = input().lower()
        print("I SAW '" + user_input + "'")
        if len(new_word_list) == 0:
            word_length = len(user_input)
        elif user_input == "" or user_input == "empty string":
            break
        elif user_input == "<undo>":
            new_word_list.pop()
            continue
        elif len(user_input) != word_length:
            print("Error. That was a different length. Length should be " + str(word_length))
            continue
        new_word_list.append(user_input)
    printDebug("word list is set to")
    printDebug(new_word_list)
    global_words = new_word_list
    return new_word_list


# find a word suggestion
def GetInitialChoice(words):
    dic = dict()
    word_length = len(words[0])
    for word1 in words:
        inner_dic = dict()
        for word2 in words:
            if word2 == word1: continue
            count = 0
            for i in range(word_length):
                if word1[i] == word2[i]:
                    count += 1
            printDebug(word1 + " matches " + word2 + " with " + str(count) + " letters")
            #if count == 0: continue
            #inner_dic[word2] = count
            if count in inner_dic:
                inner_dic[count].append(word2)
            else:
                inner_dic[count] = [word2]
        dic[word1] = inner_dic
    printDebug(dic)
    return dic

def GiveChoice(dic):

    maxi = 0
    choice = []
    for word in dic:
        if len(dic[word]) > maxi:
            maxi = len(dic[word])
            choice = [word]
        elif len(dic[word]) == maxi:
            choice.append(word)
        printDebug(word + " reveals data on " + str(len(dic[word])) + " options")


    string = "You should choose "
    for word in choice:
        string += word + " or "
    string = string[:-4] + " (reveals data on "
    string += str(maxi) + " option group"
    if maxi != 1:
        string += "s"
    string += ")"
    print(string)
    

# receive a result
def GetReduceData(words):
    # get the user to input the word they tried & the number of matches
    print("the word list: " + GetPrettyPrintWords(words))
    print("input the word that was tried (string or index), empty string to reset")
    tried_word = ""
    num_matches = -1
    #do the get word
    while tried_word == "":
        user_input = input().lower()
        print("I SAW '" + user_input + "'")
        if user_input == "" or user_input == "empty string": return GetReduceData(words)
        #do the error checking
        #i.e. if is number, is it 0<=i<len(words)
        #     if is string, is it in words
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
            tried_word = words[number]
            print("I UNDERSTOOD '" + tried_word + "'")
        else:
            # parse as a string
            if user_input in words:
                tried_word = user_input
            else:
                print("that was not in the list of words")
        

    #do the get num
    print("input the number of letter matches that word had, empty string to reset")
    while num_matches == -1:
        user_input = input().lower()
        print("I SAW '" + user_input + "'")
        if user_input == "" or user_input == "empty string": return GetReduceData(words)
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
    # now do the clever removal of words that match that don't match that num matches
    return (tried_word, num_matches)

def UseDicToRemoveWords(dic, word, matches):
    new_words = dic[word][matches]
    kept_words = None

    new_dic = dic.remove(word)
    

def Play(lastList = False):
    if lastList:
        words = global_words
    else:
        words = ReceiveWords()
    dic = GetInitialChoice(words)

    solved = False
    while not solved:
        GiveChoice(dic)
        word, matches = GetReduceData(words)
        if matches == len(words[0]):
            print("YOU DID IT!")
            solved = True
        else:
            
            dic = GetInitialChoice(dic[word][matches])
            words = list(dic.keys())

while True:
    Play()
