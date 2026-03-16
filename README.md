# KLM Menu — Usage Guide
`klm_menu.py` — Reusable terminal menu engine

---

## Overview

`klm_menu.py` provides a simple hotkey/number-driven terminal menu system.
You define menus as dicts, wire them into a `menu_system` dict, and call
`present_menu()` in a loop. That's it.

---

## Public API

### `present_menu(menu_name, menu_system)`
- Displays the named menu, gets user input, follows sub-menu links.
- Returns `(cmd, menu_name)` when a leaf action is chosen.
- `cmd` is the action string from the menu option (`M_CMD`).

### `display_menu(menu_dict)`
- Prints a menu to stdout. Called internally by `present_menu()`.
- Useful if you want to display without processing input.

### `print_banner(header, star="*", width=25)`
- Prints a decorated header banner. Use anywhere for section headings.

---

## Menu Dict Structure

Each menu is a plain dict with this shape:

```python
my_menu = {
    "menu":    "Title shown in banner",  # display name
    "name":    "key_name",               # key used in menu_system
    "options": [
        # Each option: [cmd, prompt_text, hotkey]
        ["my_action",    "Do Something",  "s"],
        ["menu:submenu", "Open Sub-Menu", "o"],  # ':' means navigate
        ["exit",         "Exit",          "x"],
    ],
    "back_option": True,               # adds a 'Back...' (b) option automatically
    "back_to":     "parent_menu_name"  # key to navigate back to
}
```

### Option format — `[cmd, prompt_text, hotkey]`

| Field | Description |
|---|---|
| `cmd` | Action string returned to your `show_menu()` loop. Use `"menu:<name>"` to navigate to another menu. |
| `prompt_text` | Text shown in the menu list. |
| `hotkey` | Single letter the user can press (case-insensitive). Users can also type the item number. |

---

## Menu System Dict

Collect all menus into one dict keyed by their `"name"`:

```python
menu_system = {
    "main":    main_menu,
    "submenu": sub_menu,
}
```

> The key **must** match the `"name"` field inside the menu dict.

---

## How to Call from `main.py` — Minimal Example

```python
import klm_menu

# 1. Define your menus
main_menu = {
    "menu": "My App",
    "name": "main",
    "options": [
        ["do_work",       "Do Work",   "w"],
        ["menu:settings", "Settings",  "s"],
        ["exit",          "Exit",      "x"],
    ],
    "back_option": False,
    "back_to": None
}

settings_menu = {
    "menu": "Settings",
    "name": "settings",
    "options": [
        ["toggle_flag", "Toggle Flag", "t"],
    ],
    "back_option": True,
    "back_to": "main"
}

# 2. Wire into menu_system
menu_system = {
    "main":     main_menu,
    "settings": settings_menu,
}

# 3. Write your show_menu() loop
def show_menu(m):
    menu_name = "main"          # starting menu key
    while True:
        cmd, menu_name = klm_menu.present_menu(menu_name, m)
        if cmd == "exit":
            break
        elif cmd == "do_work":
            print("Doing work...")
        elif cmd == "toggle_flag":
            print("Flag toggled.")

# 4. Entry point
show_menu(menu_system)
```

---

## How `present_menu()` Navigates

- **cmd contains `:`** → navigation command (e.g. `"menu:settings"`).
  `present_menu()` resolves the target and loops back automatically.
  Your `show_menu()` loop **never sees these** — handled internally.

- **cmd does NOT contain `:`** → leaf action.
  `present_menu()` returns `(cmd, current_menu_name)` to your loop.

- **`"back_option": True`** injects a `Back...` item automatically.
  It returns `"menu:<back_to>"` which `present_menu()` handles internally.

---

## Real Project Example (SpinLaunch Simulator)

```python
sim_menu = {
    "menu": "SpinLaunch Missile Simulator",
    "name": "simulation",
    "options": [
        ["reset_sim",     "Reset Simulation", "n"],
        ["menu:edit_sim", "Edit Simulation",  "e"],
        ["run_sim",       "Run Simulation",   "r"],
        ["menu:output",   "Output",           "o"],
        ["exit",          "Exit",             "x"]
    ],
    "back_option": False,
    "back_to": None
}

edit_sim_menu = {
    "menu": "Edit Simulation Menu",
    "name": "edit_sim",
    "options": [
        ["edit_mass",      "Edit Mass (kg)",     "m"],
        ["edit_distance",  "Edit Distance (km)", "d"],
        ["print_settings", "Print All Settings", "p"],
    ],
    "back_option": True,
    "back_to": "simulation"
}

menu_system = {
    "simulation": sim_menu,
    "edit_sim":   edit_sim_menu,
}

def show_menu(m):
    menu_name = "simulation"
    while True:
        cmd, menu_name = klm_menu.present_menu(menu_name, m)
        if cmd == "exit":
            break
        elif cmd == "reset_sim":
            reset_sim()
        elif cmd == "run_sim":
            run_sim()
        elif cmd == "edit_mass":
            edit_var(e, cmd)
        elif cmd == "print_settings":
            print_all_settings(e)
```

---

## `print_banner()` Standalone Use

Use `print_banner()` anywhere you want a section heading:

```python
klm_menu.print_banner("Results")
# Output:
# *************************
#          Results
# *************************

klm_menu.print_banner("WARNING", star="#", width=30)
```

---

## Tips & Conventions

- Root menu: `"back_option": False`, `"back_to": None`
- Sub-menus: `"back_option": True`, `"back_to": "<parent key>"`
- `"name"` in the menu dict **must** match its key in `menu_system`
- Hotkeys are single letters; keep them unique within each menu
- Users can enter the hotkey letter **or** the item number — both work
- `"exit"` is just a convention for the exit command — handle it in your loop
