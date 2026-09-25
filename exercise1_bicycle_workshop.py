# -*- coding: utf-8 -*-
"""Ejercicio 1: Sistema de Control del Taller de Bicicletas (Arquitectura Limpia).

Curso: Programación (213023) - UNAD
Fase 2 - Propuesta de proyecto

Este archivo es el punto de entrada ligero. El sistema está organizado en capas:
- bicycle_workshop.domain:         entidades (User, BicycleWorkshop)
- bicycle_workshop.application:    casos de uso (LoginService, WorkshopService)
- bicycle_workshop.infrastructure: ventanas GUI y raíz de composición

Ejecutar: python exercise1_bicycle_workshop.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bicycle_workshop.infrastructure.app import main

if __name__ == "__main__":
    main()
