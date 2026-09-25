# -*- coding: utf-8 -*-
"""Bicycle Workshop Control System (Clean Architecture package).

Layers:
- domain: pure business entities (Usuario, BicicletaTaller)
- application: use cases (LoginService, WorkshopService)
- infrastructure: GUI (CustomTkinter) and composition root
"""

__version__ = "1.0.0"


def main():
    """Launch the application (delegates to the composition root).

    Kept lazy so importing this package does not pull in tkinter;
    the domain and application layers stay GUI-free.
    """
    from bicycle_workshop.infrastructure.app import main as _run
    return _run()


__all__ = ["__version__", "main"]