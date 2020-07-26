# Credit goes to wolfmanstout
# https://handsfreecoding.org/2020/07/25/say-what-you-see-efficient-ui-interaction-with-ocr-and-gaze-tracking/

# See installation instructions:
# https://github.com/wolfmanstout/gaze-ocr
# Place dll files in <caster_user_directory>caster\data\dll

import threading
import time
import gaze_ocr
import screen_ocr  # dependency of gaze-ocr
 
from dragonfly import (
    Dictation,
    Grammar,
    MappingRule,
    get_engine
)

from castervoice.lib.actions import Key, Text, Mouse
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R
from castervoice.lib import settings

import six
if six.PY2:
    from castervoice.lib.util.pathlib import Path
else:
    from pathlib import Path # pylint: disable=import-error

DLL_DIRECTORY = str(Path(settings.SETTINGS["paths"]["USER_DLL_PATH"]))
 
# Initialize eye tracking and OCR.
tracker = gaze_ocr.eye_tracking.EyeTracker.get_connected_instance(DLL_DIRECTORY)
ocr_reader = screen_ocr.Reader.create_fast_reader()
gaze_ocr_controller = gaze_ocr.Controller(ocr_reader, tracker)
 
 
class OcrRule(MappingRule):
    mapping = {
        # Click on text.
        "<text> click": gaze_ocr_controller.move_cursor_to_word_action("%(text)s") + Mouse("left"),
 
        # Move the cursor for text editing.
        "go before <text>": gaze_ocr_controller.move_cursor_to_word_action("%(text)s", "before") + Mouse("left"),
        "go after <text>": gaze_ocr_controller.move_cursor_to_word_action("%(text)s", "after") + Mouse("left"),
 
        # Select text starting from the current position.
        "words before <text>": gaze_ocr_controller.move_cursor_to_word_action("%(text)s", "before") + Key("shift:down") + Mouse("left") + Key("shift:up"),
        "words after <text>": gaze_ocr_controller.move_cursor_to_word_action("%(text)s", "after") + Key("shift:down") + Mouse("left") + Key("shift:up"),
 
        # Select a phrase or range of text.
        "words <text> [through <text2>]": gaze_ocr_controller.select_text_action("%(text)s", "%(text2)s"),
 
        # Select and replace text.
        "replace <text> with <replacement>": gaze_ocr_controller.select_text_action("%(text)s") + Text("%(replacement)s"),
    }
 
    extras = [
        Dictation("text"),
        Dictation("text2"),
        Dictation("replacement"),
    ]
 
    def _process_begin(self):
        # Start OCR now so that results are ready when the command completes.
        gaze_ocr_controller.start_reading_nearby()
 
if get_engine().name == 'natlink':
    # Force NatLink to schedule background threads frequently by regularly waking up
    # a dummy thread.
    shutdown_dummy_thread_event = threading.Event()
    def run_dummy_thread():
        while not shutdown_dummy_thread_event.is_set():
            time.sleep(1)
    
    dummy_thread = threading.Thread(target=run_dummy_thread)
    dummy_thread.start()
    
    # Initialize a Dragonfly timer to manually yield control to the thread.
    def wake_dummy_thread():
        dummy_thread.join(0.002)
    
    wake_dummy_thread_timer = get_engine().create_timer(wake_dummy_thread, 0.02)
    
    def unload():
        # ... after unloading the grammar ...
        shutdown_dummy_thread_event.set()
        dummy_thread.join()
 
def get_rule():
    return OcrRule, RuleDetails(name="ocr rule")
