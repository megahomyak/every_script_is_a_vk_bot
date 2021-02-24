[Документация на русском | RU docs](README_RU.md)

# Every script is a VK bot

VK bots is a python beginners' worst disease, but I'm moving it to the next level!
This library can turn your code into a VK bot.

## Usage:

### Installation:

    pip install every_script_is_a_vk_bot

### Import some functions from it:

    from every_script_is_a_vk_bot import print, input, start

### Call a `start` function at the beginning of your script, passing a token in it:

    start("your-vk-token")

    a = do_something()
    print(a)

### You can also pass your login (`phone_number`) and `password`:

    start(phone_number=1234567890, password="your-great-password")

### You can also pass `group_id` if this is a group:

    start(token="your-group-vk-token", group_id=1234567)

### Run your program and send the `/start` (or `/старт`) message to the bot to continue the program's execution from the `start()` call:

![Start message](start_message.png)

### `print()` will send messages to the chat where the bot was started (`print` won't send anything if no arguments were passed):

    print("abc", 123, sep=".")  # Output will be "abc.123" (without quotes)

### `input()` will wait for messages from the guy who started the bot and from the same chat where it was started:

    a = input()  # Waiting for messages

    print(a)  # Sending user's input as an output

### You can change `input`'s behavior by setting `listen_only_first_user` to `False`. Now it will catch any messages from any user as an input:

    start("your-group-vk-token", listen_only_first_user=False)

    # Also it will disable the need to write '/start' to start the bot

### If you want to disable messages in your console, you need to pass a `console_messages_enabled` argument to `start`, setting this argument to `False`:

    start("your-group-vk-token", console_messages_enabled=False)

### You can also specify the language of messages in the console:

    start("your-group-vk-token", language="ru")  # Or language="eng"

### Example:

    from every_script_is_vk_a_bot import start, print, input

    start(
        "your-group-vk-token",
        console_messages_enabled=False, listen_only_first_user=False
    )
    
    while True:
        msg = input()
        if msg == "hi":
            print("Hello!")

