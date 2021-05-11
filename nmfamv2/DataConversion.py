import sys


def listFromListString(listAsString, typeOfData):
    if not isinstance(listAsString, str):
        print("Error: listAsString is not of type string")
        sys.exit()
    if listAsString[0] != "[":
        print("Error: first char in listAsString is not '['")
        sys.exit()
    if listAsString[len(listAsString) - 1] != "]":
        print("Error: last char in listAsString is not ']'")
        sys.exit()
    newList = listAsString[1:len(listAsString) - 1].split(",")
    if typeOfData == float:
        return list(map(lambda x: float(x), newList))


def test():
    dataFromString = listFromListString("[1.32,2.2,3.03,4.02,5.01]", float)
    print(dataFromString)
    for item in dataFromString:
        if not isinstance(item, float):
            print("Error: element is not of type float")
            sys.exit()
