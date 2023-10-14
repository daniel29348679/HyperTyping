# %%
import keyboard as kb
import time
import threading

combo_time = 100  # ms


def write_and_anti(str):
    kb.write(str)
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
            kb.call_later(find_word, (), combo_time * 0.001 * 2)
            print(char_time_up_queue)


def find_word():
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
        # print(pressed_keys)
        if pressed_keys == ["b", "c"]:
            kb.write("\b\bbeacues")
        return
    char_time_up_queue_lock.release()


char_time_up_queue_lock = threading.Lock()
char_time_up_queue = []

if __name__ == "__main__":
    time.sleep(1)
    write_and_anti("'esc+s' -> Setting, 'esc+q' -> Quit")
    kb.hook(callback)

    while True:
        time.sleep(0.0001)
        hotkey = kb.read_hotkey()
        kb.stash_state()
        print(hotkey)
        if hotkey == "esc+q":
            break

    kb.write("\b")
    write_and_anti("Quit HyperTyping successful!!!!")

# %%
