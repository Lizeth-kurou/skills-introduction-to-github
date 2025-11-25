# Student Activity Registration System

A simple system for managing student registrations for school activities.

## Features

- Register students for activities
- View all registered students
- Search for student registrations
- Remove student registrations

## Usage

### Running the Application

```bash
python registration.py
```

### API

```python
from registration import StudentActivityRegistry

# Create a registry
registry = StudentActivityRegistry()

# Register a student
registry.register_student("John Doe", "john@example.com", "Chess Club")

# Get all registrations
all_registrations = registry.get_all_registrations()

# Search for a student
results = registry.search_student("John")

# Remove a registration
registry.remove_registration("john@example.com", "Chess Club")
```

## Available Activities

- Chess Club
- Science Fair
- Drama Club
- Sports Team
- Music Band
- Art Workshop

## Contributing

Feel free to contribute by opening a pull request!
