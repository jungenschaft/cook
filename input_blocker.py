from pynput import keyboard, mouse

pressed = set()

def on_press(key):
    pressed.add(key)
    # Uncomment to allow Alt+F4 during manual testing:
    # if keyboard.Key.alt in pressed and key == keyboard.Key.f4:
    #     return True
    return False

def on_release(key):
    pressed.discard(key)
    return False

keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release, suppress=True)
keyboard_listener.start()

mouse_listener = mouse.Listener(on_click=lambda *args: False, on_scroll=lambda *args: False, suppress=True)
mouse_listener.start()
