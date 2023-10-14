import keyboard as kb
import time

combo_time = 100 #ms

def write_and_anti(str):
    kb.write(str)
    kb.press('shift')
    for _ in range(len(str)):
        kb.send('left')
    kb.release('shift')
    
    
def callback(x):
    print(x)
    if (x.name >='a' and x.name <= 'z') or (x.name >='0' and x.name <= '9'):
        if x.event_type == 'up':
            char_time_up_queue.append((x.name, time.thread_time_ns()))     
    
char_time_up_queue = []

if __name__ == "__main__":
    time.sleep(1)
    write_and_anti("'esc+s' -> Setting, 'esc+q' -> Quit")    
    kb.hook(callback)

    while True:
        if len(char_time_up_queue) >0 and time.thread_time_ns() - char_time_up_queue[-1][1] > combo_time*1000000:
            pressed_keys = [ name for name, _ in char_time_up_queue]
            char_time_up_queue = []
            pressed_keys = pressed_keys.sort()
            print(pressed_keys)
        
        time.sleep(0.001)
        if kb.read_hotkey() == 'esc+q':
            break    

    kb.write('\b')
    write_and_anti("Quit HyperTyping successful!!!!")

    
