from transitions import Machine

from database.models.types import StateEnum


class Dialog:
    TRANSITIONS = [
        StateEnum.START,
        StateEnum.SIZE,
        StateEnum.PAY_METHOD,
        StateEnum.CONFIRM,
        StateEnum.THANKS,
        StateEnum.START,
    ]
    MESSAGES = {
        StateEnum.START: "Привет",
        StateEnum.SIZE: "Какую вы хотите пиццу? Большую или маленькую?",
        StateEnum.PAY_METHOD: "Как вы будете платить?",
        StateEnum.CONFIRM: "Вы хотите большую {size} пиццу, оплата - {pay_method}?",
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
        self.machine = Machine(model=self, states=StateEnum, initial=state)
        self.machine.add_ordered_transitions(self.TRANSITIONS, conditions="check",
                                             after="after", before="before")
        self.answer = None
        self.data = None

    def handle(self, text, data):
        self.data = data
        self.next_state(text=text)

    def check(self, text):
        answers = self.ANSWERS[self.state]
        return not answers or text in answers

    def before(self, text):
        self.data[self.state.value] = text.lower()

    def after(self, text):
        self.answer = self.MESSAGES[self.state].format(**self.data)
