"""
menu_main.py — Generic main.py template using klm_menu
Replace placeholders marked with TODO to build your own project.
"""

import klm_menu

# TODO: import your own modules here
# import my_module


# ---------------------------------------------------------------------------
# Environment / State
# ---------------------------------------------------------------------------

e = {}  # TODO: replace with your env module, e.g. e = my_env.new_env()


# ---------------------------------------------------------------------------
# Action functions  (one per leaf cmd in your menus)
# ---------------------------------------------------------------------------

def action_one():
    # TODO: replace with real logic
    print("Action One executed.")


def action_two():
    # TODO: replace with real logic
    print("Action Two executed.")


def action_three():
    # TODO: replace with real logic
    print("Action Three executed.")


def reset():
    global e
    e = {}  # TODO: replace with your env module, e.g. e = my_env.new_env()
    print("Reset.")


# ---------------------------------------------------------------------------
# Menu definitions
# ---------------------------------------------------------------------------

main_menu = {
    "menu": "My App",           # TODO: rename
    "name": "main",
    "options": [
        ["reset",          "Reset",         "n"],
        ["menu:actions",   "Actions",       "a"],
        ["menu:settings",  "Settings",      "s"],
        ["exit",           "Exit",          "x"],
    ],
    "back_option": False,
    "back_to": None
}

actions_menu = {
    "menu": "Actions",          # TODO: rename / add options
    "name": "actions",
    "options": [
        ["action_one",   "Action One",   "1"],
        ["action_two",   "Action Two",   "2"],
    ],
    "back_option": True,
    "back_to": "main"
}

settings_menu = {
    "menu": "Settings",         # TODO: rename / add options
    "name": "settings",
    "options": [
        ["action_three", "Action Three", "t"],
    ],
    "back_option": True,
    "back_to": "main"
}

menu_system = {
    "main":     main_menu,
    "actions":  actions_menu,
    "settings": settings_menu,
}


# ---------------------------------------------------------------------------
# Menu loop
# ---------------------------------------------------------------------------

def show_menu(m):
    menu_name = "main"
    while True:
        cmd, menu_name = klm_menu.present_menu(menu_name, m)
        if cmd == "exit":
            break
        elif cmd == "reset":
            reset()
        elif cmd == "action_one":
            action_one()
        elif cmd == "action_two":
            action_two()
        elif cmd == "action_three":
            action_three()
        # TODO: add elif branches for every new cmd you add


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    reset()
    show_menu(menu_system)
