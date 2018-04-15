from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def areUniqueFirstNames(arg1, arg2):
    """
    Check if the arguments represent different first names. The arguments represent the same first name
    if one of them is a nickname of the other. Ignores typos.
    :param arg1: a first name
    :param arg2: another first name
    :return: True if the arguments represent different first names
    """

    # Open the nicknames DB
    with open("nicknames.csv", "r") as nicknamesFile:
        # Store all the nicknames which the arguments appear in
        arg1MatchingNicknames = []
        arg2MatchingNicknames = []

        # Read the nickname file line by line
        allTheNicknamesList = nicknamesFile.read().split("\n")
        for nicknamesString in allTheNicknamesList:
            nicknamesList = nicknamesString.split(",")

            # First argument
            fuzzyMatchingScores = process.extract(arg1, nicknamesList, scorer=fuzz.ratio)
            if fuzzyMatchingScores[0][1] > int((1 - 1.0/len(arg1))*100):
                arg1MatchingNicknames.append(nicknamesList)

            # Second argument
            fuzzyMatchingScores = process.extract(arg2, nicknamesList, scorer=fuzz.ratio)
            if fuzzyMatchingScores[0][1] > int((1 - 1.0/len(arg2))*100):
                arg2MatchingNicknames.append(nicknamesList)

    # If the arguments appear in the same nickname 'Family' they aren't unique
    for i in arg1MatchingNicknames:
        if i in arg2MatchingNicknames:
            return False
    return True


def areUniqueMiddleNames(arg1, arg2):
    """
    Check if the arguments represent different middle names. The arguments represent different middle names
    if both of the middle names exists and they aren't close on the keyboard.
    :param arg1: a middle name
    :param arg2: another middle name
    :return: True if the middle names are different
    """
    if arg1 == "" or arg2 == "" or arg1 == arg2:
        return False
    return not isCloseOnKeyboard(arg1, arg2)


def isCloseOnKeyboard(key1, key2):
    """
    Checks if two keys are close on the keyboard.
    Assuming the keyboard has a QWERTY layout and the keys are letters.
    :param key1: a key
    :param key2: another key
    :return: true if the keys are close to each other
    """
    mapOfTheKeyboard = {
        'a': ['q', 'w', 's', 'x', 'z'],
        'b': ['n', 'h', 'g', 'f', 'v'],
        'c': ['v', 'f', 'd', 's', 'x'],
        'd': ['w', 'e', 'r', 'f', 'v', 'c', 'x', 's'],
        'e': ['w', 's', 'd', 'f', 'r'],
        'f': ['r', 't', 'g', 'v', 'c', 'd', 'e'],
        'g': ['t', 'y', 'h', 'n', 'b', 'v', 'f', 'r'],
        'h': ['y', 'u', 'j', 'm', 'n', 'b', 'g', 't'],
        'i': ['u', 'j', 'k', 'l', 'o'],
        'j': ['y', 'u', 'i', 'k', 'm', 'n', 'h'],
        'k': ['u', 'i', 'o', 'l', 'm', 'j'],
        'l': ['i', 'o', 'p', 'k'],
        'm': ['n', 'h', 'j', 'k'],
        'n': ['b', 'g', 'h', 'j', 'm'],
        'o': ['i', 'k', 'l', 'p'],
        'p': ['o', 'l'],
        'q': ['a', 's', 'w'],
        'r': ['e', 'd', 'f', 'g', 't'],
        's': ['q', 'w', 'e', 'd', 'c', 'x', 'z', 'a'],
        't': ['r', 'f', 'g', 'h', 'y'],
        'u': ['y', 'h', 'j', 'k', 'i'],
        'v': ['c', 'd', 'f', 'g', 'b'],
        'w': ['q', 'a', 's', 'd', 'e'],
        'x': ['z', 'a', 's', 'd', 'c'],
        'y': ['t', 'g', 'h', 'j', 'u'],
        'z': ['a', 's', 'x']
    }

    return key2 in mapOfTheKeyboard[key1]


def areUniqueLastNames(arg1, arg2):
    """
    Check if the arguments represent different last names. The arguments must be the same. Ignores typos.
    :param arg1: a last name
    :param arg2: another last name
    :return: True if the arguments represent different last names
    """
    return fuzz.ratio(arg1, arg2) < int((1 - 1.0/len(arg1))*100)


def areUniqueNames(firstName1, middleName1, lastName1, firstName2, middleName2, lastName2):
    """
    Check if the arguments represent different people. One unique part of the name is enough to make the whole name unique.
    :param firstName1: first name of the first person
    :param middleName1: middle name of the first person
    :param lastName1: last name of the first person
    :param firstName2: first name of the second person
    :param middleName2: middle name of the first person
    :param lastName2: last name of the second person
    :return: True if the arguments represent different people.
    """
    return areUniqueFirstNames(firstName1, firstName2) or areUniqueMiddleNames(middleName1, middleName2) or areUniqueLastNames(lastName1, lastName2)


