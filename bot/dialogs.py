from collections import OrderedDict
import re

from transitions import Machine
from transitions.core import MachineError

from database.models.types import StateEnum


class Dialog:
    TRIGGERS = OrderedDict((
        (re.compile(r"Да"), "say_yes"),
        (re.compile(r"Нет"), "say_no"),
        (re.compile(r"Большую"), "say_big"),
        (re.compile(r"Маленькую"), "say_small"),
        (re.compile(r"Картой"), "say_card"),
        (re.compile(r"Наличкой"), "say_cash"),
        (re.compile(r".*"), "say_anything"),
    ))
    TRANSITIONS = [
        {
            "trigger": "say_anything",
            "source": StateEnum.START,
            "dest": StateEnum.SIZE,
            "after": "after",
            "before": "before",
        },
        {
            "trigger": "say_big",
            "source": StateEnum.SIZE,
            "dest": StateEnum.PAY_METHOD,
            "after": "after",
            "before": "before",
        },
        {
            "trigger": "say_small",
            "source": StateEnum.SIZE,
            "dest": StateEnum.PAY_METHOD,
            "after": "after",
            "before": "before",
        },
        {
            "trigger": "say_card",
            "source": StateEnum.PAY_METHOD,
            "dest": StateEnum.CONFIRM,
            "after": "after",
            "before": "before",
        },
        {
            "trigger": "say_cash",
            "source": StateEnum.PAY_METHOD,
            "dest": StateEnum.CONFIRM,
            "after": "after",
            "before": "before",
        },
        {
            "trigger": "say_yes",
            "source": StateEnum.CONFIRM,
            "dest": StateEnum.THANKS,
            "after": "after",
            "before": "before",
        },
        {
            "trigger": "say_no",
            "source": StateEnum.CONFIRM,
            "dest": StateEnum.SIZE,
            "after": "after",
            "before": "before",
        },
        {
            "trigger": "say_anything",
            "source": StateEnum.THANKS,
            "dest": StateEnum.SIZE,
            "after": "after",
            "before": "before",
        },
    ]
    MESSAGES = {
        StateEnum.START: "Привет",
        StateEnum.SIZE: "Какую вы хотите пиццу? Большую или маленькую?",
        StateEnum.PAY_METHOD: "Как вы будете платить?",
        StateEnum.CONFIRM: "Вы хотите {size} пиццу, оплата - {pay_method}?",
        StateEnum.THANKS: "Спасибо за заказ",
    }
    ANSWERS = {
        StateEnum.START: (),
        StateEnum.SIZE: ("Большую", "Маленькую"),
        StateEnum.PAY_METHOD: ("Картой", "Наличкой"),
        StateEnum.CONFIRM: ("Да", "Нет"),
        StateEnum.THANKS: (),
    }

    def __init__(self, state):
        self.machine = Machine(model=self, transitions=self.TRANSITIONS, states=StateEnum,
                               initial=state)
        self.answer = None
        self.data = None

    def handle(self, text, data):
        self.data = data
        self.answer = self.MESSAGES[self.state].format(**self.data)
        for regex, trigger in self.TRIGGERS.items():
            if regex.match(text):
                try:
                    self.trigger(trigger, text=text)
                except MachineError:
                    pass
                break

    def before(self, text):
        self.data[self.state.value] = text.lower()

    def after(self, text):
        self.answer = self.MESSAGES[self.state].format(**self.data)
