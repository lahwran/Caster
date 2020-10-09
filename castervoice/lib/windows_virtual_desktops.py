import time

from dragonfly import Window, Key
from ctypes import windll
# https://github.com/mrob95/py-VirtualDesktopAccessor
try:
    import pyvda  # pylint: disable=import-error
except Exception as e:
    # This could fail on linux or windows <10
    print("Importing package pyvda failed with exception %s" % str(e))

ASFW_ANY = -1


def go_to_desktop_number(n):
    # Helps make sure that the target desktop gets focus

    with open("C:\Users\Lauren\PycharmProjects\py_inspect\update.trigger", "w") as w:
        w.write(str(time.time()))
    windll.user32.AllowSetForegroundWindow(ASFW_ANY)
    pyvda.GoToDesktopNumber(n)


def move_current_window_to_desktop(n=1, follow=False):
    window_handle = Window.get_foreground().handle
    pyvda.MoveWindowToDesktopNumber(window_handle, n)
    if follow:
        go_to_desktop_number(n)


def close_all_workspaces():
    total = pyvda.GetDesktopCount()
    go_to_desktop_number(total)
    Key("wc-f4/10:" + str(total-1)).execute()

def get_current_desktop():
    return pyvda.GetCurrentDesktopNumber()

enhancer_config = "C:\\Users\\Lauren\\Documents\\GitHub\\win-10-virtual-desktop-enhancer\\settings.ini"
import ConfigParser
class GrumpyConfigParser(ConfigParser.ConfigParser):
    def write(self, fp):
        for section in self._sections:
            fp.write("[%s]\n" % section)
            for (key, value) in self._sections[section].items():
                if key == "__name__":
                    continue
                if (value is not None) or (self._optcre == self.OPTCRE):
                    key = "=".join((key, str(value).replace('\n', '\n\t')))

                fp.write("%s\n" % (key))
            fp.write("\n")

    optionxform = str

def save_desktop_names(names):
    try:

        config = GrumpyConfigParser()
        config.readfp(open(enhancer_config))
        for index, entry in enumerate(names):
            config.set("DesktopNames", str(index+1), entry.replace("(","").replace(")","").replace("|", ", "))
        with open(enhancer_config, 'wb') as configfile:
            config.write(configfile)
    except Exception as e:
        import traceback
        traceback.print_exc()


desktop_names_cache = []
def get_desktop_names(from_cache=True):
    global desktop_names_cache
    import subprocess, os
    if from_cache and desktop_names_cache:
        return desktop_names_cache
    try:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "VirtualDesktop.exe")
        output = subprocess.check_output([path, "/LIST"]).replace("\r", "").replace(" (visible)", "")
        lines = output.split("\n")
        started = False
        desktops = []
        for line in lines:
            if not started:
                if "-" in line:
                    started = True
                continue
            if line.strip():
                line = line.replace(",", "|")
                line = "|".join(entry.strip() for entry in line.split("|"))
                if "|" in line and "(" not in line:

                    line = "(" + line + ")"
                desktops.append(line)
            elif not line.strip():
                break


        print "detected virtual desktops:", repr(desktops)
        save_desktop_names(desktops)
        desktop_names_cache = desktops
        return desktops
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("exception not propagated, caster doesn't know virtual desktop names because of it ")
        return desktop_names_cache
