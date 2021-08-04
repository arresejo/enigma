from string import ascii_uppercase

from reflector import Reflector
from validation import Validator, TypeValidator, RangeValidator


class Rotor(Reflector):
    """
    Generic Rotor class

    This class simulates a rotor with custom wiring pattern in the Enigma machine. It provides functions for mainly
    perform the bidirectional encoding (left-to-right and right-to-left) and the rotation of the rotor.

    Two translation tables are built internally in order to encode a character form the bidirectional encoding:
    - right-to-left table: mapping alphabetic characters from A to Z to the wiring characters
    - left-to-right mapping the wiring characters to the alphabetic characters from A to Z

    :param wiring: The internal rotor wiring composed by 26 alphabetic characters in upper case
    :type wiring: str
    :param notch: The character corresponding to the notch (default value is None)
    :type notch: str
    :param position: The character corresponding to the rotor's start position (default value is "A")
    :type position: str
    :param ring_setting: The one-based rotor's ring setting (default value is 1)
    :type ring_setting: int
    :raises: :class:`TypeError, ValueError`: If one of the provided parameter is invalid

    .. note:: All the class members are ring setting agnostic

    Example::
        rotor = Rotor("FSOKANUERHMBTIYCWLQPZXVGJD")
        assert (rotor.encode_left_to_right("A") == "E")
        assert (rotor.encode_right_to_left("A") == "F")
    """
    def __init__(self, wiring, notch=None, position="A", ring_setting=1):
        super().__init__(wiring)
        self.notch = notch
        self.position = position
        self.ring_setting = ring_setting
        self.__trans_table_right_to_left = str.maketrans(ascii_uppercase, self.wiring)
        self.__trans_table_left_to_right = str.maketrans(self.wiring, ascii_uppercase)

    def reset(self):
        """
        Reset the rotor position to "A" and the ring setting to 1
        """
        self.position = "A"
        self.ring_setting = 1

    def rotate(self):
        """
        Perform one rotation step of the rotor, it updates the position to the next wiring character (circular update)
        """
        self.position = ascii_uppercase[(self.position + 1) % len(ascii_uppercase)]

    def encode_right_to_left(self, char):
        """
        Encode the provided character accordingly to the right to left translation table

        :param char: The character to encode
        :type char: str
        :return: The encoded character
        :rtype: str
        :raises: :class:`TypeError, ValueError`: If the provided character is invalid
        """
        self._alpha_character_validator.validate(char)
        return char.upper().translate(self.__trans_table_right_to_left)

    def encode_left_to_right(self, char):
        """
        Encode the provided character accordingly to the left to right translation table

        :param char: The character to encode
        :type char: str
        :return: The encoded character
        :rtype: str
        :raises: :class:`TypeError, ValueError`: If the provided character is invalid
        """
        self._alpha_character_validator.validate(char)
        return char.upper().translate(self.__trans_table_left_to_right)

    @property
    def notch(self):
        """
        The rotor's notch

        :getter: Returns the 0-based index of the notch's character
        :setter: Sets the notch's character
        :type: int for the getter, str for the setter
        :raises: :class:`TypeError, ValueError`: If the provided notch's character is invalid
        """
        return self.__notch

    @notch.setter
    def notch(self, notch):
        if notch is not None:
            self._alpha_character_validator.validate(notch)
            self.__notch = ascii_uppercase.index(notch)
        else:
            self.__notch = None

    @property
    def position(self):
        """
        The rotor's position

        .. note:: Use the Use :func:`position <Rotor.char_position>` to get position's character

        :getter: Returns the 0-based index of the rotor's position
        :setter: Sets the rotor's position character
        :type: int for the getter, str for the setter
        """
        return self.__position

    @position.setter
    def position(self, position):
        self._alpha_character_validator.validate(position)
        self.__position = ascii_uppercase.index(position.upper())

    @property
    def char_position(self):
        """
        The rotor's position character

        .. note:: Use :func:`position <Rotor.position>` to get the the 0-based index

        :return: The character corresponding to the current rotor's position
        :rtype: str
        """
        return ascii_uppercase[self.__position]

    @property
    def ring_setting(self):
        """
        The rotor's ring setting

        .. note:: The ring setting allowed range of values is 1-26

        :getter: Returns the value of the ring setting
        :setter: Sets the value of the ring setting
        :type: int
        :raises: :class:`TypeError, ValueError`: If the provided ring setting invalid
        """
        return self.__ring_setting

    @ring_setting.setter
    def ring_setting(self, ring_setting):
        Validator(TypeValidator(int), RangeValidator(1, 26)).validate(ring_setting)
        self.__ring_setting = ring_setting

    @property
    def on_notch_position(self):
        """
        Check if the rotor is on notch position

        :return: True if the current rotor's position is on notch, False otherwise
        :rtype: bool
        """
        return self.position == self.notch


class RotorI(Rotor):
    """
    Rotor I class

    This class simulates a rotor with wiring pattern I in the Enigma machine

    Example::
        rotor = RotorI()
    """
    def __init__(self, position="A", ring_setting=1):
        super().__init__("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q", position, ring_setting)


class RotorII(Rotor):
    """
    Rotor II class

    This class simulates a rotor with wiring pattern II in the Enigma machine

    Example::
        rotor = RotorII()
    """
    def __init__(self, position="A", ring_setting=1):
        super().__init__("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E", position, ring_setting)


class RotorIII(Rotor):
    """
    Rotor III class

    This class simulates a rotor with wiring pattern III in the Enigma machine

    Example::
        rotor = RotorIII()
    """

    def __init__(self, position="A", ring_setting=1):
        super().__init__("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V", position, ring_setting)


class RotorIV(Rotor):
    """
    Rotor IV class

    This class simulates a rotor with wiring pattern IV in the Enigma machine

    Example::
        rotor = RotorIV()
    """
    def __init__(self, position="A", ring_setting=1):
        super().__init__("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J", position, ring_setting)


class RotorV(Rotor):
    """
    Rotor V class

    This class simulates a rotor with wiring pattern V in the Enigma machine

    Example::
        rotor = RotorV()
    """
    def __init__(self, position="A", ring_setting=1):
        super().__init__("VZBRGITYUPSDNHLXAWMJQOFECK", "Z", position, ring_setting)


class RotorBeta(Rotor):
    """
    Rotor Beta class

    This class simulates a rotor with wiring pattern Beta in the Enigma machine

    Example::
        rotor = RotorBeta()
    """
    def __init__(self, position="A", ring_setting=1):
        super().__init__("LEYJVCNIXWPBQMDRTAKZGFUHOS", None, position, ring_setting)


class RotorGamma(Rotor):
    """
    Rotor Gamma class

    This class simulates a rotor with wiring pattern Gamma in the Enigma machine

    Example::
        rotor = RotorGamma()
    """
    def __init__(self, position="A", ring_setting=1):
        super().__init__("FSOKANUERHMBTIYCWLQPZXVGJD", None, position, ring_setting)


def rotor_factory(name):
    return globals()[f"Rotor{name}"]()


if __name__ == "__main__":

    rotor = Rotor("FSOKANUERHMBTIYCWLQPZXVGJD")
    assert (rotor.encode_left_to_right("A") == "E")
    assert (rotor.encode_right_to_left("A") == "F")

    rotor = RotorI()
    assert (rotor.encode_right_to_left("A") == "E")
    assert (rotor.encode_left_to_right("A") == "U")
