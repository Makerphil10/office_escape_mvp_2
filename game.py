"""Office Escape MVP - A text-based office escape room game."""

import random


class Room:
    """Represents a room in the office escape game."""

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.items = []
        self.exits = {}
        self.locked = False
        self.lock_requires = None

    def add_exit(self, direction, room):
        self.exits[direction] = room

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            return True
        return False

    def get_description(self):
        desc = f"\n--- {self.name} ---\n{self.description}\n"
        if self.items:
            desc += "\nYou see: " + ", ".join(self.items)
        if self.exits:
            desc += "\nExits: " + ", ".join(self.exits.keys())
        return desc


class Player:
    """Represents the player."""

    def __init__(self):
        self.inventory = []
        self.current_room = None

    def pick_up(self, item):
        self.inventory.append(item)

    def has_item(self, item):
        return item in self.inventory


class Game:
    """Main game controller."""

    def __init__(self):
        self.player = Player()
        self.rooms = {}
        self.running = False
        self.setup_rooms()

    def setup_rooms(self):
        # Create rooms
        cubicle = Room("Your Cubicle", "A cramped office cubicle. Papers are scattered everywhere.")
        hallway = Room("Hallway", "A long, dimly lit hallway. The exit door is to the north.")
        break_room = Room("Break Room", "A small break room with a coffee machine and a locked cabinet.")
        server_room = Room("Server Room", "A cold room filled with humming servers.")
        lobby = Room("Lobby", "The office lobby. The front door is right there!")

        # Add items
        cubicle.add_item("keycard")
        cubicle.add_item("memo")
        break_room.add_item("coffee mug")
        server_room.add_item("master key")

        # Set up exits
        cubicle.add_exit("north", hallway)
        hallway.add_exit("south", cubicle)
        hallway.add_exit("east", break_room)
        hallway.add_exit("west", server_room)
        hallway.add_exit("north", lobby)
        break_room.add_exit("west", hallway)
        server_room.add_exit("east", hallway)

        # Lock the server room (requires keycard)
        server_room.locked = True
        server_room.lock_requires = "keycard"

        # Lock the lobby (requires master key)
        lobby.locked = True
        lobby.lock_requires = "master key"

        # Store rooms
        self.rooms = {
            "cubicle": cubicle,
            "hallway": hallway,
            "break_room": break_room,
            "server_room": server_room,
            "lobby": lobby,
        }

        # Set starting room
        self.player.current_room = cubicle

    def process_command(self, command):
        """Process a player command and return the result text."""
        command = command.strip().lower()
        parts = command.split(maxsplit=1)

        if not parts:
            return "Please enter a command."

        action = parts[0]
        arg = parts[1] if len(parts) > 1 else ""

        if action in ("go", "move", "walk"):
            return self.move(arg)
        elif action in ("take", "pick", "grab", "get"):
            return self.take(arg)
        elif action in ("look", "examine"):
            return self.look()
        elif action in ("inventory", "inv", "i"):
            return self.show_inventory()
        elif action in ("help", "h", "?"):
            return self.show_help()
        elif action in ("quit", "exit", "q"):
            self.running = False
            return "Thanks for playing!"
        else:
            return f"Unknown command: '{action}'. Type 'help' for available commands."

    def move(self, direction):
        """Move the player in a direction."""
        if not direction:
            return "Move where? Specify a direction (north, south, east, west)."

        room = self.player.current_room
        if direction not in room.exits:
            return f"You can't go {direction} from here."

        next_room = room.exits[direction]

        if next_room.locked:
            if self.player.has_item(next_room.lock_requires):
                next_room.locked = False
                self.player.current_room = next_room
                if next_room.name == "Lobby":
                    self.running = False
                    return (
                        "\nYou unlock the door and step into the lobby.\n"
                        "You push open the front door and escape the office!\n"
                        "\n*** CONGRATULATIONS! You escaped! ***\n"
                    )
                return f"You use the {next_room.lock_requires} to unlock the door.\n" + next_room.get_description()
            else:
                return f"The door is locked. You need a {next_room.lock_requires}."

        self.player.current_room = next_room
        return next_room.get_description()

    def take(self, item_name):
        """Pick up an item from the current room."""
        if not item_name:
            return "Take what? Specify an item name."

        # Strip "up" prefix so "pick up <item>" works correctly
        if item_name.startswith("up "):
            item_name = item_name[3:]

        room = self.player.current_room
        if item_name in room.items:
            room.remove_item(item_name)
            self.player.pick_up(item_name)
            return f"You picked up the {item_name}."
        else:
            return f"There's no '{item_name}' here."

    def look(self):
        """Look around the current room."""
        return self.player.current_room.get_description()

    def show_inventory(self):
        """Show the player's inventory."""
        if self.player.inventory:
            return "You are carrying: " + ", ".join(self.player.inventory)
        return "Your inventory is empty."

    def show_help(self):
        """Show available commands."""
        return (
            "Available commands:\n"
            "  go <direction>  - Move in a direction (north, south, east, west)\n"
            "  take <item>     - Pick up an item\n"
            "  look            - Look around the current room\n"
            "  inventory       - Check your inventory\n"
            "  help            - Show this help message\n"
            "  quit            - Quit the game"
        )

    def run(self):
        """Run the main game loop."""
        print("=== OFFICE ESCAPE ===")
        print("You fell asleep at your desk and woke up locked in the office.")
        print("Find your way out! Type 'help' for commands.\n")
        print(self.player.current_room.get_description())

        self.running = True
        while self.running:
            try:
                command = input("\n> ")
                result = self.process_command(command)
                print(result)
            except (EOFError, KeyboardInterrupt):
                print("\nThanks for playing!")
                break


if __name__ == "__main__":
    game = Game()
    game.run()
