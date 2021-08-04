from string import ascii_uppercase

from encoder import TranslationTableEncoder
from validation import TypeValidator, AlphaValidator, LengthValidator, Validator


class Reflector(TranslationTableEncoder):
    """
    Generic Reflector class

    :param wiring: The internal reflector wiring composed by 26 alphabetic characters in upper case
    :type wiring: str
    :raises: :class:`TypeError, ValueError`: If the provided wiring string is invalid

    Example::
       reflector = Reflector("EJMZALYXVBWFCRQUONTSPIKHGD")
    """
    def __init__(self, wiring):
        self.wiring = wiring
        super().__init__(ascii_uppercase, self.wiring)

    @property
    def wiring(self):
        """
        The reflector's wiring

        :getter: Returns the reflector's wiring
        :setter: Sets the reflector's wiring
        :type: str
        """
        return self.__wiring

    @wiring.setter
    def wiring(self, wiring):
        Validator(TypeValidator(str), AlphaValidator(), LengthValidator(26)).validate(wiring)
        self.__wiring = wiring.upper()

    def __str__(self):
        return f"{type(self).__name__}"

    def __repr__(self):
        return f"{type(self).__name__}"


class ReflectorA(Reflector):
    """
    Reflector A class

    This class simulates a reflector with wiring pattern A in the Enigma machine

    Example::
       reflector = ReflectorA()
    """
    def __init__(self):
        super().__init__("EJMZALYXVBWFCRQUONTSPIKHGD")


class ReflectorB(Reflector):
    """
    Reflector B class

    This class simulates a reflector with wiring pattern B in the Enigma machine

    Example::
       reflector = ReflectorB()
    """
    def __init__(self):
        super().__init__("YRUHQSLDPXNGOKMIEBFZCWVJAT")


class ReflectorC(Reflector):
    """
    Reflector C class

    This class simulates a reflector with wiring pattern C in the Enigma machine

    Example::
       reflector = ReflectorC()
    """
    def __init__(self):
        super().__init__("FVPJIAOYEDRZXWGCTKUQSBNMHL")


class ReflectorBThin(Reflector):
    def __init__(self):
        super().__init__("ENKQAUYWJICOPBLMDXZVFTHRGS")


class ReflectorCThin(Reflector):
    def __init__(self):
        super().__init__("RDOBJNTKVEHMLFCWZAXGYIPSUQ")


def reflector_factory(name):
    return globals()[f"Reflector{name}"]()


if __name__ == "__main__":

    reflector = Reflector("FVPJIAOYEDRZXWGCTKUQSBNMHL")

    assert (reflector.encode("F") == "A")
    assert (reflector.encode("A") == "F")
    assert (reflector.encode("D") == "J")
    assert (reflector.encode("J") == "D")
    assert (reflector.encode("L") == "Z")
    assert (reflector.encode("Z") == "L")