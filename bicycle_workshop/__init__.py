# -*- coding: utf-8 -*-
"""Sistema de Control del Taller de Bicicletas (paquete de Arquitectura Limpia).

Capas:
- domain: entidades puras de negocio (Usuario, BicicletaTaller)
- application: casos de uso (LoginService, WorkshopService)
- infrastructure: GUI (CustomTkinter) y raíz de composición
"""

__version__ = "1.0.0"


def main():
    """Inicia la aplicación (delega a la raíz de composición).

    Se mantiene la importación diferida para que importar este paquete no
    cargue tkinter; las capas de dominio y aplicación permanecen libres de GUI.
    """
    from bicycle_workshop.infrastructure.app import main as _run
    return _run()


__all__ = ["__version__", "main"]
