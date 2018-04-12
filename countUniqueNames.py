from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# need to be updated according to the name length
MINIMUM_RATIO_TO_IGNORE_TYPO = 80


def areUniqueFirstNames(arg1, arg2):
    """
    Check if the arguments represent different first names. The arguments represent the same first name
    if they are the same or one of the is a nickname of the other. Ignores typos.
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
            if fuzzyMatchingScores[0][1] > MINIMUM_RATIO_TO_IGNORE_TYPO:
                arg1MatchingNicknames.append(nicknamesList)

            # Second argument
            fuzzyMatchingScores = process.extract(arg2, nicknamesList, scorer=fuzz.ratio)
            if fuzzyMatchingScores[0][1] > MINIMUM_RATIO_TO_IGNORE_TYPO:
                arg2MatchingNicknames.append(nicknamesList)
    # If the arguments appear in the same nickname 'Family' they aren't unique
    for i in arg1MatchingNicknames:
        if i in arg2MatchingNicknames:
            return False
    return True


def areUniqueMiddleNames(arg1, arg2):
    return False
    #return arg1 != arg2


def areUniqueLastNames(arg1, arg2):
    """
    Check if the arguments represent different last names. The arguments must be the same. Ignores typos.
    :param arg1: a last name
    :param arg2: another last name
    :return: True if the arguments represent different last names
    """
    return fuzz.ratio(arg1, arg2) < MINIMUM_RATIO_TO_IGNORE_TYPO


def areUniqueNames(firstName1, middleName1, lastName1, firstName2, middleName2, lastName2):
    """
    Check if the arguments represent different people.
    :param firstName1: first name of the first person
    :param middleName1: middle name of the first person
    :param lastName1: last name of the first person
    :param firstName2: first name of the second person
    :param middleName2: middle name of the first person
    :param lastName2: last name of the second person
    :return: True if the arguments represent different people.
    """
    return areUniqueFirstNames(firstName1, firstName2) or areUniqueMiddleNames(middleName1, middleName2) or areUniqueLastNames(lastName1, lastName2)


def normalize(x):
    return x.lower()


def countUniqueNames(billFirstName, billLastName, shipFirstName, shipLastName, billNameOnCard):
    # (TODO) Normalize all the arguments
    # (TODO) split name on card
    # (TODO) add support for middle name

    # print "areUniqueFirstNames:", areUniqueFirstNames(billFirstName.lower(), shipFirstName.lower())
    # print "areUniqueLastNames:", areUniqueLastNames(billLastName.lower(), shipLastName.lower())

    uniqueNameCounter = 1

    # Split billNameOnCard to first and last names
    cardLastName = billNameOnCard.split(" ")[-1]
    cardFirstName = ""
    for name in billNameOnCard.split(" "):
        if name != cardLastName:
            cardFirstName += name

    billMiddleName = ""
    shipMiddleName = ""
    cardMiddleName = ""

    # If there is a middle name than separate the first and middle names from each other
    if " " in billFirstName or "\t" in billFirstName:
        billMiddleName = billFirstName.split()[1]
        billFirstName = billFirstName.split()[0]
    if " " in shipFirstName or "\t" in shipFirstName:
        shipMiddleName = shipFirstName.split()[1]
        shipFirstName = shipFirstName.split()[0]
    if " " in cardFirstName or "\t" in cardFirstName:
        cardMiddleName = cardFirstName.split()[1]
        cardFirstName = cardFirstName.split()[0]

    if areUniqueNames(billFirstName, billMiddleName, billLastName, shipFirstName, shipMiddleName, shipLastName):
        uniqueNameCounter += 1
    return uniqueNameCounter


def main():
    print countUniqueNames("Ally", "Cohen", "Ally", "Cohen", "Ally Cohen")


def tester():
    countUniqueNames("Ally", "Cohen", "Ally", "Cohen", "Ally Cohen")

if __name__ == "__main__":
    main()
