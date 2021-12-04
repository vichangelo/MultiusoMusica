# -*- coding: latin-1 -*-


import baseclasses


def triad_compose(self):
    if (3 not in self.formants) and (4 not in self.formants):
        self.name += "sus"
        if (2 in self.formants) and (5 not in self.formants):
            self.name += "2"
        if 5 in self.formants:
            self.name += "4"

    if self.formants == {7}:
        self.name = self.root + "5"
    if ((8 in self.formants) and (7 not in self.formants)
            and (6 not in self.formants)):
        self.name = self.root + "5+"

    if 3 in self.formants:
        self.name += "m"
    if 6 in self.formants:
        self.name += "(b5)"


def tetrad_compose(self):
    if self.name[-1].isdigit():
        self.name += "/"
    if (9 in self.formants) and ("m(b5)" in self.name):
        self.name = self.root + "dim"
    if 10 in self.formants:
        self.name += "7"
        if "(b5)" in self.name:
            self.name = self.name[:-5] + "7(b5)"

    if 11 in self.formants:
        self.name += "7M"


def extended_compose(self):
    listformant = list(self.formants)
    listformant.sort()

    for f in listformant:
        if (self.name[-1].isdigit()) or (self.name[-1] == "M"):
            self.name += "/"

        if f == 1:
            self.name += "b9"
        if f == 2:
            self.name += "9"

        if f == 4 and (3 in self.formants):
            self.name += "b11"
        if f == 5 and ("4" not in self.name):
            self.name += "11"
        if f == 6 and (7 in self.formants):
            self.name += "#11"

        if f == 8 and (7 in self.formants):
            self.name += "b13"
        if f == 9 and (6 not in self.formants):
            self.name += "13"


def compose(self, rotate=False):
    i = 0
    while i < len(self.notes):
        self.decompose()
        self.triad_compose()
        self.tetrad_compose()
        self.extended_compose()
        if self.name[-1] == "/":
            self.name = self.name[:-1]
        if rotate is False:
            return

        self.alt_names.append(self.name)
        self.notes = self.notes[1:] + self.notes[:1]
        self.name = ""
        self.dec_or_comp()

        #print(self.notes)
        #print(self.root)
        #print(self.name)
        i += 1


baseclasses.Chord.triad_compose = triad_compose
baseclasses.Chord.tetrad_compose = tetrad_compose
baseclasses.Chord.extended_compose = extended_compose
baseclasses.Chord.compose = compose


def run_decompose():
    prompt = ("\nPor favor, insira o acorde para que possamos descobrir "
              "suas notas.\n")
    print(prompt)
    
    name = input("Insira: ")
    chord = baseclasses.Chord(name)
    chord.decompose()

    resultado = "As notas do seu acorde são: {}, {}".format(chord.notes[0],
                                                            chord.notes[1])
    if len(chord.notes) > 2:
        i = 2
        while i < len(chord.notes) - 1:
            resultado += ", {}".format(chord.notes[i])
            i += 1
        if i == len(chord.notes) - 1:
            resultado += " e {}".format(chord.notes[i])
    resultado += "."
    
    print(resultado)

def run_compose():
    prompt = ("\nPor favor, insira as notas em maiúsculas e separadas por "
              "espaços para que possamos identificar o acorde.\n")
    print(prompt)
    
    notes = input("Insira: ")
    chord = baseclasses.Chord("", notes)
    chord.compose(True)
    
    resultado = ("Seu acorde pode ser chamado por {}, "
                 "ou também por {}").format(chord.alt_names[0],
                                            chord.alt_names[1])
    if len(chord.notes) > 2:
        i = 2
        while i < len(chord.notes):
            resultado += ", ou por {}".format(chord.alt_names[i])
            i += 1

    resultado += "."
    print(resultado)
