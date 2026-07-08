from dataclasses import dataclass, field
from typing import List

@dataclass
class Task:
    description: str
    due_time: str
    is_completed: bool = False

    def mark_complete(self) -> None:
        """Marks the task as finished."""
        pass

@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Assigns a new task to the pet."""
        pass

    def get_pending_tasks(self) -> List[Task]:
        """Returns all tasks that are not yet completed."""
        pass

@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Adds a new pet to the owner's profile."""
        pass

    def get_all_pets(self) -> List[Pet]:
        """Returns all pets owned by this owner."""
        pass

@dataclass
class PawPalSystem:
    owners: List[Owner] = field(default_factory=list)

    def register_owner(self, owner: Owner) -> None:
        """Registers a new owner in the system."""
        pass

    def get_daily_schedule(self, owner: Owner) -> List[Task]:
        """Aggregates all pending tasks for all pets belonging to an owner."""
        pass