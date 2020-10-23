import enum


@enum.unique
class StateEnum(enum.Enum):
    START = "START"
    SIZE = "size"
    PAY_METHOD = "pay_method"
    CONFIRM = "confirm"
    THANKS = "thanks"
