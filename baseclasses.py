"""Module with the base classes for the multi-purpose musical python script.

Classes:
    Scale: Has the methods and attributes to instantiate a scale, turning it
        into class data, and apply it to the 12 keys of the chromatic scale.
    Chord: Has the methods and attributes to instantiate a chord and decompose
        it, retrieving its notes.

Imports:
    base: Has essential methods and variables such as the chromatic scale.
"""
import base


class Scale:
    """Class to instantiate and store scales.

    Attributes:
        name_struct (dict): Pair the names and structures of scales.

    Methods:
        apply: Apply the structure of the scale chosen by name to the 12 keys
            of the chromatic scale.
    """

    name_struct = {}

    def __init__(self, name: str, structure: str):
        """Receives a name and structure and assigns then to 'name_struct'.

        Args:
            name: Name of the scale represented symbolically. i.e: "M" for
                the diatonic major scale.
            structure: Structure of the scale in degrees written in roman
                numerals and separated by spaces. i.e: "I II III IV V VI VII"
        """
        Scale.name_struct[name] = structure.split()

    @classmethod
    def apply(cls, scalename):
        """Applies a scale structure to all 12 keys.

        Creates a dictionary to be filled with the notes of the scale
        on all keys, then creates a list of said keys. Iterates the
        dictionary while the number of degrees in the scale isn't met
        and sums to it the second notes of the intervals of the scale,
        using the function return_degree and the tonic.

        Args:
            scalename (str): Name of a scale stored in this class.

        Returns:
            applied_dict (dict): pairs of keys and notes after appliance
        """
        applied_dict = {"C": [], "C#": [], "D": [], "Eb": [],
                        "E": [], "F": [], "F#": [], "G": [],
                        "G#": [], "A": [], "Bb": [], "B": []}
        keys = list(applied_dict.keys())
        degrees = Scale.name_struct[scalename]
        count = 0
        i = 0

        while count < len(degrees):
            for key in applied_dict:
                current_degree = base.return_degree(keys[i],
                                                    degrees[count])
                applied_dict[key].append(current_degree)
                i += 1
            i = 0
            count += 1

        return applied_dict


