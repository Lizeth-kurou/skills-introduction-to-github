"""
Student Activity Registration System

A module for managing student registrations for school activities.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class StudentRegistration:
    """Represents a student registration for an activity."""
    name: str
    email: str
    activity: str

    def __str__(self) -> str:
        return f"{self.name} ({self.email}) - {self.activity}"


class StudentActivityRegistry:
    """Manages student registrations for school activities."""

    AVAILABLE_ACTIVITIES = [
        "Chess Club",
        "Science Fair",
        "Drama Club",
        "Sports Team",
        "Music Band",
        "Art Workshop",
    ]

    def __init__(self) -> None:
        """Initialize an empty registry."""
        self._registrations: list[StudentRegistration] = []

    def register_student(
        self, name: str, email: str, activity: str
    ) -> StudentRegistration:
        """
        Register a student for an activity.

        Args:
            name: The student's full name
            email: The student's email address
            activity: The activity to register for

        Returns:
            The created StudentRegistration object

        Raises:
            ValueError: If the activity is not in the list of available activities
            ValueError: If the student is already registered for this activity
        """
        if not name or not name.strip():
            raise ValueError("Student name cannot be empty")

        if not email or not email.strip():
            raise ValueError("Student email cannot be empty")

        if activity not in self.AVAILABLE_ACTIVITIES:
            raise ValueError(
                f"Invalid activity: {activity}. "
                f"Available activities: {', '.join(self.AVAILABLE_ACTIVITIES)}"
            )

        # Check for duplicate registration
        for reg in self._registrations:
            if reg.email == email and reg.activity == activity:
                raise ValueError(
                    f"Student with email {email} is already registered for {activity}"
                )

        registration = StudentRegistration(
            name=name.strip(), email=email.strip(), activity=activity
        )
        self._registrations.append(registration)
        return registration

    def get_all_registrations(self) -> list[StudentRegistration]:
        """
        Get all current registrations.

        Returns:
            A list of all StudentRegistration objects
        """
        return self._registrations.copy()

    def search_student(self, query: str) -> list[StudentRegistration]:
        """
        Search for students by name or email.

        Args:
            query: The search query (case-insensitive)

        Returns:
            A list of matching StudentRegistration objects
        """
        query_lower = query.lower()
        return [
            reg
            for reg in self._registrations
            if query_lower in reg.name.lower() or query_lower in reg.email.lower()
        ]

    def get_registrations_by_activity(
        self, activity: str
    ) -> list[StudentRegistration]:
        """
        Get all registrations for a specific activity.

        Args:
            activity: The activity name

        Returns:
            A list of StudentRegistration objects for that activity
        """
        return [reg for reg in self._registrations if reg.activity == activity]

    def remove_registration(self, email: str, activity: str) -> bool:
        """
        Remove a student's registration for an activity.

        Args:
            email: The student's email address
            activity: The activity to unregister from

        Returns:
            True if the registration was removed, False if not found
        """
        for i, reg in enumerate(self._registrations):
            if reg.email == email and reg.activity == activity:
                self._registrations.pop(i)
                return True
        return False

    def get_student_activities(self, email: str) -> list[str]:
        """
        Get all activities a student is registered for.

        Args:
            email: The student's email address

        Returns:
            A list of activity names
        """
        return [reg.activity for reg in self._registrations if reg.email == email]


def main() -> None:
    """Interactive command-line interface for the registration system."""
    registry = StudentActivityRegistry()

    print("Welcome to the Student Activity Registration System!")
    print("=" * 50)

    while True:
        print("\nOptions:")
        print("1. Register a student")
        print("2. View all registrations")
        print("3. Search for a student")
        print("4. View registrations by activity")
        print("5. Remove a registration")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "1":
            print("\nAvailable activities:")
            for i, activity in enumerate(registry.AVAILABLE_ACTIVITIES, 1):
                print(f"  {i}. {activity}")

            name = input("Enter student name: ").strip()
            email = input("Enter student email: ").strip()
            activity_num = input("Enter activity number: ").strip()

            try:
                activity_idx = int(activity_num) - 1
                if 0 <= activity_idx < len(registry.AVAILABLE_ACTIVITIES):
                    activity = registry.AVAILABLE_ACTIVITIES[activity_idx]
                    reg = registry.register_student(name, email, activity)
                    print(f"\nSuccess! Registered: {reg}")
                else:
                    print("\nInvalid activity number.")
            except ValueError as e:
                print(f"\nError: {e}")

        elif choice == "2":
            registrations = registry.get_all_registrations()
            if registrations:
                print("\nAll registrations:")
                for reg in registrations:
                    print(f"  - {reg}")
            else:
                print("\nNo registrations yet.")

        elif choice == "3":
            query = input("Enter search query (name or email): ").strip()
            results = registry.search_student(query)
            if results:
                print(f"\nFound {len(results)} result(s):")
                for reg in results:
                    print(f"  - {reg}")
            else:
                print("\nNo matching registrations found.")

        elif choice == "4":
            print("\nAvailable activities:")
            for i, activity in enumerate(registry.AVAILABLE_ACTIVITIES, 1):
                print(f"  {i}. {activity}")

            activity_num = input("Enter activity number: ").strip()
            try:
                activity_idx = int(activity_num) - 1
                if 0 <= activity_idx < len(registry.AVAILABLE_ACTIVITIES):
                    activity = registry.AVAILABLE_ACTIVITIES[activity_idx]
                    results = registry.get_registrations_by_activity(activity)
                    if results:
                        print(f"\nRegistrations for {activity}:")
                        for reg in results:
                            print(f"  - {reg.name} ({reg.email})")
                    else:
                        print(f"\nNo registrations for {activity}.")
                else:
                    print("\nInvalid activity number.")
            except ValueError:
                print("\nPlease enter a valid number.")

        elif choice == "5":
            email = input("Enter student email: ").strip()
            print("\nAvailable activities:")
            for i, activity in enumerate(registry.AVAILABLE_ACTIVITIES, 1):
                print(f"  {i}. {activity}")

            activity_num = input("Enter activity number to remove: ").strip()
            try:
                activity_idx = int(activity_num) - 1
                if 0 <= activity_idx < len(registry.AVAILABLE_ACTIVITIES):
                    activity = registry.AVAILABLE_ACTIVITIES[activity_idx]
                    if registry.remove_registration(email, activity):
                        print(f"\nRemoved registration for {email} from {activity}.")
                    else:
                        print("\nRegistration not found.")
                else:
                    print("\nInvalid activity number.")
            except ValueError:
                print("\nPlease enter a valid number.")

        elif choice == "6":
            print("\nThank you for using the Student Activity Registration System!")
            break

        else:
            print("\nInvalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
