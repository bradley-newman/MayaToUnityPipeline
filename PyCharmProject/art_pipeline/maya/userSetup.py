print("\nRunning userSetup.py...")
import maya_pipeline as mp
import maya.cmds as cmds


def init():
    mp.create_log()
    cmds.scriptJob(event=("quitApplication", on_quit_application))


def on_quit_application():
    print("on_quit_application")
    mp.debug_log("Maya Quit.")


init()

mp.debug_log("Finished running userSetup.py\n", print_to_script_editor=True)
