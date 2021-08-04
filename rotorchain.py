from string import ascii_uppercase

from encoder import CharacterEncoder
from reflector import Reflector, ReflectorB, ReflectorC
from rotor import RotorI, RotorII, RotorIII, RotorIV, RotorV, RotorBeta, Rotor
from validation import TypeValidator, RangeValidator


class RotorChain(CharacterEncoder):
    """
    This class simulates a rotor chain in the Enigma machine

    As models M3 and M4 of the Enigma machine, it supports 3 or 4 rotors configuration and allows to encode a character
    through the whole rotor chain, it handles also the rotation and ring setting logic.

    The order of reflector and rotors definition respect the physical order (left-to-right).

    :param reflector: The reflector associated to the rotor chain
    :type reflector: Reflector
    :param *rotors:  The rotors associated to the rotor chain
    :type *rotors: Variable length rotor list
    :raises: :class:`TypeError, ValueError`: If one of the provided parameter is invalid

    Example::
        rotorChain = RotorChain(ReflectorB(), RotorI(), RotorII(), RotorIII())
        assert(rotorChain.encode("A") == "B")

        rotorChain = RotorChain(ReflectorC(), RotorI("Q", 7), RotorII("E", 11), RotorIII("V", 15), RotorIV("Z", 19))
        assert(rotorChain.encode("Z") == "V")
    """
    def __init__(self, reflector, *rotors):
        super().__init__()
        self.reflector = reflector
        self.rotors = rotors

    def reset(self):
        """
        Reset all rotors of the chain to position to "A" and the ring setting to 1
        """
        for rotor in self.rotors:
            rotor.reset()

    def rotate(self):
        """
        Perform one rotation step of the rotor chain taking into account physical properties like notches on the rotors.

        As described below, the rotation logic is almost the same in both cases we have 3 or 4 rotors.

        In the case of the 3 rotors chain, we start by the rotation of the leftmost rotor. If we consider the following
        rotor chain composed by 3 rotors, lets say R1, R2 and R3. We have two distinct cases of rotation:
        - If R2 is on notch position, R2 and R1 rotate
        - If R3 is on notch position, R2 rotates
        Finally, R3 always rotates.

        In the case of the 4 rotors chain, we start by the rotation of the second rotor from the left because the fourth
        rotor never rotates. If we consider the following rotor chain composed by 4 rotors, lets say R1, R2, R3 and R4.
        We have also two distinct cases of rotations:
        - If R3 is on notch position, R3 and R2 rotate
        - If R4 is on notch position, R3 rotates
        Finally, R4 always rotates.
        """
        start_index = len(self.rotors) - 3
        if self.rotors[start_index+1].on_notch_position:
            self.rotors[start_index+1].rotate()
            self.rotors[start_index].rotate()
        elif self.rotors[start_index+2].on_notch_position:
            self.rotors[start_index+1].rotate()
        self.rotors[start_index+2].rotate()

    def encode_right_to_left(self, char):
        """
        Wrapper function for the right-to-left encoding, see __encode_rotor_chain

        :param char: The character to encode
        :type char: str
        :return: The encoded character
        :rtype: str
        """
        return self.__encode_rotor_chain(char, True)

    def encode_left_to_right(self, char):
        """
        Wrapper function for the left-to-right encoding, see __encode_rotor_chain

        :param char: The character to encode
        :type char: str
        :return: The encoded character
        :rtype: str
        """
        return self.__encode_rotor_chain(char, False)

    def encode(self, char):
        """
        Perform first of all a rotation step then the whole encoding of a character through the rotor chain

        The character to encode follows the path defined by the aggregation of reflectors and rotors wiring inside the
        rotor chain. It starts first from a right-to-left encoding through the rotors then a left-to-right encoding by
        the reflector and finally a left to right encoding.

        :param char: The character to encode
        :type char: str
        :return: The encoded character
        :rtype: str
        """
        self.rotate()
        return self.encode_left_to_right(self.reflector.encode(self.encode_right_to_left(char)))

    def __encode_rotor_chain(self, char, right_to_left):
        """
        Encode a character though the whole rotor chain in a specific direction taking into account physical properties
        like to rotors positions and the ring settings

        :param char: The character to encode
        :type char: str
        :param right_to_left: True if the encoding must be performed from right to left, False otherwise
        :type right_to_left: bool
        :return: The encoded character
        :rtype: str
        :raises: :class:`TypeError, ValueError`: If the provided character is invalid
        """
        self._alpha_character_validator.validate(char)

        current_char, prev_rotor_position = char.upper(), 0

        for rotor in reversed(self.__rotors) if right_to_left else self.__rotors:
            current_char = ascii_uppercase[
                (ascii_uppercase.index(
                    current_char) + rotor.position - rotor.ring_setting + 1 - prev_rotor_position) % len(
                    ascii_uppercase)]
            if right_to_left:
                current_char = rotor.encode_right_to_left(current_char)
            else:
                current_char = rotor.encode_left_to_right(current_char)
            prev_rotor_position = rotor.position - rotor.ring_setting + 1

        current_char = ascii_uppercase[
            (ascii_uppercase.index(current_char) - prev_rotor_position) % len(ascii_uppercase)]

        return current_char

    @property
    def reflector(self):
        """
        The reflector belonging to the chain

        :getter: Returns the reflector
        :setter: Sets the reflector
        :type: Reflector
        :raises: :class:`TypeError`: If the provided reflector is invalid
        """
        return self.__reflector

    @reflector.setter
    def reflector(self, reflector):
        TypeValidator(Reflector).validate(reflector)
        self.__reflector = reflector

    @property
    def rotors(self):
        """
        The list of 3 or 4 rotors belonging to the chain

        :getter: Returns the list of rotors
        :setter: Sets the list of rotors
        :type: Rotors list
        :raises: :class:`TypeError, ValueError`: If the provided list of rotors is invalid
        """
        return self.__rotors

    @rotors.setter
    def rotors(self, rotors):
        RangeValidator(3, 4).validate(len(rotors))
        map(lambda x: TypeValidator(Rotor).validate(x), rotors)
        self.__rotors = rotors

    @property
    def state(self):
        """
        The current state of the rotor chain

        .. note:: The state returned by this getter is ring setting agnostic

        :return: A dictionary with the state of the rotor chain, each key-value pair contains to the rotor's name and
                 the character corresponding to its position
        :rtype: dict
        """
        state = {}
        for rotor in self.rotors:
            state[rotor] = ascii_uppercase[rotor.position]
        return state


