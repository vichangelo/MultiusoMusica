"""Base module for multi-purpose musical python script.

Functions:
    check_accident(total, subj, octave=1): returns the equivalent semitones
    if the submitted note or interval is sharp or flat.
    return_degree(n, degree): returns the second note in an interval according
    to the tonic and the degree.

Classes:
    Scale: has the methods and attributes to instantiate a scale and apply it
    to the 12 keys of the chromatic scale.
    Chord: has the methods and attributes to instantiate a chord and decompose
    it, retrieving its notes.

Vars:
    notes (list): list containing the 12 notes of the chromatic scale
    degrees_dict (dict): dictionary containing all the degrees of the diatonic
    scale and their corresponding semitones
    chords_dict (dict): dictionary containing all the symbols used in chord
    names, and their corresponding semitones
"""

notes = ["C", "C#", "D", "Eb", "E", "F",
         "F#", "G", "G#", "A", "Bb", "B"]
degrees_dict = {"I": 0, "ii": 1, "II": 2, "iii": 3, "III": 4,
                "IV": 5, "v": 6, "V": 7, "vi": 8, "VI": 9,
                "vii": 10, "VII": 11}
chords_dict = {"2": 2, "9": 2, "m": 3, "4": 5, "11": 5,
               "5-": 6, "º": 6, "dim": 6, "5": 7, "5+": 8,
               "6": 9, "13": 9, "7": 10, "7M": 11}


def check_accident(total, subj, octave=1):
    """Checks if certain symbol is sharp or flat.

    Uses a chord string and a symbol substring and, based on the contents
    of the substring and its position, determines if its symbol is
    sharp or flat. Then, returns an integer of the corresponding
    amount of semitones.

    Args:
        total (str): string of the chord. ex: "Dm7(b9)"
        subj (str): string of the symbol. ex: "9"
        octave (int): optional, used in case the symbol has 2 digits
    """
    if subj in total and len(total) > 2:
        accident1 = total.index(subj[0]) - 1
        accident2 = total.index(subj[0]) + octave
        if total.endswith(subj):
            accident2 = accident1

        if total[accident1] == "b" or total[accident2] == "-":
            return - 1
        elif total[accident1] == "#" or total[accident2] == "+":
            return 1
        else:
            return 0
    else:
        return 0


def return_degree(n, degree):
    """Returns the second note of an interval.

    Given a tonic and a degree, this function will assign the tonic
    to its index in the list of notes and then sum it with the number
    of semitones associated with the degree in its dictionary. Then,
    return a note from the aforementioned list with the new index.

    Args:
        n (str): note from the chromatic scale
        degree (str): degree between unison ("I") and major seventh
        ("VII"), minor and diminisheds are written in lowercase.
    """
    n = notes.index(n)
    n += degrees_dict[degree]

    if n > 11:
        n = n - 12
    return notes[n]


class Scale:
    """Model class to define and instantiate scales.

    Attributes:
        name (str): scale's name.
        structure (list): Degrees that compose the scale, separated by
            minuses. ex: "I-II-III-IV-V-VI-VII"
    """

    def __init__(self, name, structure="I-II-III-IV-V-VI-VII"):
        """Turns the structure into a list."""
        self.name = name
        self.structure = str(structure).split("-")

    def is_minor(self):
        """Returns true if the scale has a minor third."""
        if "iii" in self.structure:
            return True
        else:
            return False

    def is_diminished(self):
        """Returns true if the scale has a diminished fifth."""
        if "v" in self.structure:
            return True
        else:
            return False

    def apply(self):
        """Applies the scale structure to all 12 keys.

        Creates a dictionary to be filled with the notes of the scale
        on all keys, then creates a list of said keys. Iterates the
        dictionary while the number of degrees in the scale isn't met
        and sums to it the second notes of the intervals of the scale,
        using the function return_degree and the tonic.
        """
        total = {"C": [], "C#": [], "D": [], "Eb": [], "E": [], "F": [],
                 "F#": [], "G": [], "G#": [], "A": [], "Bb": [], "B": []}
        keys = list(total.keys())
        degrees = self.structure
        count = 0
        i = 0

        while count < len(degrees):
            for key in total:
                current_degree = return_degree(keys[i], degrees[count])
                total[key].append(current_degree)
                i += 1
            i = 0
            count += 1

        return total


class Chord:
    """doc"""
    def __init__(self, name):
        self.notes = []
        self.name = str(name)
        self.root = self.name[0]

        if len(self.name) > 1:
            if self.name[1] == "#" or self.name[1] == "b":
                self.root = self.root + self.name[1]
        self.notes.append(self.root)

    def has_second(self):
        name = self.name
        if "9" in name or "2" in name:
            degree_index = chords_dict["9"] + check_accident(self.name, "9")
            degree = list(degrees_dict.keys())[degree_index]
            self.notes.append(return_degree(self.root, degree))

    def has_third(self):
        name = self.name
        if "sus" in name or (self.name == self.root + "5"):
            return
        elif "m" in name or "dim" in name or "º" in name or "5-" in name:
            degree_index = chords_dict["m"]
            degree = list(degrees_dict.keys())[degree_index]
            self.notes.append(return_degree(self.root, degree))
        else:
            self.notes.append(return_degree(self.root, "III"))

    def has_fourth(self):
        name = self.name
        if ("sus" in name and "2" not in name) or "4" in name:
            degree_index = chords_dict["4"] + check_accident(self.name, "4")
            degree = list(degrees_dict.keys())[degree_index]
            self.notes.append(return_degree(self.root, degree))
        if "11" in name:
            degree_index = chords_dict["11"] + check_accident(self.name, "11", 2)
            degree = list(degrees_dict.keys())[degree_index]
            self.notes.append(return_degree(self.root, degree))

    def has_fifth(self):
        name = self.name
        if "no5" in name:
            return
        elif "dim" in name or "º" in name or "5-" in name:
            self.notes.append(return_degree(self.root, "v"))
        else:
            degree_index = chords_dict["5"] + check_accident(self.name, "5")
            degree = list(degrees_dict.keys())[degree_index]
            self.notes.append(return_degree(self.root, degree))

    def has_sixth(self):
        name = self.name
        if "6" in name or "13" in name:
            degree_index = chords_dict["13"] + check_accident(self.name, "13", 2)
            degree = list(degrees_dict.keys())[degree_index]
            self.notes.append(return_degree(self.root, degree))

    def has_seventh(self):
        name = self.name
        if "7" in name and ("7M" not in name and "maj7" not in name):
            degree_index = chords_dict["7"] + check_accident(self.name, "7")
            degree = list(degrees_dict.keys())[degree_index]
            self.notes.append(return_degree(self.root, degree))
        if "7M" in name or "maj7" in name:
            degree_index = chords_dict["7M"] + check_accident(self.name, "7M", 1)
            degree = list(degrees_dict.keys())[degree_index]
            self.notes.append(return_degree(self.root, degree))

    def decompose_chord(self):
        self.has_second()
        self.has_third()
        self.has_fourth()
        self.has_fifth()
        self.has_sixth()
        self.has_seventh()


print(__doc__)
print(check_accident.__doc__)
