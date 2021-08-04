from encoder import TranslationTableEncoder
from validation import Validator, TypeValidator, AlphaValidator, UniqueValuesValidator


class PlugLead(TranslationTableEncoder):

    """
    Plug Lead class

    This class simulates a lead that connect two plugs in the Enigma machine

    :param chars: A string that represents the two different characters the lead should connect
    :type chars: str
    :raises: :class:`TypeError, ValueError`: If the provided chars string is invalid

    Example::
        lead = PlugLead("AG")
        lead.encode("A")
    """
    def __init__(self, chars):
        self.chars = chars
        super().__init__(self.chars, self.chars[::-1])

    @property
    def chars(self):
        """
        The two characters the plug lead connects

        :getter: Returns the plug lead's characters
        :setter: Sets the plug lead's characters
        :type: str
        """
        return self.__chars

    @chars.setter
    def chars(self, chars):
        Validator(TypeValidator(str), AlphaValidator(), UniqueValuesValidator(2)).validate(chars)
        self.__chars = chars.upper()

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return len(set(self._trans_table.keys()).intersection(set(other._trans_table.keys()))) > 0
        return False


if __name__ == "__main__":

    # tests from workbook
    lead = PlugLead("AG")
    assert (lead.encode("A") == "G")
    assert (lead.encode("D") == "D")

    lead = PlugLead("DA")
    assert (lead.encode("A") == "D")
    assert (lead.encode("D") == "A")

    # custom tests
    good_inputs = [("AB", "A"), ("AB", "B"), ("AB", "C")]
    expected_outputs = ["B", "A", "C"]

    bad_inputs = ["", "A", "AA"]
    expected_error = [ValueError] * len(bad_inputs)

    # meta-tests
    assert (len(good_inputs) == len(expected_outputs))
    assert (len(bad_inputs) == len(expected_error))

    # good tests (normal and boundary)
    for i in range(len(good_inputs)):
        assert (PlugLead(good_inputs[i][0]).encode(good_inputs[i][1]) == expected_outputs[i])

    # bad tests (errors)
    for i in range(len(bad_inputs)):
        try:
            PlugLead(bad_inputs[i])
            assert False
        except expected_error[i]:
            pass





