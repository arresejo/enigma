import re
from abc import ABC
from abc import abstractmethod


class Validatable(ABC):
    @abstractmethod
    def validate(self, item):
        pass


class Validator(ABC):

    def __init__(self, *validators):
        self.__validators = validators

    def validate(self, item):
        return all(map(lambda x: x.validate(item), self.__validators))


class TypeValidator(Validatable):
    def __init__(self, item_type):
        self.__item_type = item_type

    def validate(self, item):
        if not isinstance(item, self.__item_type):
            raise TypeError(f"must be a {self.__item_type.__name__}")
        return True


class LengthValidator(Validatable):
    def __init__(self, item_len, compare_fct=lambda x, y: x == y):
        self.__item_len = item_len
        self.__compare_fct = compare_fct

    def validate(self, item):
        if not self.__compare_fct(len(item), self.__item_len):
            raise ValueError(f"length is invalid")
        return True


class AlphaValidator(Validatable):
    def validate(self, item):
        if not str(item).isalpha():
            raise ValueError("must be alphabetical")
        return True


class UniqueValuesValidator(Validatable):
    def __init__(self, nb_unique, case_sensitive=False):
        self.__nb_unique = nb_unique
        self.__case_sensitive = case_sensitive

    def validate(self, item):
        if not self.__case_sensitive:
            item = str(item).lower()
        if len(set(item)) != self.__nb_unique:
            raise ValueError(f"must composed of {self.__nb_unique} unique values")
        return True


class RegexValidator(Validatable):
    def __init__(self, regex):
        self.__regex = re.compile(regex)

    def validate(self, item):
        if not self.__regex.match(item):
            raise ValueError(f"must match with regex {self.__regex}")
        return True


class RangeValidator(Validatable):
    def __init__(self, min_range, max_range, inclusive=True):
        self.__min_range = min_range
        self.__max_range = max_range
        self.__inclusive = inclusive

    def validate(self, item):
        if self.__inclusive:
            valid_range = self.__min_range <= item <= self.__max_range
        else:
            valid_range = self.__min_range < item < self.__max_range
        if not valid_range:
            raise ValueError(f"must be between {self.__min_range} and {self.__max_range}")
        return True


if __name__ == "__main__":
    pass
