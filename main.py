# -*- coding: latin-1 -*-
"""Module that begins the script by invoking the others and their functions.

First, get their input of choice of function, then invokes the respective
module of the script.
"""
import chordcomposer
import keyfinder
import scalemaker

introduction = ("\nOl�! Bem-vindo ao programa multiuso para m�sicos!\n"
                "Digite 'T' para tirar o tom de uma m�sica inserindo "
                "seus acordes, 'A' para identificar ou decomp�r acordes "
                "e 'E' para montar escalas.\n")
print(introduction)


selector1 = str(input("Insira:  "))
if selector1 == "T":
    print(("\nPara descobrir o tom da m�sica, insira os acordes "
          "separados por espa�os.\n"))
    keyfinder.keyfind()

elif selector1 == "A":
    announcement = ("\nDigite 'D' para descobrir as notas de um acorde ou 'I' "
                    "para identificar um acorde a partir de suas notas.\n")
    print(announcement)

    selector2 = str(input("Insira: "))
    if selector2 == "D":
        chordcomposer.run_decompose()
    if selector2 == "I":
        chordcomposer.run_compose()

elif selector1 == "E":
    scalemaker.scalemake()

exit()
