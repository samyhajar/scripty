# File: django_starter/utils/validators.py


class Validators:
    @staticmethod
    def is_valid_identifier(name):
        """Check if the given name is a valid Python identifier."""
        return name.isidentifier()
