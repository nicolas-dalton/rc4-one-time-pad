# Name: Nicolas Dalton
# Date: 9-24-2020
# Course: COSC 4343 Fall 2020 (Dr. Shebaro)
# Program Description: A python program that implements the RC4, an example of stream cipher
                    # and generalization of the One-time Pad


import string

#Function description: Converts a list of characters into a list of bytes
#precondition: Receives a list of characters
#postcondition: returns a list of bytes
def convertToBits(textList):
    bitList = []
    for i in textList:
        bitList.append(format(ord(i), '08b'))
    return bitList

#Function description: Converts a list of bytes into a list of characters
#precondition: Receives a list of bytes
#postcondition: returns a list of characters
def convertToString(bytesList):
    characterList = []
    for i in bytesList:
        characterList.append(chr(int(i, 2)))
    return characterList

#Function description: Performs an exclusive or on two bytes
#precondition: Receives two strings of bytes
#postcondition: returns a list of characters
def exclusiveOr(byteString1, byteString2):
    returnValue = ""
    for i in range(len(byteString1)):
        if byteString1[i] == byteString2[i]:
            returnValue+="0"
        if byteString1[i] != byteString2[i]:
            returnValue += "1"
    return returnValue

#Function description: Performs the One-Time Pad algorithim
#precondition: a message and a key, two strings, length of both strings must be the same size
#postcondition:  Returns a new encrypted or decrypted message
def oneTimePad(text, key):
    #Converts the text and key strings to list of bytes
    textList = list(text)
    textBytesList = convertToBits(textList)
    keyList = list(key)
    keyBytesList = convertToBits(keyList)
    newTextByteList = []
    #For each byte in order in both message and key list use exclusive or operation
    #Each byte must be converted to a String
    for i in range(len(textBytesList)):
        characterByteString = str(textBytesList[i])
        keyByteString = str(keyBytesList[i])
        byteString = exclusiveOr(characterByteString, keyByteString)
        decimalCharacter = int(byteString, 2)
        newTextByteList.append(format(decimalCharacter, '08b'))
    #Converts each byte in the new message list to its corresponding ASCII characters
    newTextList = convertToString(newTextByteList)
    newText = ""
    for i in range(len(newTextList)):
        newText += newTextList[i]
    return newText
#Function description: Performs the RC4 algorithim and uses one-time pad after
    #creating a key stream
#precondition: a message and a key, two strings, key must be short
#postcondition:  Returns a new encrypted or decrypted message
def rc4(text, key):
    #Phase 1: Initialization
    s = []
    k = []
    keyStreamList = []
    for i in range(256):
        s.append(i)
        k.append(key[i % len(key)])
    j = 0
    for i in range(256):
        j = (j+s[i]+ord(k[i]))% 256
        s[i],s[j] = s[j],s[i]
    i = j = 0
    # Phase 2: KeyStream Generator
    textLength = len(text)
    while textLength > 0:
        i = (i+1) % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]
        t = (s[i]+s[j]) % 256
        keyStreamList.append(s[t])
        textLength = textLength - 1
    #Phase 3: One-Time Pad
    keyStream = ""
    for i in keyStreamList:
        keyStream+= chr(i)
    cipherText = oneTimePad(text, keyStream)
    return cipherText

#Function description: Displays the menu of options
#precondition: nothing
#postcondition:  Displays the menu of options
def menu():
    option = 1
    while option != 3:
        option = int(input("Choose the following the options: \n 1 - One-Time Pad \n 2 - RC4 \n 3 - Exit : "))
        if option == 1:
            message = input("Enter a message you would like to encrypt/decrypt : ")
            key = input("Enter a key for the message (Key must be the same size as the message) : ")
            if len(message)!= len(key):
                print("Length of the key does not equal the length of the message!!!")
            if len(message) == len(key):
                encrypt = oneTimePad(message, key)
                print("Encrypted Message : "+ encrypt)
                decrypt = oneTimePad(encrypt, key)
                print("Decrypted Message : " + decrypt)
        elif option == 2:
            message = input("Enter a message you would like to encrypt/decrypt : ")
            key = input("Enter a short key for the message: ")
            encrypt = rc4(message, key)
            print("Encrypted Message : " + encrypt)
            decrypt = rc4(encrypt, key)
            print("Decrypted Message : " + decrypt)
        elif option > 3 or option < 1:
            print("That option is not available! Try again!")

menu()