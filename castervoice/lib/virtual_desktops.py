import sys

if sys.platform == "win32":
    from .windows_virtual_desktops import (
        go_to_desktop_number, get_current_desktop, move_current_window_to_desktop, close_all_workspaces, get_desktop_names
    )
else:
    def unimplemented(*args, **keywordargs):
        print("Virtual desktop commands are not implemented on this platform")


    go_to_desktop_number = get_current_desktop = move_current_window_to_desktop = close_all_workspaces = unimplemented

def go_to_desktop_partial(n):
    def result(n):
        return go_to_desktop_number(n)
    return result


def names_to_indices(from_cache=True):
    names = get_desktop_names(from_cache)
    return {name: index+1 for index, name in enumerate(names)}

# commented because: i didn't finish this, this needs testing
#def get_current_desktop_name(from_cache=True):
#    current = get_current_desktop()
#    names = get_desktop_names(from_cache)
