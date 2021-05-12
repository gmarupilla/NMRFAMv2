import sys

bmseTranslator = {
    "(+-)-Acetylcarnitine": "bmse000142",
    "Benzoate": "bmse000300",
    "Citrate": "bmse000076",
    "DSS": "bmse000795",
    "Ethanol": "bmse000297",
    "Formate": "bmse000203",
    "Fumaric-acid": "bmse000083",
    "L-ornithine": "bmse000162",
    "Sarcosine": "bmse000160"
}

synonymTranslator = {
    "(+-)-acetylcarnitine": "(+-)-Acetylcarnitine",
    "dl-o-acetylcarnitine": "(+-)-Acetylcarnitine",
    "ammonium": "(+-)-Acetylcarnitine",
    "(3-carboxy-2-hydroxypropyl)trimethyl-": "(+-)-Acetylcarnitine",
    "hydroxide": "(+-)-Acetylcarnitine",
    "inner salt": "(+-)-Acetylcarnitine",
    "acetate": "(+-)-Acetylcarnitine",
    "acetyl-dl-carnitine": "(+-)-Acetylcarnitine",
    "1-propanaminium": "(+-)-Acetylcarnitine",
    "2-(acetoxy)-3-carboxy-n": "(+-)-Acetylcarnitine",
    "benzoate": "Benzoate",
    "kyselina benzoova": "Benzoate",
    "benzenemethanoic acid": "Benzoate",
    "benzoesaeure": "Benzoate",
    "solvo powder": "Benzoate",
    "benzoic acid": "Benzoate",
    "acide benzoique": "Benzoate",
    "retarder": "Benzoate",
    "citrate": "Citrate",
    "2-hydroxytricarballylic acid": "Citrate",
    "3-carboxy-3-hydroxypentane-1": "Citrate",
    "5-dioic acid": "Citrate",
    "1,2,3-propanetricarboxylic acid": "Citrate",
    "k-lyte": "Citrate",
    "anhydrous citric acid": "Citrate",
    "dss": "DSS",
    "sodium 3-(trimethylsilyl)-1-propanesulfonate": "DSS",
    "3-(trimethylsilyl)-1-propanesulfonic acid sodium salt": "DSS",
    "2,2-dimethyl-2-silapentane-5-sulfonate sodium salt": "DSS",
    "dss sodium salt": "DSS",
    "ethanol": "Ethanol",
    "etoh": "Ethanol",
    "sd alchol 23-hydrogen": "Ethanol",
    "ethyl hydrate": "Ethanol",
    "alcohol": "Ethanol",
    "denatured alcohol": "Ethanol",
    "ethyl alcohol and water": "Ethanol",
    "molasses alcohol": "Ethanol",
    "dehydrated ethanol": "Ethanol",
}


def check_dictionary_formats():
    synKeys = synonymTranslator.keys()
    for i in range(len(synKeys)):
        for j in synKeys[i]:
            if synKeys[i][j].isupper():
                print("Error: There is an uppercase in 'synonymTranslator' keys")
                sys.exit()
    keysFromBMSETranslator = bmseTranslator.keys()
    synValues = synonymTranslator.values()
    for i in range(len(synValues)):
        if not synValues[i] in keysFromBMSETranslator:
            print("Error: There is a value in 'synonymTranslator' that is not in the keys of 'bmseTranslator'")
            sys.exit()


def translate_to_gizzmo_name(synonymName):
    # checkDictionaryFormats()

    lowerSynonymName = synonymName.lower()

    return synonymTranslator[lowerSynonymName]


def translate_list_to_gizzmo_names(synonymNameList):
    # checkDictionaryFormats()
    gizzmoNames = []
    for synonymName in synonymNameList:
        lowerSynonymName = synonymName.lower()

        gizzmoNames.append(synonymTranslator[lowerSynonymName])

    return gizzmoNames


def translate_to_bmse(synonymName):
    check_dictionary_formats()

    gizzmo_name = translate_to_gizzmo_name(synonymName)
    if gizzmo_name is None:
        return None

    return bmseTranslator[gizzmo_name]
