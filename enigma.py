from plugboard import Plugboard
from reflector import ReflectorB, ReflectorA
from rotor import RotorI, RotorII, RotorIII, RotorIV, RotorV, RotorBeta, RotorGamma
from rotorchain import RotorChain
from validation import Validator, TypeValidator, AlphaValidator, LengthValidator


class Enigma:
    """
        This class simulates the Enigma machine

        As models M3 and M4 of the Enigma machine, it supports 3 or 4 rotors configuration.

        The order of reflector and rotors definition respect the physical order (left-to-right).

        :param reflector: The reflector associated to the Enigma machine
        :type reflector: Reflector
        :param *rotors:  The rotors associated to the Enigma machine
        :type *rotors: Variable length rotor list
        :raises: :class:`TypeError, ValueError`: If one of the provided parameter is invalid

        Example::
            enigma = Enigma(ReflectorB(), RotorI(), RotorII(), RotorIII("V"))
            enigma.encode("HELLOWORLDHELLOWORLDHELLOWORLD")

            enigma = Enigma(ReflectorA(), RotorIV("E", 18), RotorV("Z", 24), RotorBeta("G", 3), RotorI("P", 5))
            enigma.plugboard.set("PC XZ FM QA ST NB HY OR EV IU")
            enigma.encode("BUPXWJCDPFASXBDHLBBIBSRNWCSZXQOLBNXYAXVHOGCUUIBCVMPUZYUUKHI")
    """
    def __init__(self, reflector, *rotors):
        self._rotor_chain = RotorChain(reflector, *rotors)
        self.plugboard = Plugboard()
        self.__alpha_string_validator = Validator(TypeValidator(str), LengthValidator(1, lambda x, y: x >= y), AlphaValidator())

    def encode(self, string):
        """
        Perform the whole encoding of a string on the Enigma machine

        Each character of the string is first encoded by the plug board then the character is encoded through the
        rotor chain and finally the character is encoded by the plug board again.

        :param char: The string to encode
        :type char: str
        :return: The encoded string
        :rtype: str
        """
        self.__alpha_string_validator.validate(string)
        encoded_string = ""
        for letter in string:
            encoded_string += self.plugboard.encode(self._rotor_chain.encode(self.plugboard.encode(letter)))
        return encoded_string

    def reset(self):
        """
        Reset all rotors of the machine to position to "A" and the ring setting to 1
        """
        self._rotor_chain.reset()

    @property
    def plugboard(self):
        """
        The plug board associated to the Enigma machine

        :getter: Returns the plug board
        :setter: Sets the plug board
        :type: Plugboard
        """
        return self.__plugboard

    @plugboard.setter
    def plugboard(self, plugboard):
        self.__plugboard = plugboard

    @property
    def reflector(self):
        """
        The reflector associated to the Enigma machine

        :getter: Returns the reflector
        :setter: Sets the reflector
        :type: Reflector
        """
        return self._rotor_chain.reflector

    @reflector.setter
    def reflector(self, reflector):
        self._rotor_chain.reflector = reflector

    @property
    def rotors(self):
        """
        The rotors associated to the Enigma machine

        :getter: Returns the list of rotors
        :setter: Sets the list of rotors
        :type: Rotors list
        """
        return self._rotor_chain.rotors

    @rotors.setter
    def rotors(self, rotors):
        self._rotor_chain.rotors = rotors


