"""
Real-Time ASCII Camera - Terminal Renderer
Uses curses for smooth, flicker-free terminal output.
"""

import curses
from typing import List, Optional


class AsciiRenderer:
    """Curses-based terminal renderer for ASCII art"""
    
    def __init__(self):
        self.stdscr: Optional[curses.window] = None
        self.width = 0
        self.height = 0
    
    def set_screen(self, stdscr: curses.window):
        """Set the curses screen"""
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        
        # Configure curses
        curses.curs_set(0)  # Hide cursor
        curses.noecho()
        curses.cbreak()
        self.stdscr.nodelay(True)  # Non-blocking input
        self.stdscr.keypad(True)
    
    def get_dimensions(self) -> tuple:
        """Get current terminal dimensions (width, height)"""
        if self.stdscr:
            self.height, self.width = self.stdscr.getmaxyx()
        return self.width, self.height
    
    def render_frame(self, lines: List[str]):
        """Render a complete ASCII frame to the terminal (Grayscale)"""
        if not self.stdscr:
            return
        
        try:
            self.stdscr.clear()
            for y, line in enumerate(lines):
                if y >= self.height - 1: break
                try:
                    self.stdscr.addstr(y, 0, line[:self.width - 1])
                except: pass
            self.stdscr.refresh()
        except: pass

    def render_status(self, text: str):
        """Render a status line at the bottom"""
        if not self.stdscr:
            return
        try:
            self.stdscr.addstr(self.height - 1, 0, text[:self.width - 1], curses.A_REVERSE)
        except curses.error:
            pass
    
    def get_key(self) -> Optional[int]:
        """Get a key press (non-blocking)"""
        if not self.stdscr:
            return None
        try:
            return self.stdscr.getch()
        except curses.error:
            return None
