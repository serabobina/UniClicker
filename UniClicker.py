import mouse
import keyboard
import time


start_key = 'o'
stop_key = 'p'
delay = 0.1
playing_delay_min = 0
playing_delay_max = 0.1
playing_delay = 0.001
main_delay = 0.01
run_range = -1
delay_delay = 0.00001


def check_key(key):
    flag = keyboard.is_pressed(key)
    if flag:
        while True:
            if not keyboard.is_pressed(key):
                break
    return flag


def check_start():
    return check_key(start_key)


def check_stop():
    return check_key(stop_key)


def run_delay(delay):
    start_time = time.time()

    while True:
        end_time = time.time()

        if end_time - start_time >= delay and delay != -1:
            return 1

        if check_stop():
            return 0

        time.sleep(delay_delay)


def listening():
    print("Listening...")
    events = list()

    x, y = mouse.get_position()
    last_event = mouse.MoveEvent(x=x, y=y, time=12345)

    mouse.hook(events.append)

    run_delay(-1)

    mouse.unhook(events.append)

    events.append(last_event)

    return events


def scroll_speed(event):
    global playing_delay

    if type(event) == mouse.WheelEvent:
        value = -(event.delta / 10000)
        if playing_delay_min <= (playing_delay + value) <= playing_delay_max:
            playing_delay += value


def play(events):
    mouse.hook(scroll_speed)
    for event in events:
        mouse.play([event])

        if not run_delay(playing_delay):
            return 0

        if check_stop():
            return 0

    mouse.unhook(scroll_speed)

    return 1


def run(events, range=-1):
    print("Playing...")
    i = 0
    while True:
        if not play(events):
            return 0

        i += 1

        if i >= range and range != -1:
            break

        if not run_delay(delay):
            return 0
    return 1


def stop_program():
    mouse.unhook_all()
    keyboard.unhook_all()


def CSBlocker():
    usage()
    while True:
        if check_start():
            events = listening()

            run(events, run_range)

            print("Stopped...")

        if check_stop():
            return 0

        if not run_delay(main_delay):
            return 0


def usage():
    message = f'''
Usage:
Listening: press "{start_key}"
Stop listening and start: "{stop_key}"
Edit speed: scroll mouse
Stop running / Exit: "{stop_key}"
'''
    print(message)


def change_number_of_times():
    global run_range

    message = "Write how many times the program should play the subsequence(for infinity -1): "
    while True:
        number_of_times = input(message).strip()

        if number_of_times.isdigit():
            run_range = int(number_of_times)
            return 1
        else:
            message = 'Incorrect. Input must be number: '


def print_modes(modes):
    modes = list(modes)

    print()

    for i in range(len(modes)):
        print(f"{i + 1}) {modes[i]}")


def get_mode(modes):
    message = f"Write number of mode, you want to use: "
    modes = list(modes)
    while True:
        number_of_mode = input(message).strip()

        if number_of_mode.isdigit() and 0 < int(number_of_mode) <= len(modes):
            return modes[int(number_of_mode) - 1]
        else:
            message = f'Incorrect. Input must be number and be in range [1-{len(modes)}]: '


def greeting():
    message = f'''
███    █▄  ███▄▄▄▄    ▄█   ▄████████  ▄█        ▄█   ▄████████    ▄█   ▄█▄     ▄████████    ▄████████   
███    ███ ███▀▀▀██▄ ███  ███    ███ ███       ███  ███    ███   ███ ▄███▀    ███    ███   ███    ███         
███    ███ ███   ███ ███▌ ███    █▀  ███       ███▌ ███    █▀    ███▐██▀      ███    █▀    ███    ███     
███    ███ ███   ███ ███▌ ███        ███       ███▌ ███         ▄█████▀      ▄███▄▄▄      ▄███▄▄▄▄██▀ 
███    ███ ███   ███ ███▌ ███        ███       ███▌ ███        ▀▀█████▄     ▀▀███▀▀▀     ▀▀███▀▀▀▀▀           
███    ███ ███   ███ ███  ███    █▄  ███       ███  ███    █▄    ███▐██▄      ███    █▄  ▀███████████  
███    ███ ███   ███ ███  ███    ███ ███▌    ▄ ███  ███    ███   ███ ▀███▄    ███    ███   ███    ███    
████████▀   ▀█   █▀  █▀   ████████▀  █████▄▄██ █▀   ████████▀    ███   ▀█▀    ██████████   ███    ███     
                                     ▀                           ▀                         ███    ███       
Author: Serabobina'''
    print(message)


def main():
    greeting()

    modes = {"Start": CSBlocker,
             "Change number of times": change_number_of_times}

    while 1:
        print_modes(modes)

        mode = get_mode(modes)

        function = modes[mode]

        ans = function()

        if not ans:
            return


if __name__ == '__main__':
    main()
