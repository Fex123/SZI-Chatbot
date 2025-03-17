
"""
ValidationService
Class responsible for validating user input data
"""
class ValidationService:
    @staticmethod
    def validate_username(value: str) -> str:
        if len(value) < 3 or len(value) > 50:
            raise ValueError('Username must be between 3 and 50 characters')
        return value

    @staticmethod
    def validate_password(value: str) -> str:
        if len(value) < 6:
            raise ValueError('Password must be at least 6 characters')
        return value

    @staticmethod
    def get_model_config():
        return {
            'str_min_length': 3,
            'str_max_length': 50,
            'password_min_length': 6
        }
