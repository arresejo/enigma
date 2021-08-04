from functools import reduce

from encoder import CharacterEncoder
from pluglead import PlugLead
from validation import TypeValidator, RegexValidator


class Plugboard(CharacterEncoder):

    """
    Plug Board class

    This class simulates a plug board that aggregate none or maximum 10 plug leads in the Enigma machine.

    Example::
        plugboard = Plugboard()

        plugboard.set("FH TS BE UQ KD AL")

        assert (plugboard.encode("A") == "L")
        assert (plugboard.encode("E") == "B")
        assert (plugboard.encode("Z") == "Z")
    """
    def __init__(self):
        super().__init__()
        self.__plug_leads = []
        self.__adder_validator = TypeValidator(PlugLead)
        self.__setter_validator = RegexValidator("^([A-Z]{2} *){1,10}$")

    def add(self, plug_lead):
        """
        Add a new plug lead to the plug board if the following conditions are met:
        - The plug lead is valid (e.g. not wiring a already allocated character)
        - A free location available on the plug board

        :param plug_lead: A valid Plug Lead
        :type plug_lead: PlugLead
        :raises: :class:`TypeError, ValueError`: If there there is no free location on the plug board
                                                 or if the provided plug lead is invalid
        """
        self.__adder_validator.validate(plug_lead)

        if len(self.__plug_leads) == 10:
            raise ValueError("maximum number of plug leads reached")
        if plug_lead in self.__plug_leads:
            raise ValueError(f"one or both letters in {plug_lead.chars} are already wired")

        self.__plug_leads.append(plug_lead)

    def set(self, string):
        """
        Parse the provided plug board string and set the plug leads accordingly.

        The plug board string must be composed by one or several pairs of letters separated by a space.

        Add a new plug lead to the plug board if the following conditions are met:
        - The plug lead is valid (e.g. not wiring a already allocated character)
        - A free location available on the plug board

        :param string: A valid plug board string
        :type string: str
        :raises: :class:`TypeError, ValueError`: If there there is no free location on the plug board
                                                 or the provided plug board string is invalid

        Example::
            PlugBoard().set("FH TS BE UQ KD AL")
        """
        self.__setter_validator.validate(string)

        for pair in string.upper().split(" "):
            self.add(PlugLead(pair))

    def encode(self, char):
        """
        Encode the provided character accordingly to plug board configuration.

        :param char: The character to encode
        :type char: str
        :return: The encoded character
        :rtype: str
        :raises: :class:`TypeError, ValueError`: If the provided character is invalid
        """
        self._alpha_character_validator.validate(char)
        return reduce((lambda acc, fn: fn.encode(acc)), self.__plug_leads, char)


if __name__ == "__main__":

    # Tests from workbook
    plugboard = Plugboard()

    plugboard.add(PlugLead("SZ"))
    plugboard.add(PlugLead("GT"))
    plugboard.add(PlugLead("DV"))
    plugboard.add(PlugLead("KU"))

    assert (plugboard.encode("K") == "U")
    assert (plugboard.encode("A") == "A")

    # Custom tests
    plugboard = Plugboard()
    plugboard.set("FH TS BE UQ KD AL")
    assert (plugboard.encode("A") == "L")
    assert (plugboard.encode("E") == "B")
    assert (plugboard.encode("Z") == "Z")
