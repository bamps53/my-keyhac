import time
import keyhac
import pyauto
from keyhac import *
from pyauto import *


def configure(keymap):
    # キーバインドに"したくない"アプリケーションソフトを指定する（False を返す）
    def is_target(window):
        if window.getProcessName() in ("cmd.exe",            # cmd
                                       "mintty.exe",         # mintty
                                       "gvim.exe",           # GVim
                                       # "eclipse.exe",        # Eclipse
                                       "VirtualBox.exe",     # VirtualBox
                                       "putty.exe",          # PuTTY
                                       "ttermpro.exe",       # TeraTerm
                                       "vncviewer.exe"):     # UltraVNC
            return False
        return True

    keymap_global = keymap.defineWindowKeymap(check_func=is_target)

    # 【基本方針】
    # UNIXライクな感じで端末とそれ以外との違和感を減らす

    # 【補足事項】
    # CapsLockキーは，そこそこ良い所にあるキーなのでモディファイアとして使用したい
    # しかしながらCapsLockはKeyhacだけだとうまくモディファイできないので一旦レジストリで右Ctrlになっていることを想定しています
    # 本来のショートカットであるC-?を潰すとたまに面倒くさいことになるので，
    # それらはLC-RC-?で呼び出せるようにしておきます
    # User modifier key definition
    keymap.defineModifier("Apps", "User0")
    keymap.defineModifier("(9)", "User1")
    keymap_global["O-(9)"] = "Tab"
    keymap_global["S-(9)"] = "Shift-Tab"
    keymap_global["C-(9)"] = "Ctrl-Tab"

    # 【矢印キー】
    keymap_global["U0-H"] = "Left"
    keymap_global["U0-J"] = "Down"
    keymap_global["U0-K"] = "Up"
    keymap_global["U0-L"] = "Right"

    keymap_global["U0-U1-H"] = "C-Left"
    keymap_global["U0-U1-J"] = "C-Down"
    keymap_global["U0-U1-K"] = "C-Up"
    keymap_global["U0-U1-L"] = "C-Right"

    keymap_global["U0-U"] = "Home"
    keymap_global["U0-I"] = "End"
    keymap_global["U0-U1-U"] = "Shift-Home"
    keymap_global["U0-U1-I"] = "Shift-End"
    keymap_global["U0-Y"] = "End", "S-Home"
    keymap_global["U0-U1-Y"] = "End", "S-Home"
    keymap_global["U0-O"] = "Back"
    keymap_global["U0-P"] = "Delete"
    keymap_global["U0-U1-O"] = "Shift-Home", "Back"
    keymap_global["U0-U1-P"] = "Shift-End", "Delete"

    keymap_global["U0-M"] = "Enter"
    keymap_global["U0-Space"] = "Enter"

    keymap_global["O-LAlt"] = "Alt-BackQuote"

    keymap_global["U0-D"] = keymap.defineMultiStrokeKeymap("U0-D")
    keymap_global["U0-D"]["U0-D"] = "Home", "S-End", "C-X", "Back"
    keymap_global["U0-D"]["U0-W"] = "C-S-Right", "C-X"
    keymap_global["U0-D"]["U0-B"] = "C-S-Left", "C-X"

    def delay(sec=0.05):
        time.sleep(sec)

    def get_clippedText():
        return (getClipboardText() or "")

    def paste_string(s):
        setClipboardText(s)
        delay()
        keymap.InputKeyCommand("C-V")()

    def copy_string(sec=0.05):
        keymap.InputKeyCommand("C-C")()
        delay(sec)
        return get_clippedText()

    def send_input(ime_mode, keys, sleep=0.01):
        if ime_mode is not None:
            if keymap.getWindow().getImeStatus() != ime_mode:
                keymap.InputKeyCommand("(243)")()
        for key in keys:
            delay(sleep)
            try:
                keymap.InputKeyCommand(key)()
            except:
                keymap.InputTextCommand(key)()

    def find_window(arg_exe, arg_class):
        wnd = pyauto.Window.getDesktop().getFirstChild()
        last_found = None
        while wnd:
            if wnd.isVisible() and not wnd.getOwner():
                # if wnd.getProcessName() == arg_exe:
                # print(wnd.getClassName() == arg_class)
                if wnd.getClassName() == arg_class and wnd.getProcessName() == arg_exe:
                    last_found = wnd
            wnd = wnd.getNext()
        return last_found

    def google_search():

        if keymap.getWindow().getProcessName() == "chrome.exe":
            send_input(1, ["C-T", "C-K"])
        else:
            wnd = find_window("chrome.exe", "Chrome_WidgetWin_1")
            print(wnd.getClassName(), wnd.getProcessName())
            if wnd:
                send_input(1, ["C-LWin-1", "C-T", "C-K"], 0.05)
            else:
                send_input(1, ["LWin-1"])

    keymap_global["U0-S"] = google_search
