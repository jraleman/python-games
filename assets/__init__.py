"""
Name: __init__.py
Author: jraleman
Year: 2016
"""

# Assets used in some games.
__all__ = ['poc_ttt_provided', 'poc_ttt_provided', 'poc_grid', 'poc_queue',
            'poc_zombie_gui', 'poc_fifteen_gui']

# Deprecated to keep older scripts who import this from breaking
import poc_ttt_provided
import poc_ttt_gui
import poc_grid
import poc_queue
import poc_zombie_gui
import poc_fifteen_gui