if __name__ == "__main__":

    # Testing the only step of rotors IV et V for the very first key press when middle rotor is on notch
    enigma = Enigma(ReflectorB(), RotorIV(), RotorV("Z"), RotorBeta())

    assert(enigma.encode("AZERTYAZERTYAZERTYAZERTYAZERTYAZERTYAZERTYAZERTYAZERTYAZERTYAZERTYAZERTYAZERTYAZERTY") == "ZGQKHTNUHSNXLVKHCXBSKNIQPPQBBVIUXSVCPQDTRTOUNVVXUFGMHEJNDPKTBJREBPDUJIYCHBZHIWZGQKHT")

    #
    enigma = Enigma(ReflectorB(), RotorI(), RotorBeta(), RotorII("E"))
    assert (enigma.encode("AZERTYAZERTYAZERTYAZERTYAZERTYAZERTYAZERTYAZERTYAZERTYAZERTYAZERTYAZERTYAZERTYAZERTY") == "TWFFGKBVYXOTPNXYQUXCYDFFWUUBCOQTZEXLSTSCORRTIORUFMZEKEULQGRSBMPNGFPVJAZSLHMENZUIYORW")

    #
    enigma = Enigma(ReflectorB(), RotorBeta(), RotorI("Q"), RotorGamma())
    assert (enigma.encode("AZERTYAZERTYAZERTYAZERTYAZERTYAZERTYAZERTYAZERTYAZERTYAZERTYAZERTYAZERTYAZERTYAZERTY") == "YTGISZNJKJWKMIZOSUXJJCCUFQBABXYYVGZXMOBSIGXRHINFYBWOJMSVLNUOXFUJWCWJBZWBPIIWMEYTGISZ")

    ##################################################################################################

    # Rotor 3 on notch
    enigma = Enigma(ReflectorB(), RotorI(), RotorII(), RotorIII("V"))
    assert (enigma.encode("HELLOWORLDHELLOWORLDHELLOWORLD") == "KTBGVOLHWWNRWRBYFFRILMOGCSDKRX")

    # Rotor 2 on notch
    enigma = Enigma(ReflectorB(), RotorI(), RotorII("E"), RotorIII())
    assert (enigma.encode("HELLOWORLDHELLOWORLDHELLOWORLD") == "ILFDEEINWRBOFYNJYEMHLOQQAYIHYB")

    # Rotors 2 and 3 on notches
    enigma = Enigma(ReflectorB(), RotorI(), RotorII("E"), RotorIII("V"))
    assert (enigma.encode("HELLOWORLDHELLOWORLDHELLOWORLD") == "VDXRESQKDISZGWPXETYKSLHMSPEJQG")

    # Rotor 1 on notch
    enigma = Enigma(ReflectorB(), RotorI("Q"), RotorII(), RotorIII())
    assert (enigma.encode("HELLOWORLDHELLOWORLDHELLOWORLD") == "SKOWJLNOWXEMKREECEEWZMGDAUPNNR")

    # Rotors 1 and 3 on notches
    enigma = Enigma(ReflectorB(), RotorI("Q"), RotorII(), RotorIII("V"))
    assert (enigma.encode("HELLOWORLDHELLOWORLDHELLOWORLD") == "TMDBGNMPJGYKSIIJHWWGJAAJLVUHSW")

    # Rotors 1 and 2 on notches
    enigma = Enigma(ReflectorB(), RotorI("Q"), RotorII("E"), RotorIII())
    assert (enigma.encode("HELLOWORLDHELLOWORLDHELLOWORLD") == "UIYIXDGFWNUCYQAECEWTANSCCDQHPP")

    # Rotors 1, 2 and 3 on notches
    enigma = Enigma(ReflectorB(), RotorI("Q"), RotorII("E"), RotorIII("V"))
    assert (enigma.encode("HELLOWORLDHELLOWORLDHELLOWORLD") == "ZJQYJEBQIVVYCWXBDZQXSRCWGPJYCF")

    ##################################################################################################

    # Enigma Machine Demonstration

    # Example 1
    # Set up your enigma machine with rotors I II III, reflector B, ring settings 01 01 01, and initial positions A A Z.
    # The plugboard should map the following pairs: HL MO AJ CX BZ SR NI YW DG PK.
    enigma = Enigma(ReflectorB(), RotorI(), RotorII(), RotorIII("Z"))
    enigma.plugboard.set("HL MO AJ CX BZ SR NI YW DG PK")

    assert (enigma.encode("HELLOWORLD") == "RFKTMBXVVW")

    # Example 2
    # Set up your enigma machine with rotors IV V Beta I, reflector A, ring settings 18 24 03 05, and initial positions E Z G P.
    # The plugboard should map the following pairs: PC XZ FM QA ST NB HY OR EV IU.
    # Find the result of decoding the following string: BUPXWJCDPFASXBDHLBBIBSRNWCSZXQOLBNXYAXVHOGCUUIBCVMPUZYUUKHI.
    enigma = Enigma(ReflectorA(), RotorIV("E", 18), RotorV("Z", 24), RotorBeta("G", 3), RotorI("P", 5))
    enigma.plugboard.set("PC XZ FM QA ST NB HY OR EV IU")
    print(enigma.encode("BUPXWJCDPFASXBDHLBBIBSRNWCSZXQOLBNXYAXVHOGCUUIBCVMPUZYUUKHI"))
