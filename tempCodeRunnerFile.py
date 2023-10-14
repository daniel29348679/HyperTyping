
    kb.hook(callback)

    while True:
        if len(char_time_up_queue) >0 and time.thread_time_ns() - ch