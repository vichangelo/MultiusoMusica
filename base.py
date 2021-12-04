"""Base module containing essential variables and functions.

Vars:
    notes (list): The 12 notes of the chromatic scale.
    degrees_dict (dict): Pairs degrees of the chromatic scale, written in
        roman numerals and their corresponding semitone number.
    chords_dict (dict): Pairs chord symbols with their corresponding semitone
        number from the tonic.

Functions:
    check_accident: Checks if a symbol in a chord string is sharp or flat.
    return_degree: Returns the second note of an interval.
"""


notes = ["C", "C#", "D", "Eb", "E", "F",
         "F#", "G", "G#", "A", "Bb", "B"]
degrees_dict = {"I": 0, "ii": 1, "II": 2, "iii": 3, "III": 4,
                "IV": 5, "v": 6, "V": 7, "vi": 8, "VI": 9,
                "vii": 10, "VII": 11}
chords_dict = {"2": 2, "9": 2, "m": 3, "4": 5, "11": 5,
               "5-": 6, "º": 6, "dim": 6, "5": 7, "5+": 8,
               "6": 9, "13": 9, "7": 10, "7M": 11}


def check_accident(chord_string, symbol):
    """Checks if a symbol in a chord string is sharp or flat.

    Uses a chord string and a symbol string and, if the chord string is more
    than just the root and contains the symbol, declares two types of
    accidents. It then assigns to them an index through which the accident
    symbol may be found in the chord string. Finally, checks if the characters
    in these indexes are indeed the accidents and returns an integer equivalent
    to the number of semitones the accident means.

    Args:
        chord_string (str): string of the chord. i.e: "Dm7(b9)"
        symbol (str): string of the symbol. i.e: "9"

    Vars:
        accident1 (int): index for checking an accident of the "b/#" type
        accident2 (int): index for checking an accident of the "-/+" type
    """
    if symbol in chord_string and len(chord_string) > 2:
        accident1 = chord_string.index(symbol[0]) - 1
        accident2 = chord_string.index(symbol[0]) + 1
        if len(symbol) > 2:
            accident2 += 1

        # If the chord ends with the symbol, then it can't be the second type.
        if chord_string.endswith(symbol):
            accident2 = accident1

        if chord_string[accident1] == "b" or chord_string[accident2] == "-":
            return -1
        elif chord_string[accident1] == "#" or chord_string[accident2] == "+":
            return 1
        else:
            return 0
    else:
        return 0


def return_degree(tonic, degree):
    """Returns the second note of an interval.

    Given a tonic and a degree, this function will assign the tonic
    to its index in the list of notes and then sum it with the number
    of semitones associated with the degree in its dictionary. Then,
    return a note from the aforementioned list with the new index.

    Args:
        tonic (str): note from the chromatic scale
        degree (str): degree between unison ("I") and major seventh
        ("VII"), minor and diminisheds are written in lowercase.
    """
    tonic = notes.index(tonic)
    tonic += degrees_dict[degree]

    if tonic > 11:
        tonic = tonic - 12
    return notes[tonic]
