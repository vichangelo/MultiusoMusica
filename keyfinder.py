# python 3.7.1
"""Application to find the key of music based on its chords.

Utilizes a base module containing essential classes and functions (see its
documentation for further detail), then interfaces them with the user in order
to perform the required action.
"""


import base


def compare(chord_notes, scale_keys, percentage=False):
    """Compares the notes of a chord with keys on a given scale.

    Iterates the scale, then the keys, then compares the notes in the keys
    with the notes in the chord(s). If the parameter percentage is True then
    the function also returns the probability of the match in percentage.

    Args:
        chord_notes (list): notes of the chord(s) to be analyzed
        scale_keys (dict): notes of the keys of a given scale to be analyzed
        percentage (bool): optional, determines whether percentage is returned
    Returns:
        matches (dict): number of matches per key
        results (dict): notes shared between chord and key
    """
    scale = list(scale_keys.values())
    matches = {}
    results = {}
    i = 0

    for key in scale:
        matches[key[0]] = i
        results[key[0]] = []
        i += 1
        for note in key:
            for chord_note in chord_notes:
                if note == chord_note:
                    matches[key[0]] = i
                    results[key[0]].append(note)
                    i += 1
        i = 0

    if percentage:
        scale_length = len(scale[0])
        for match in matches:
            a = matches[match] / scale_length
            b = round(a * 100)
            if b > 100:
                b = 100
            matches[match] = str(b) + "%"

    return matches


# Instanciando escala diatônica maior, utilizando estrutura padrão.
dia_maior = base.Scale("diatonica maior")
tons_maior = dia_maior.apply()

chords_input = str(input("Acordes: ")).split()
chords = []
notes = []
i = 0
for chord in chords_input:
    chords.append(base.Chord(chord))
    chords[i].decompose_chord()
    notes.extend(chords[i].notes)
    i += 1

# print(__doc__)
print(notes)
print(compare(notes, tons_maior, True))
