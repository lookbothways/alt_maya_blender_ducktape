import bpy
import os
from bpy.types import Operator


bl_info = {
    "name": "ALT Blender Maya Ducktape 2",
    "blender": (4, 5, 0),
    "category": "Interface",
    "version": (1, 0, 5),
    "author": "lookbothways.studio",
    "description": "Orbit like Maya when ALT is held down (auto-loads keymaps safely).",
}


# ------------------------------------------------------------------------
# Keymap helpers
# ------------------------------------------------------------------------
def find_keyconfig_file(name):
    """Find the full path to a built-in keyconfig preset."""
    for d in bpy.utils.script_paths(subdir="presets/keyconfig"):
        candidate = os.path.join(d, name)
        if os.path.exists(candidate):
            return candidate
    print(f"[ALT Ducktape] Could not locate {name}")
    return None


def load_keymap(filename):
    """Use Blender's internal operator to load and activate a keymap preset."""
    try:
        filepath = find_keyconfig_file(filename)
        if not filepath:
            return False
        bpy.ops.preferences.keyconfig_activate(filepath=filepath)
        print(f"[ALT Ducktape] Loaded keymap: {filename}")
        return True
    except Exception as e:
        print(f"[ALT Ducktape] Failed to load {filename}: {e}")
        return False


def init_keymaps():
    """Load both keymaps once at startup to make switching instant."""
    load_keymap("industry_compatible.py")
    load_keymap("blender.py")
    print("[ALT Ducktape] Keymap initialization complete.")
    return None


# ------------------------------------------------------------------------
# ALT-based Keymap Switcher Operator
# ------------------------------------------------------------------------
class ALTKeymapSwitcher(Operator):
    """Toggle keymaps when ALT is held"""
    bl_idname = "wm.alt_keymap_switcher2"
    bl_label = "ALT Blender Maya Ducktape2"
    bl_options = {'REGISTER'}

    is_alt_pressed: bool = False

    def modal(self, context, event):
        if event.type in {'LEFT_ALT', 'RIGHT_ALT'}:
            if event.value == 'PRESS' and not self.is_alt_pressed:
                self.is_alt_pressed = True
                load_keymap("industry_compatible.py")
                #self.report({'INFO'}, "Switched to Industry Compatible keymap")
            elif event.value == 'RELEASE' and self.is_alt_pressed:
                self.is_alt_pressed = False
                load_keymap("blender.py")
                #self.report({'INFO'}, "Switched to Blender keymap")
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


# ------------------------------------------------------------------------
# Registration & Startup Hooks
# ------------------------------------------------------------------------
def delayed_start():
    """Start the ALT keymap switcher after keymaps are initialized."""
    bpy.ops.wm.alt_keymap_switcher2('INVOKE_DEFAULT')
    return None


def register():
    bpy.utils.register_class(ALTKeymapSwitcher)
    bpy.app.timers.register(init_keymaps, first_interval=1.0)
    bpy.app.timers.register(delayed_start, first_interval=2.0)
    print("[ALT Ducktape] Add-on registered successfully.")


def unregister():
    bpy.utils.unregister_class(ALTKeymapSwitcher)
    print("[ALT Ducktape] Add-on unregistered.")


if __name__ == "__main__":
    register()
    bpy.ops.wm.alt_keymap_switcher2('INVOKE_DEFAULT')
