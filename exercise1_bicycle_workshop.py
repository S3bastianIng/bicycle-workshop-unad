# -*- coding: utf-8 -*-
"""Exercise 1: Bicycle Workshop Control System (Clean Architecture).

Course: Programming (213023) - UNAD
Phase 2 - Project proposal

This file is the thin entry point. The system is organized in layers:
- bicycle_workshop.domain:     entities (User, BicycleWorkshop)
- bicycle_workshop.application: use cases (LoginService, WorkshopService)
- bicycle_workshop.infrastructure: GUI windows and composition root

Run: python exercise1_bicycle_workshop.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bicycle_workshop.infrastructure.app import main

if __name__ == "__main__":
    main()