class Chord:
    """Class to instantiate and operate on chords.

    Instantiates chords with at least their name or notes, and determines the
    functioning of other methods through the central method 'dec_or_comp'.
    Then, through its methods, can compose or decompose the chord discovering
    its name or set of notes.

    Attributes:
        alt_names (list): List of alternative names for the chord.
        formants (set): The chords internal intervals from the root.
        name (str): The chord's name.
        notes (list): The chord's notes.
        root (str): The chord's first note.
        deccomp (int): '0' for decomposing the chord, '1' for the opposite.

    Methods:
        dec_or_comp: Defines if a chord needs decomposing or composing.
        has_second - has_seventh: Adds the interval to the chord's notes, if
            it has it in its name, and vice-versa (putting it in the formants).
        is_inverted: The same as the methods above, but for bar chords.
        decompose: uses the above methods to fully decompose a chord from its
            name to its constituent notes.
    """

    def __init__(self, name="", notes=""):
        """Instantiates the chord and its core attributes."""
        self.name = name
        self.alt_names = []
        self.notes = notes.split(" ")
        self.root = ""
        self.formants = set()

    def dec_or_comp(self):
        """Identify the chord's path and establishes values accordingly.

        Checks whether the chord needs decomposing (empty 'notes') or
        composing ('empty name'), and assigns it to an attribute 'deccomp'
        in form of 0 or 1, respectively, so it can be used as a signal for
        further methods. Then, assigns values to the core attributes,
        identifying the 'root' and preparing 'notes' and 'name' to be filled.
        """
        # For decomposition, 'notes' begins an empty list, 'root' is assigned
        # from the name and added to 'notes', and 'deccomp' is valued 0.
        if self.notes == [""]:
            self.notes = []
            if len(self.name) > 0:
                self.root = self.name[0]
            if len(self.name) > 1:
                if self.name[1] == "#" or self.name[1] == "b":
                    self.root = self.name[:2]
            self.notes.append(self.root)
            self.deccomp = 0

        # For composition, 'root' is assigned from the first note, added
        # to the empty name and 'deccomp' is valued 1.
        if self.name == "":
            self.root = self.notes[0]
            self.name += self.root
            self.deccomp = 1

    def has_second(self):
        """Check for presence of a second or ninth in 'name' or 'notes'."""
        name = self.name

        # Here we can see the usage of 'deccomp' to define whether the chord
        # follows the path of decomposition or composition.

        # If 'deccomp' equals 0, the script detects a symbol in the name
        # and uses the 'base' variable 'degrees_dict' and functions
        # 'return_degree' and 'check_accident' to get the symbol meaning
        # in semitones, check if it is sharp or flat and apply its interval
        # to the root of the chord, appending the result to 'notes'.

        if self.deccomp == 0:
            if "9" in name or "2" in name:
                degree_index = (base.chords_dict["9"]
                                + base.check_accident(self.name, "9"))
                degree = list(base.degrees_dict.keys())[degree_index]
                self.notes.append(base.return_degree(self.root, degree))

        # If 'deccomp' equals 1, the script will check if any of the notes
        # in the list corresponds to this interval from the root, and add
        # the interval's semitones to the set 'formants' if positive.

        if self.deccomp == 1:
            for note in self.notes:
                if note == base.return_degree(self.root, "ii"):
                    self.formants.add(1)
                if note == base.return_degree(self.root, "II"):
                    self.formants.add(2)

    def has_third(self):
        """Check for presence of a third in 'name' or 'notes'."""
        name = self.name

        if self.deccomp == 0:
            if "sus" in name or (self.name == self.root + "5"):
                return
            elif "m" in name or "dim" in name or "5-" in name:
                degree_index = base.chords_dict["m"]
                degree = list(base.degrees_dict.keys())[degree_index]
                self.notes.append(base.return_degree(self.root, degree))
            else:
                self.notes.append(base.return_degree(self.root, "III"))

        if self.deccomp == 1:
            for note in self.notes:
                if note == base.return_degree(self.root, "iii"):
                    self.formants.add(3)
                if note == base.return_degree(self.root, "III"):
                    self.formants.add(4)

    def has_fourth(self):
        """Check for presence of a fourth or eleventh in 'name' or 'notes'."""
        name = self.name

        if self.deccomp == 0:
            if ("sus" in name and "2" not in name) or "4" in name:
                degree_index = (base.chords_dict["4"]
                                + base.check_accident(self.name, "4"))
                degree = list(base.degrees_dict.keys())[degree_index]
                self.notes.append(base.return_degree(self.root, degree))
            if "11" in name:
                degree_index = (base.chords_dict["11"]
                                + base.check_accident(self.name, "11"))
                degree = list(base.degrees_dict.keys())[degree_index]
                self.notes.append(base.return_degree(self.root, degree))

        if self.deccomp == 1:
            for note in self.notes:
                if note == base.return_degree(self.root, "IV"):
                    self.formants.add(5)
                if note == base.return_degree(self.root, "v"):
                    self.formants.add(6)

    def has_fifth(self):
        """Check for presence of a fifth in 'name' or 'notes'."""
        name = self.name

        if self.deccomp == 0:
            if "no5" in name:
                return
            elif "dim" in name or "5-" in name:
                self.notes.append(base.return_degree(self.root, "v"))
            else:
                degree_index = (base.chords_dict["5"]
                                + base.check_accident(self.name, "5"))
                degree = list(base.degrees_dict.keys())[degree_index]
                self.notes.append(base.return_degree(self.root, degree))

        if self.deccomp == 1:
            for note in self.notes:
                if note == base.return_degree(self.root, "v"):
                    self.formants.add(6)
                if note == base.return_degree(self.root, "V"):
                    self.formants.add(7)

    def has_sixth(self):
        """Check for presence of a sixth or thirteenth in 'name' or 'notes'."""
        name = self.name

        if self.deccomp == 0:
            if "6" in name or "13" in name:
                degree_index = (base.chords_dict["13"]
                                + base.check_accident(self.name, "13"))
                degree = list(base.degrees_dict.keys())[degree_index]
                self.notes.append(base.return_degree(self.root, degree))

        if self.deccomp == 1:
            for note in self.notes:
                if note == base.return_degree(self.root, "vi"):
                    self.formants.add(8)
                if note == base.return_degree(self.root, "VI"):
                    self.formants.add(9)

    def has_seventh(self):
        """Check for presence of a seventh in 'name' or 'notes'."""
        name = self.name

        if self.deccomp == 0:
            if "7" in name and ("7M" not in name and "maj7" not in name):
                degree_index = (base.chords_dict["7"]
                                + base.check_accident(self.name, "7"))
                degree = list(base.degrees_dict.keys())[degree_index]
                self.notes.append(base.return_degree(self.root, degree))
            if "7M" in name or "maj7" in name:
                degree_index = (base.chords_dict["7M"]
                                + base.check_accident(self.name, "7M", 1))
                degree = list(base.degrees_dict.keys())[degree_index]
                self.notes.append(base.return_degree(self.root, degree))

        if self.deccomp == 1:
            for note in self.notes:
                if note == base.return_degree(self.root, "vii"):
                    self.formants.add(10)
                if note == base.return_degree(self.root, "VII"):
                    self.formants.add(11)

    def is_inverted(self):
        """Check for presence of an inversion chord."""
        name = self.name
        if len(name) < 3:
            return
        if (name[-1] in base.notes) and (name[-1] not in self.notes):
            self.notes.append(name[-1])
        if (name[-2] in base.notes) and (name[-2:] not in self.notes):
            self.notes.append(name[-2:])

    def decompose(self):
        """Main method, fully decomposes in its constituent notes."""
        self.dec_or_comp()
        self.has_second()
        self.has_third()
        self.has_fourth()
        self.has_fifth()
        self.has_sixth()
        self.has_seventh()
        self.is_inverted()


# Debugging code.
"""name = input("Acorde: ")
x = Chord(name)
x.decompose()
print(x.name, x.notes, x.root)
exit()
"""
