from abc import ABC
from abc import abstractmethod

from validation import Validator, TypeValidator, LengthValidator, AlphaValidator


class CharacterEncoder(ABC):
    """
    Character Encoder abstract class

    This class is the foundation for an encoder definition. It instantiates the commons validators in order to check
    if the provided character to encode is an alphabetic character of length 1.

    This class defines also the abstract encode method to be implemented by child classes.
    """
    def __init__(self):
        self._alpha_character_validator = Validator(TypeValidator(str), LengthValidator(1), AlphaValidator())

    @abstractmethod
    def encode(self, char):
        pass


class TranslationTableEncoder(CharacterEncoder):
    """
    Translation Table Encoder class

    This class allows to encode a character accordingly to a translation table.

    The constructor takes two arguments x and y of equal length, each character in x will
    be mapped to the character at the same position in y.

    :param x: The string with current characters
    :type x: str
    :param y: The string with mapping characters
    :type y: str

    Example::
        encoder = TranslationTableEncoder("ABC", "123")
        encoder.encode("A") == "1"
    """
    def __init__(self, x, y):
        super().__init__()
        self._trans_table = str.maketrans(x, y)

    def encode(self, char):
        """
        Encode the provided character accordingly to the translation table

        :param char: The character to encode
        :type char: str
        :return: The encoded character
        :rtype: str
        :raises: :class:`TypeError, ValueError`: If the provided character is invalid
        """
        self._alpha_character_validator.validate(char)
        return str(char).upper().translate(self._trans_table)


if __name__ == "__main__":

    encoder = TranslationTableEncoder("ABC", "XYZ")

    assert (encoder.encode("A") == "X")
    assert (encoder.encode("B") == "Y")
    assert (encoder.encode("C") == "Z")
    assert (encoder.encode("D") == "D")
