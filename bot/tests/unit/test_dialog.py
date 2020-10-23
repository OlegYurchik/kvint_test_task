import pytest

from database.models.types import StateEnum
from dialogs import Dialog


@pytest.mark.parametrize("state, data, text, expected", (
    (StateEnum.START, {}, "/start", StateEnum.SIZE),
    (StateEnum.START, {"абра": "кадабра"}, "Пока", StateEnum.SIZE),
    (StateEnum.SIZE, {}, "Маленькую", StateEnum.PAY_METHOD),
    (StateEnum.SIZE, {}, "крошечнкую", StateEnum.SIZE),
    (StateEnum.PAY_METHOD, {"size": "маленькую"}, "Наличкой", StateEnum.CONFIRM),
    (StateEnum.PAY_METHOD, {"size": "большую"}, "Никак", StateEnum.PAY_METHOD),
    (StateEnum.CONFIRM, {"size": "маленькую", "pay_method": "картой"}, "Да", StateEnum.THANKS),
    (StateEnum.CONFIRM, {"size": "большую", "pay_method": "наличкой"}, "Нет", StateEnum.START),
    (StateEnum.CONFIRM, {"size": "большую", "pay_method": "картой"}, "А?", StateEnum.CONFIRM),
    (StateEnum.THANKS, {}, "Что угодно", StateEnum.START),
    (StateEnum.THANKS, {}, "Любой текст", StateEnum.START),
))
def test_dialog(state, data, text, expected):
    dialog = Dialog(state=state)
    dialog.handle(text=text, data=data)
    assert dialog.state is expected
