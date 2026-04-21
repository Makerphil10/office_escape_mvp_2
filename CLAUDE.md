# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A text-based office escape room game written in Python (stdlib only, no dependencies). The player navigates rooms, collects items, unlocks doors, and escapes the office.

## Running the Game

```bash
python game.py
```

No build step, no dependencies, no virtual environment needed.

## Architecture

Single-file game (`game.py`) with three classes:

- **Room** — Holds description, items list, exits (direction → Room), and optional lock (item name required to enter).
- **Player** — Tracks inventory and current room.
- **Game** — Owns the room graph, command parser, and game loop. `setup_rooms()` wires all rooms/items/locks. `process_command()` dispatches text input to action methods (`move`, `take`, `look`, etc.).

## Game Flow

The room graph forms a linear progression: Cubicle → Hallway → (Break Room | Server Room) → Lobby (win). Two locked doors gate progress: Server Room requires `keycard` (found in Cubicle), Lobby requires `master key` (found in Server Room).

## Command Parser

`process_command()` splits input into `(action, arg)` on the first space. Action words map to methods — multiple synonyms per action (e.g., `go`/`move`/`walk`). The `take` method has special handling to strip the "up" prefix so "pick up \<item\>" works.
