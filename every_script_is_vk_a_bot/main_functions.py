import random
from typing import Optional, Generator, Any

import saya

_YOU_NEED_TO_START_THE_BOT_MSG = (
    "Сначала вызови start()", "You need to start() the bot at first"
)

_vk_client: Optional[saya.Vk] = None
current_user_id: Optional[int] = None
current_peer_id: Optional[int] = None
_is_user = None
_console_messages_enabled: bool = True
_preferred_language_is_russian = None
_listen_only_first_user = True


event: Optional[dict] = None


def _translated_print(ru_text: str, eng_text: str) -> None:
    if _console_messages_enabled:
        if _preferred_language_is_russian is None:
            print(f"{ru_text} | {eng_text}")
        else:
            print(ru_text if _preferred_language_is_russian else eng_text)


def _listen_for_messages() -> Generator[dict, Any, None]:
    global event
    for event_ in _vk_client.longpoll.listen(True):  # Dicts instead of lists
        if event_["type"] == "message_new":
            event = event_
            yield event_


def _get_text_from_message(event_: dict) -> str:
    return event_["text"] if _is_user else event_["object"]["message"]["text"]


def _get_peer_id_from_message(event_: dict) -> str:
    return (
        event_["peer_id"]
    ) if _is_user else event_["object"]["message"]["peer_id"]


def _get_from_id_from_message(event_: dict) -> str:
    return (
        event_["object"]["from"]
    ) if _is_user else event_["object"]["message"]["from_id"]


def start(
        token: Optional[str] = None, group_id: Optional[int] = None,
        phone_number: Optional[int] = None,
        password: Optional[str] = None,
        console_messages_enabled: bool = True,
        language: Optional[str] = None,
        listen_only_first_user: bool = True) -> None:
    global _vk_client, _is_user, current_user_id, current_peer_id
    global _console_messages_enabled, _preferred_language_is_russian
    global _listen_only_first_user
    if language is not None:
        if language == "ru":
            _preferred_language_is_russian = True
        elif language == "eng":
            _preferred_language_is_russian = False
        else:
            raise ValueError("language is not equals to ru or eng")
    assert (
        token is not None
        or (phone_number is not None and password is not None)
    ), _translated_print(
        "Тебе нужен хотя бы токен (token) или телефонный номер (phone_number) "
        "с паролем (password), чтобы запустить бота", "You need at least token "
        "or phone_number with password to start the bot"
    )
    _vk_client = saya.Vk(
        token=token, group_id=group_id, login=phone_number, password=password
    )
    _console_messages_enabled = console_messages_enabled
    _listen_only_first_user = listen_only_first_user
    _is_user = not group_id
    if _listen_only_first_user:
        _translated_print(
            'Ожидаю сообщения "/старт"', 'Waiting for the "/start" message'
        )
        for event_ in _listen_for_messages():
            text = _get_text_from_message(event_)
            if text.lower() in ("/старт", "/start"):
                _translated_print(
                    'Сообщение "/старт" получено, продолжаю выполнение скрипта',
                    'The message "/start" was received, continuing script '
                    'execution'
                )
                current_user_id = _get_from_id_from_message(event_)
                current_peer_id = _get_peer_id_from_message(event_)
                return


def print_(*values: Any, sep: Optional[str] = None) -> None:
    assert _vk_client is not None, _translated_print(
        *_YOU_NEED_TO_START_THE_BOT_MSG
    )
    assert current_peer_id is not None, _translated_print(
        "Сначала напиши боту что-то (используя input()), чтоб он знал, куда "
        "отвечать",
        "Provide some input to make the bot know where to send this message"
    )
    if values:
        if sep is None:
            sep = " "
        message = sep.join(map(str, values))
        _vk_client.messages.send(
            message=message, peer_id=current_peer_id,
            random_id=random.randint(0, 1_000_000)
        )


def input_(__prompt: Optional[str] = None, /) -> str:
    global current_peer_id
    assert _vk_client is not None, _translated_print(
        *_YOU_NEED_TO_START_THE_BOT_MSG
    )
    _translated_print(
        "Ожидаю пользовательского ввода", "Waiting for user's input"
    )
    if __prompt is not None:
        print_(__prompt)
    for event_ in _listen_for_messages():
        if (
            not _listen_only_first_user
            or (
                _get_from_id_from_message(event_) == current_user_id
                and _get_peer_id_from_message(event_) == current_peer_id
            )
        ):
            _translated_print("Ввод получен", "Input received")
            if not _listen_only_first_user:
                current_peer_id = _get_peer_id_from_message(event_)
            return _get_text_from_message(event_)
