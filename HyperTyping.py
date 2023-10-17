# %%
import keyboard as kb
import time
import threading

combo_time = 10  # ms
print_string_delay = 0  # ms


def write_and_anti(str):
    kb.write(str, delay=print_string_delay * 0.001)
    kb.press("shift")
    for _ in range(len(str)):
        kb.send("left")
    kb.release("shift")


allow_keys = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
]


def callback(x):
    global char_time_up_queue
    print(x)
    if x.name in allow_keys:
        if x.event_type == "up":
            char_time_up_queue_lock.acquire()
            char_time_up_queue.append((x.name, time.monotonic_ns()))
            char_time_up_queue_lock.release()
            kb.call_later(check_word, (), combo_time * 0.001 * 2)
            print(char_time_up_queue)


def check_word():
    global char_time_up_queue
    print("find_word")
    char_time_up_queue_lock.acquire()
    if (
        len(char_time_up_queue) > 0
        and time.monotonic_ns() - char_time_up_queue[-1][1] > combo_time * 1000000
    ):
        pressed_keys = []
        for charname, _ in char_time_up_queue:
            if charname not in pressed_keys:
                pressed_keys.append(charname)

        char_time_up_queue = []
        char_time_up_queue_lock.release()

        pressed_keys.sort()
        pressed_keys = tuple(pressed_keys)
        find_word(pressed_keys)
        return
    char_time_up_queue_lock.release()


def find_word(keys):
    global word_dict
    word_dict_lock.acquire()
    if keys in word_dict:
        for _ in range(len(keys)):
            kb.send("backspace")
        kb.write(word_dict[keys])
    word_dict_lock.release()


def init_word_dict():
    global word_dict
    with open("word_dict.txt", "r") as f:
        for line in f:
            line = line.strip()
            [keyword, word] = line.split(",")
            keys = [ch for ch in keyword]
            keys.sort()
            keys = tuple(keys)
            word_dict[keys] = word
            print(keys, word)


char_time_up_queue_lock = threading.Lock()
char_time_up_queue = []

word_dict = {}
word_dict_lock = threading.Lock()

if __name__ == "__main__":
    init_word_dict()
    time.sleep(2)
    write_and_anti("'esc+h' -> Menu, 'esc+q' -> Quit HyperTyping")
    kb.hook(callback)

    while True:
        time.sleep(0.0001)
        hotkey = kb.read_hotkey()
        kb.stash_state()
        print(hotkey)
        if hotkey == "esc+h":
            kb.send("backspace")
            write_and_anti("'s' -> Setting, 'q' -> Quit HyperTyping")
            hotkey = kb.read_hotkey()
            kb.stash_state()

            if hotkey == "q":
                break
            if hotkey == "s":
                kb.send("backspace")
                write_and_anti("'a' -> All word dictionary, 'q' -> Quit")
                hotkey = kb.read_hotkey()
                kb.stash_state()

                if hotkey == "a":
                    kb.send("backspace")
                    word_dict_lock.acquire()
                    for keys, word in word_dict.items():
                        print(str(keys) + " -> " + word)
                    word_dict_lock.release()
                    continue
                if hotkey == "q":
                    kb.send("backspace")
                    continue
            continue

        elif hotkey == "esc+q":
            break

    kb.send("backspace")
    write_and_anti("Quit HyperTyping successful!!!!")

# %%
