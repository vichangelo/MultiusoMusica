# -*- coding: latin-1 -*-
"""Module to declare scales and apply them to certain key.

Store declared scales in a class dictionary from the import (see its
documentation for further detail) and return a certain key (chosen by the user)
of one of them.

Imports:
    baseclasses: gets the essential Scale class
Functions:
    scalemake(): handles the process of user input and scale output.
"""

import baseclasses

# Declaring scales to the dictionary in the imported class Scale.
# First the standard major and minor scales.
baseclasses.Scale("M", "I II III IV V VI VII")
baseclasses.Scale("m", "I II iii IV V vi vii")
baseclasses.Scale("Hm", "I II iii IV V vi VII")
baseclasses.Scale("Mm", "I II iii IV V VI VII")

# Now, the greek modes.
baseclasses.Scale("J", "I II III IV V VI VII")
baseclasses.Scale("d", "I II iii IV V VI vii")
baseclasses.Scale("f", "I ii iii IV V vi vii")
baseclasses.Scale("Li", "I II III v V VI VII")
baseclasses.Scale("M", "I II III IV V VI vii")
baseclasses.Scale("E", "I II iii IV V vi vii")
baseclasses.Scale("lo", "I ii iii IV v vi vii")


def scalemake():
    """Receive user input, uses imported function and prints output.

    Vars:
        scale: scale chosen by user to be applied in a certain key.
        tones: all keys's notes in the chosen scale
        key: key chosen by user
    """
    prompt = ("Selecione a escala que deseja usar. Digite 'M' para a escala "
              "diatônica maior e 'm' para a escala diatônica menor.\n")
    print(prompt)
    scale = input("Insira: ")
    tones = baseclasses.Scale.apply(scale)

    print("\nAgora digite, em maiúscula, o tom que deseja.\n")
    key = input("Insira: ")
    print(tones[key])