def countUniqueNames(billFirstName, billLastName, shipFirstName, shipLastName, billNameOnCard):
    """
    Count the number of unique names in a transaction.
    :param billFirstName: first name on the billing address
    :param billLastName: last name on the billing address
    :param shipFirstName: first name on the shipping address
    :param shipLastName: last name on the shipping address
    :param billNameOnCard: full name on the credit card
    :return: the number of different names
    """
    uniqueNameCounter = 0

    # Validate the arguments
    if billFirstName == "" or billFirstName.count(" ") > 1:
        print "The billing first name isn't valid"
        return
    if billLastName == "" or billLastName.count(" ") > 0:
        print "The billing last name isn't valid"
        return
    if shipFirstName == "" or shipFirstName.count(" ") > 1:
        print "The shipping first name isn't valid"
        return
    if shipLastName == "" or shipLastName.count(" ") > 0:
        print "The shipping last name isn't valid"
        return
    if billNameOnCard == "" or billNameOnCard.count(" ") > 2 or billNameOnCard.count(" ") < 1:
        print "The name on the credit card isn't valid"
        return

    # If there is a middle name then separate the first and middle names from each other
    billMiddleName = ""
    shipMiddleName = ""
    if " " in billFirstName:
        billMiddleName = billFirstName.split()[1]
        billFirstName = billFirstName.split()[0]
    if " " in shipFirstName:
        shipMiddleName = shipFirstName.split()[1]
        shipFirstName = shipFirstName.split()[0]

    # Lower all the arguments
    billFirstName = billFirstName.lower()
    billMiddleName = billMiddleName.lower()
    billLastName = billLastName.lower()
    shipFirstName = shipFirstName.lower()
    shipMiddleName = shipMiddleName.lower()
    shipLastName = shipLastName.lower()
    billNameOnCard = billNameOnCard.lower()

    # split name on card
    nameOnCardList = billNameOnCard.split(" ")

    # Check if the billing and shipping names are unique
    if areUniqueNames(billFirstName, billMiddleName, billLastName, shipFirstName, shipMiddleName, shipLastName):
        uniqueNameCounter += 1
    # If the name on the credit card has a middle name it must be in a
    if billNameOnCard.count(" ") == 2:
        # Check if the order of the names is "<F> <M> <L>" or "<L> <F> <M>"
        if len(nameOnCardList[1]) == 1:
            cardFirstName = nameOnCardList[0]
            cardMiddleName = nameOnCardList[1]
            cardLastName = nameOnCardList[2]
        else:
            cardLastName = nameOnCardList[0]
            cardFirstName = nameOnCardList[1]
            cardMiddleName = nameOnCardList[2]

        # Check if the billing name and the name on the credit card are unique
        if areUniqueNames(billFirstName, billMiddleName, billLastName, cardFirstName, cardMiddleName, cardLastName):
            uniqueNameCounter += 1
        # Check if the shipping name and the name on the credit card are unique
        if areUniqueNames(cardFirstName, cardMiddleName, cardLastName, shipFirstName, shipMiddleName, shipLastName):
            uniqueNameCounter += 1
    else:
        # Try first assuming the name on the credit card is "<F> <L>"
        cardFirstName = nameOnCardList[0]
        cardLastName = nameOnCardList[1]
        cardAndBill1 = areUniqueNames(billFirstName, billMiddleName, billLastName, cardFirstName, "", cardLastName)
        cardAndShip1 = areUniqueNames(cardFirstName, "", cardLastName, shipFirstName, shipMiddleName, shipLastName)

        # Try also when the name on the credit card is "<L> <F>"
        cardFirstName = nameOnCardList[1]
        cardLastName = nameOnCardList[0]
        cardAndBill2 = areUniqueNames(billFirstName, billMiddleName, billLastName, cardFirstName, "", cardLastName)
        cardAndShip2 = areUniqueNames(cardFirstName, "", cardLastName, shipFirstName, shipMiddleName, shipLastName)

        # If both of the options are unique than add one to the counter
        if cardAndBill1 and cardAndBill2:
            uniqueNameCounter += 1
        if cardAndShip1 and cardAndShip2:
            uniqueNameCounter += 1

    # There is always at least one name
    if uniqueNameCounter == 0:
        uniqueNameCounter += 1

    return uniqueNameCounter


def testUnit():
    """
    Test several possible cases.
    """
    print "1. 1=", countUniqueNames("Deborah", "Egli", "Deborah", "Egli", "Deborah Egli")
    print "2. 1=", countUniqueNames("Deborah", "Egli", "Debbie", "Egli", "Debbie Egli")
    print "3. 1=", countUniqueNames("Deborah", "Egni", "Deborah", "Egli", "Deborah Egli")
    print "4. 1=", countUniqueNames("Deborah S", "Egli", "Deborah", "Egli", "Egli Deborah")
    print "5. 1=", countUniqueNames("Deborah", "Egli", "Deborah S", "Egli", "Deborah S Egli")
    print "6. 2=", countUniqueNames("Michelle", "Egli", "Deborah", "Egli", "Michelle Egli")
    print "7. 2=", countUniqueNames("bbborah", "Egli", "Deborah", "Egli", "Deborah Egli")
    print "8. 2=", countUniqueNames("Dan", "Oboud", "Oboud", "Dan", "Oboud Dan")
    print "9. 3=", countUniqueNames("abe", "dan", "shelly", "ray", "ray beck")
    print "10.",
    countUniqueNames("a", "b", "c", "d", "e")

if __name__ == "__main__":
    testUnit()
