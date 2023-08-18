'''
#how it works:
# https://www.youtube.com/watch?v=ASfAPOiq_eQ&t=1s
# youtube.com/watch?v=QwQVMqfoB2E

#The algorithm
input
If no roters, each letter comes out as itself
We create 4 roters, each with it's own scrambling
The user can decide how many roters and which roters to be used in a specific order
each roter to set with a value from 1-26
plugboard/mirror that connects one letter to another letter's path
'''

'''
Description
the roter moves by one. Once the first roter has moved 26 positions, the next
roter kicks in. After all roters have done their 26 rotations, the first roter 
can start again.

We still need to figure out the mirror issue

Roters
I	EKMFLGDQVZNTOWYHXUSPAIBRCJ	1930	Enigma I
II	AJDKSIRUXBLHWTMCQGZNPYFVOE	1930	Enigma I
III	BDFHJLCPRTXVZNYEIWGAKMUSQO	1930	Enigma I
IV	ESOVPZJAYQUIRHXLNFTGKDCMWB	December 1938	M3 Army
V	VZBRGITYUPSDNHLXAWMJQOFECK	December 1938	M3 Army
VI	JPGVOUMFYQBENHZRDKASXLICTW	1939	M3 & M4 Naval (FEB 1942)
VII	NZJHGRCXMYSWBOUFAIVLPEKQDT	1939	M3 & M4 Naval (FEB 1942)
VIII FKQHTLXOCBJSPDZRAMEWNIUYGV	1939	M3 & M4 Naval (FEB 1942)
'''

alphabet =  "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

rotor1 = list("EKMFLGDQVZNTOWYHXUSPAIBRCJ")
rotor2 = list("AJDKSIRUXBLHWTMCQGZNPYFVOE")
rotor3 = list("BDFHJLCPRTXVZNYEIWGAKMUSQO")
rotor4 = list("ESOVPZJAYQUIRHXLNFTGKDCMWB")
rotor5 = list("VZBRGITYUPSDNHLXAWMJQOFECK")
rotor6 = list("JPGVOUMFYQBENHZRDKASXLICTW")
rotor7 = list("NZJHGRCXMYSWBOUFAIVLPEKQDT")
rotor8 = list("FKQHTLXOCBJSPDZRAMEWNIUYGV")
reflector = list("YRUHQSLDPXNGOKMIEBFZCWVJAT")
plugBoard = {"H":"K", "K":"H", "C":"N", "N":"C", "O":"I", "I":"O", "F":"Y", "Y":"F", "J":"M", "M":"J", "W":"L", "L":"W"}
rotors = {1:rotor1, 2:rotor2, 3:rotor3, 4:rotor4, 5:rotor5, 6: rotor6, 7: rotor7, 8: rotor8}
rotorCounter = {1:0, 2:0, 3:0, 4:0, 5:0, 6: 0, 7: 0, 8: 0}

rotorsInUse = []

def get_rotors():
    global rotorsInUse, reflector, plugBoard
    message = input("Please enter your text: ").upper()
    choice = input("Enter e to encrypt or d to decrypt: ")
    selection = input("select you roters with a space between each number : 1 2 3 4 5 6 7 8")
    selection = selection.strip().split()
    for i in selection:
        if i.isdigit() and int(i) in [1,2,3,4,5,6,7,8]:
            rotorsInUse.append(int(i))
        else:
            print("invalid roter number", i)
    for rotor in rotorsInUse:
        position = int(input("Enter rotor position between 1-26 for roter"+ str(rotor)+ ":"))
        initRotor(rotor, position)
    plugChoice = input("For Plugboard Configuration; Enter 1 to set plugboard, or 2 for default plugboard: ")
    if plugChoice == "1":
        newPlugBoard = {}
        while True:
                new_pair = input("input a pair of letter seperate by space for a pair or 0 to exit: ").upper()
                if new_pair == "0":
                    break
                letters = new_pair.strip().split()
                newPlugBoard[letters[0]] = letters[1]
                newPlugBoard[letters[1]] = letters[0]

        plugBoard = newPlugBoard
    elif plugChoice == "2":
        print("Default value for plugboard has been selected")
    return(message, choice)



def initRotor(rotor, pos):
    for i in range(int(pos)):
        rotateRoter(rotor)


def rotateRoter(currentRoter):
    global rotors, rotorCounter
    if rotorCounter[currentRoter] < 26:
        rotor = rotors[currentRoter]
        lastItem = rotor.pop(0)
        rotor.append(lastItem)
        rotors[currentRoter] = rotor
        rotorCounter[currentRoter] += 1
    if rotorCounter[currentRoter] == 26:
        # print("Changing roter")
        rotorCounter[currentRoter] = 0
        currentRoter = getNextRotor(currentRoter)
    return currentRoter




def rotorEncrypt(message):
    global rotors, rotorCounter
    currentRoter = rotorsInUse[0]

    encryptedText = ""
    for letter in message:
        currentRoter = rotateRoter(currentRoter)
        newLetter = letter
        newLetter = plugBoardEncrypt(newLetter)

        print(newLetter, "Plugboard result")
        rotorName = rotorsInUse[0]
        rotorAlphabet = rotors[rotorName]
        lindex = rotorAlphabet.index(newLetter)
        if lindex == -1:
            continue
        else:
            for rotor in rotorsInUse:
                rotorAlphabet = rotors[rotor]
                newLetter = rotorAlphabet[lindex]
                print(lindex, newLetter, rotor, rotorAlphabet)

            newLetter = reflectorEncrypt(newLetter)

            print("reflectorValue", newLetter)
            newLetter = reverseRotorEncrypt(newLetter)
            print("reverseRoterValue", newLetter)
            newLetter = plugBoardEncrypt(newLetter)
            #print("reverseRotorValue", newLetter)
            #rotorName = rotorsInUse[0]
            #rotorAlphabet = rotors[rotorName]
            #lindex = rotorAlphabet.index(newLetter)
            #newLetter = alphabet[lindex]
            print("OutputLetter", newLetter, lindex)
            encryptedText += newLetter

    return encryptedText


def getNextRotor(rotorNumber):
    if rotorNumber in rotorsInUse:
        currentRotorPosition = rotorsInUse.index(rotorNumber)
        if currentRotorPosition == (len(rotorsInUse) - 1):
            newRotorNumber = rotorsInUse[0]
        else:
            newRotorNumber = rotorsInUse[currentRotorPosition + 1]
        return newRotorNumber
    else:
        print("Invalid roter number", rotorNumber, rotorsInUse)


def reflectorEncrypt(message):
    encryptedText = ""
    for letter in message:
        lindex = alphabet.index(letter)
        newLetter = reflector[lindex]
        encryptedText += newLetter
    return encryptedText

def plugBoardEncrypt(letter):
    if letter in plugBoard:
        return plugBoard[letter]
    else:
        return letter

def reverseRotorEncrypt(message):
    global rotors
    encryptedText = ""
    for letter in message:
        newLetter = letter
        reverseRotersInUse = rotorsInUse[:]
        reverseRotersInUse.reverse()
        indexGotten = False
        lindex = -1
        for rotorName in reverseRotersInUse:
            rotorAlphabet = rotors[rotorName]
            if not indexGotten:
                lindex = rotorAlphabet.index(letter)
                indexGotten = True

            newLetter = rotorAlphabet[lindex]
            print(lindex, newLetter, rotorName, rotorAlphabet)

        encryptedText += newLetter
    return encryptedText




if __name__ == '__main__':
    message, choice = get_rotors()
    if choice.lower() == "e":
        output = rotorEncrypt(message)
        print(output)






