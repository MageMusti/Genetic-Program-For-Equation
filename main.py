import sys

if __name__ == "__main__":
    if "--gui" in sys.argv:
        from interface.gui import run_gui
        run_gui()
    else:
        from interface.cli import run_cli
        run_cli(sys.argv)
