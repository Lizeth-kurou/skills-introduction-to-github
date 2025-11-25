"""
Tests for the Student Activity Registration System.
"""

import pytest

from registration import StudentActivityRegistry, StudentRegistration


class TestStudentRegistration:
    """Tests for the StudentRegistration dataclass."""

    def test_str_representation(self) -> None:
        """Test string representation of a registration."""
        reg = StudentRegistration(
            name="John Doe", email="john@example.com", activity="Chess Club"
        )
        assert str(reg) == "John Doe (john@example.com) - Chess Club"


class TestStudentActivityRegistry:
    """Tests for the StudentActivityRegistry class."""

    def test_register_student_success(self) -> None:
        """Test successful student registration."""
        registry = StudentActivityRegistry()
        reg = registry.register_student(
            "Jane Doe", "jane@example.com", "Chess Club"
        )

        assert reg.name == "Jane Doe"
        assert reg.email == "jane@example.com"
        assert reg.activity == "Chess Club"

    def test_register_student_trims_whitespace(self) -> None:
        """Test that registration trims whitespace from name and email."""
        registry = StudentActivityRegistry()
        reg = registry.register_student(
            "  Jane Doe  ", "  jane@example.com  ", "Chess Club"
        )

        assert reg.name == "Jane Doe"
        assert reg.email == "jane@example.com"

    def test_register_student_invalid_activity(self) -> None:
        """Test that registering for an invalid activity raises an error."""
        registry = StudentActivityRegistry()

        with pytest.raises(ValueError) as exc_info:
            registry.register_student(
                "Jane Doe", "jane@example.com", "Invalid Activity"
            )

        assert "Invalid activity" in str(exc_info.value)

    def test_register_student_empty_name(self) -> None:
        """Test that empty name raises an error."""
        registry = StudentActivityRegistry()

        with pytest.raises(ValueError) as exc_info:
            registry.register_student("", "jane@example.com", "Chess Club")

        assert "name cannot be empty" in str(exc_info.value)

    def test_register_student_empty_email(self) -> None:
        """Test that empty email raises an error."""
        registry = StudentActivityRegistry()

        with pytest.raises(ValueError) as exc_info:
            registry.register_student("Jane Doe", "", "Chess Club")

        assert "email cannot be empty" in str(exc_info.value)

    def test_register_student_duplicate(self) -> None:
        """Test that duplicate registration raises an error."""
        registry = StudentActivityRegistry()
        registry.register_student("Jane Doe", "jane@example.com", "Chess Club")

        with pytest.raises(ValueError) as exc_info:
            registry.register_student("Jane Doe", "jane@example.com", "Chess Club")

        assert "already registered" in str(exc_info.value)

    def test_register_student_same_email_different_activity(self) -> None:
        """Test that a student can register for multiple activities."""
        registry = StudentActivityRegistry()
        registry.register_student("Jane Doe", "jane@example.com", "Chess Club")
        reg2 = registry.register_student(
            "Jane Doe", "jane@example.com", "Science Fair"
        )

        assert reg2.activity == "Science Fair"
        assert len(registry.get_all_registrations()) == 2

    def test_get_all_registrations(self) -> None:
        """Test getting all registrations."""
        registry = StudentActivityRegistry()
        registry.register_student("Jane Doe", "jane@example.com", "Chess Club")
        registry.register_student("John Doe", "john@example.com", "Drama Club")

        registrations = registry.get_all_registrations()

        assert len(registrations) == 2

    def test_get_all_registrations_returns_copy(self) -> None:
        """Test that get_all_registrations returns a copy."""
        registry = StudentActivityRegistry()
        registry.register_student("Jane Doe", "jane@example.com", "Chess Club")

        registrations = registry.get_all_registrations()
        registrations.clear()

        assert len(registry.get_all_registrations()) == 1

    def test_search_student_by_name(self) -> None:
        """Test searching for a student by name."""
        registry = StudentActivityRegistry()
        registry.register_student("Jane Doe", "jane@example.com", "Chess Club")
        registry.register_student("John Smith", "john@example.com", "Drama Club")

        results = registry.search_student("jane")

        assert len(results) == 1
        assert results[0].name == "Jane Doe"

    def test_search_student_by_email(self) -> None:
        """Test searching for a student by email."""
        registry = StudentActivityRegistry()
        registry.register_student("Jane Doe", "jane@example.com", "Chess Club")
        registry.register_student("John Smith", "john@example.com", "Drama Club")

        results = registry.search_student("john@")

        assert len(results) == 1
        assert results[0].email == "john@example.com"

    def test_search_student_case_insensitive(self) -> None:
        """Test that search is case-insensitive."""
        registry = StudentActivityRegistry()
        registry.register_student("Jane Doe", "jane@example.com", "Chess Club")

        results = registry.search_student("JANE")

        assert len(results) == 1

    def test_search_student_no_results(self) -> None:
        """Test searching with no matching results."""
        registry = StudentActivityRegistry()
        registry.register_student("Jane Doe", "jane@example.com", "Chess Club")

        results = registry.search_student("nonexistent")

        assert len(results) == 0

    def test_get_registrations_by_activity(self) -> None:
        """Test getting registrations by activity."""
        registry = StudentActivityRegistry()
        registry.register_student("Jane Doe", "jane@example.com", "Chess Club")
        registry.register_student("John Smith", "john@example.com", "Chess Club")
        registry.register_student("Bob Brown", "bob@example.com", "Drama Club")

        results = registry.get_registrations_by_activity("Chess Club")

        assert len(results) == 2

    def test_remove_registration_success(self) -> None:
        """Test successful registration removal."""
        registry = StudentActivityRegistry()
        registry.register_student("Jane Doe", "jane@example.com", "Chess Club")

        result = registry.remove_registration("jane@example.com", "Chess Club")

        assert result is True
        assert len(registry.get_all_registrations()) == 0

    def test_remove_registration_not_found(self) -> None:
        """Test removal when registration doesn't exist."""
        registry = StudentActivityRegistry()

        result = registry.remove_registration("jane@example.com", "Chess Club")

        assert result is False

    def test_get_student_activities(self) -> None:
        """Test getting all activities for a student."""
        registry = StudentActivityRegistry()
        registry.register_student("Jane Doe", "jane@example.com", "Chess Club")
        registry.register_student("Jane Doe", "jane@example.com", "Drama Club")
        registry.register_student("John Doe", "john@example.com", "Sports Team")

        activities = registry.get_student_activities("jane@example.com")

        assert len(activities) == 2
        assert "Chess Club" in activities
        assert "Drama Club" in activities

    def test_available_activities(self) -> None:
        """Test that available activities are defined."""
        assert len(StudentActivityRegistry.AVAILABLE_ACTIVITIES) > 0
        assert "Chess Club" in StudentActivityRegistry.AVAILABLE_ACTIVITIES