if __name__ == "__main__":

    # With rotors I II III, reflector B, ring settings 01 01 01, and initial positions A A Z, encoding an A produces a U
    rotorChain = RotorChain(ReflectorB(), RotorI(), RotorII(), RotorIII("Z"))
    assert(rotorChain.encode("A") == "U")

    # With rotors I II III, reflector B, ring settings 01 01 01, and initial positions A A A, encoding an A produces a B
    rotorChain = RotorChain(ReflectorB(), RotorI(), RotorII(), RotorIII())
    assert(rotorChain.encode("A") == "B")

    # With rotors I II III, reflector B, ring settings 01 01 01, and initial positions Q E V, encoding an A produces an L
    rotorChain = RotorChain(ReflectorB(), RotorI("Q"), RotorII("E"), RotorIII("V"))
    assert(rotorChain.encode("A") == "L")

    # With rotors IV V Beta, reflector B, ring settings 14 09 24, and initial positions A A A, encoding an H produces a Y
    rotorChain = RotorChain(ReflectorB(), RotorIV(ring_setting=14), RotorV(ring_setting=9), RotorBeta(ring_setting=24))
    assert(rotorChain.encode("H") == "Y")

    # With rotors I II III IV, reflector C, ring settings 07 11 15 19, and initial positions Q E V Z, encoding a Z produces a V
    rotorChain = RotorChain(ReflectorC(), RotorI("Q", 7), RotorII("E", 11), RotorIII("V", 15), RotorIV("Z", 19))
    assert(rotorChain.encode("Z") == "V")