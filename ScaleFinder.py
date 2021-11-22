# python 3.7.1
"""Programa para encontrar o tom de musicas.

Usa: uma lista com as 12 notas; funções para facilitar
a montagem de escalas e destrinchagem de acordes; uma
classe para instanciar escalas e finalmente uma função
para comparar as notas de determinados acordes com as de
determinada escala e obter os tons mais prováveis.
"""

notes = ["C", "C#", "D", "Eb", "E", "F",
         "F#", "G", "G#", "A", "Bb", "B"]
degrees_dict = {"I": 0, "ii": 1, "II": 2, "iii": 3, "III": 4,
                "IV": 5, "v": 6, "V": 7, "vi": 8, "VI": 9,
                "vii": 10, "VII": 11}
chords_dict = {"2": 2, "9": 2, "m": 3, "4": 5, "11": 5,
               "5-": 6, "º": 6, "dim": 6, "5": 7, "5+": 8,
               "6": 9, "13": 9, "7": 10, "7M": 11}


def check_accident(total, subj):
    """"""
    accident = total.index(subj[0]) - 1

    if total[accident] == "b":
        return - 1
    elif total[accident] == "#":
        return 1
    else:
        return


def return_degree(n, degree):
    """Retorna segunda nota de intervalo.

    Args:
        n (str): nota qualquer da escala cromática
        degree (str): grau qualquer entre união e sétima maior.
    """
    n = notes.index(n)
    n += degrees_dict[degree]

    if n > 11:
        n = n - 12
    return notes[n]


class Scale:
    """Classe modelo para definir escalas.

    Attributes:
        name (str): nome para designar a escala
        structure (list): graus que compõem a escala, a partir da tônica
    """

    def __init__(self, name, structure="I-II-III-IV-V-VI-VII"):
        """Recebe os argumentos em string e torna a estrutura
        uma lista com os graus, para ser usada em conjunto com outra função.
        Parâmetro 'estrutura' é opcional e por padrão é a escala diatônica maior.
        """
        self.name = name
        self.structure = str(structure).split("-")

    def is_minor(self):
        if "iii" in self.structure:
            return True
        else:
            return False

    def is_diminished(self):
        if "v" in self.structure:
            return True
        else:
            return False

    def apply(self):
        """Doc"""
        tons = {"C": [], "C#": [], "D": [], "Eb": [], "E": [], "F": [],
                "F#": [], "G": [], "G#": [], "A": [], "Bb": [], "B": []}
        keys = list(tons.keys())
        degrees = self.structure
        count = 0
        i = 0

        while count < len(self.structure):
            for tom in tons:
                tons[tom].append(return_degree(keys[i], degrees[count]))
                i += 1
            i = 0
            count += 1

        return tons


class Chord:
    """doc"""
    def __init__(self, name):
        self.name = str(name)
        self.notes = []
        self.root = self.name[0]

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
        if ("sus" in name and "2" not in name) or "4" in name or "11" in name:
            degree_index = chords_dict["4"] + check_accident(self.name, "11")
            degree = list(degrees_dict.keys())[degree_index]
            self.notes.append(return_degree(self.root, degree))

    def has_fifth(self):
        name = self.name
        if "no5" in name:
            return
        elif "dim" in name or "º" or "5-" in name:
            self.notes.append(return_degree(self.root, "v"))
        else:
            degree_index = chords_dict["5"] + check_accident(self.name, "5")
            degree = list(degrees_dict.keys())[degree_index]
            self.notes.append(return_degree(self.root, degree))

    def has_sixth(self):
        name = self.name
        if "6" in name or "13" in name:



def comparar(lista_notas, tons_escala, porcentagem=False):
    """Compara as notas de um acorde com uma escala aplicada.

    Usa loops aninhados para acrescentar e atualizar valores
    num dicionário vazio, se notas dos dois primeiros
    parâmetros forem idênticas. Caso um parâmetro opcional
    seja preenchido,retorna uma porcentagem de combinações, caso não,
    retorna o número de matches.

    Args:
        lista_notas (list): nome auto-explicativo
        tons_escala (list): escala aplicada
        porcentagem (bool): opcional, define se a função
                             retornará porcentagem

    Vars:
        i (int): número de positivos

    Returns:
        matches (dict): dicionário associando notas ao seu número de
                         positivos
    """
    matches = {}
    i = 0

    # Itera todas as notas do acorde dentro de um tom, comparando
    # com as notas deste. Se forem idênticas, acrescenta um positivo
    # à nota no dicionário. Depois, itera os tons.
    for tom in tons_escala:
        matches.update({tom[0]: i})  # Aqui, 'tom[0]' é a tônica
        for grau in tom:
            for nota in lista_notas:
                if nota == grau:
                    i += 1
                    matches.update({tom[0]: i})
        i = 0  # Reset de positivos ao trocar de tom

    if porcentagem:
        for match in matches:
            a = matches[match] / len(tons_escala[0])
            b = round(a * 100)
            # if b > 100:
            # b = 100
            matches[match] = str(b) + "%"

    return matches


# Instanciando escala diatônica maior, utilizando estrutura padrão.
dia_maior = Scale("diatonica maior")
tons_maior = dia_maior.apply()

nota = input("Nota ")
grau = input("Grau ")
nts = return_degree(nota, grau)
#print(tons_maior)
print(comparar(nts, tons_maior, True))

# print(__doc__)
# help(Escala)
