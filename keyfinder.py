# -*- coding: latin-1 -*-
"""Module to find the key of a piece of music based on its chords.

Utilizes a base module containing essential classes and functions (see its
documentation for further detail), then interfaces them with the user in a
single function to perform the input and output.

Imports:
    baseclasses: contains the necessary Chord class and other functions

Functions:
    chords_input(): takes user input and turns in objects of the Chord class
    input_decompose(): decompose objects from Chord and returns their notes
                       in a list.
    compare(): takes notes in a list and compares them against notes of a scale
               in all keys to find the most probable one. If the optional
               argument is true, returns in percentage the most probable ones.
    matchformat(): uses a list of the matches with notes and percentages to
                   format it and print to the user.
    keyfind(): the titular function combines all the previous functions to
               receive input and present desired output to the user.
"""


import baseclasses


def chords_input():
    """Takes user input, turns in chord names and then in Chord objects."""
    chordinput = str(input("Acordes: ")).split()
    chords = []
    for chord in chordinput:
        chords.append(baseclasses.Chord(chord))

    return chords


def input_decompose(chords: list):
    """Takes a list of Chord objects and returns their notes in a list."""
    output = []
    for chord in chords:
        chord.decompose()
        for note in chord.notes:
            if note not in output:
                output.append(note)

    return output


def matchpercentage_calc(scalenotes: list, matches: dict):
    """Divides the number of matches by the number of notes in the scale."""
    scale_length = len(scalenotes[0])
    for match in matches:
        a = matches[match] / scale_length
        b = round(a * 100)
        if b > 100:
            b = 100
        if b < 0:
            b = 0
        matches[match] = b

    return matches


def compare(chord_notes, scale_keys, percentage=False):
    """Compares the notes of chords with keys's notes on a given scale.

    Iterates the scale, for each key setting the tonic in the dictionaries to
    be returned then comparing its notes with the chords' notes and updating
    the returns. In the percentage part, .

    Args:
        chord_notes (list): notes of the chords to be compared.
        scale_keys (dict): keys and notes of said keys of a given scale
                           to be compared.
        percentage (bool): optional, determines if percentage of combination
                           is returned.

    Vars:
        scale_values (list): list containing only the notes of scale_keys.
        i (int): counter

    Returns:
        matches (dict): keys and number of matches per key.
        results (dict): keys and notes shared between each of them and chords.
    """
    scale_values = list(scale_keys.values())
    matches = {}
    results = {}
    i = 0

    for key in scale_values:
        tonic = key[0]
        matches[tonic] = i
        results[tonic] = []
        i += 1
        for note in key:
            for chord_note in chord_notes:
                if note == chord_note:
                    matches[tonic] = i
                    results[tonic].append(note)
                    i += 1
        i = 0

    # For each note that isn't a match, probability of the key being correct
    # decreases.
    for note in chord_notes:
        for key in scale_values:
            tonic = key[0]
            if note not in key:
                matches[tonic] -= 1

    if percentage:
        return matchpercentage_calc(scale_values, matches)
    else:
        return results


def matchformat(matches: dict):
    """Formats the return of the compare() function to present it to the user.

    Turns 'matches' into tuple 'top3tup' containing its key:value pairs
    so a function can be made to sort it. Then creates and format strings
    so that the top 3 matches are displayed to the user.

    Functions:
        criteria(pairs): receive tuple top3tup and return only its integer.

    Vars:
        top3tup: tuple containing pairs of key:notes originally from 'matches'
                 but now easily sorted and obtained.
    """
    top3tup = list(matches.items())

    def criteria(pairs):
        value = pairs[1]
        return value
    top3tup.sort(reverse=True, key=criteria)

    if top3tup[0][1] == 100:
        tom = "O tom é {}.".format(top3tup[0][0])
        return print(tom)
    else:
        tons = ("Os tons mais prováveis são {} ({}%), "
                "{} ({}%) e {} ({}%).".format(top3tup[0][0], top3tup[0][1],
                                              top3tup[1][0], top3tup[1][1],
                                              top3tup[2][0], top3tup[2][1]))
        return print(tons)


def keyfind():
    """Declares major scale and executes whole script."""
    baseclasses.Scale("M", "I II III IV V VI VII")
    major_tones = baseclasses.Scale.apply("M")

    chords = chords_input()
    notes = input_decompose(chords)
    matches = compare(notes, major_tones, True)
    matchformat(matches)
    return
