class ModelConvergenceError(Exception):
    def __init__(message: str, value: str) -> None:
        super().__init__(message)
        self.message = message
        self.value = value

    def __str__(self) -> str:
        return f"{self.message}, (value: {self.value})"


class InvalidParameterError(Exception):
    def __init__(message: str, value: str) -> None:
        super().__init__(message)
        self.message = message
        self.value = value
    
    def __str__(self) -> str:
        return f"{self.message}, (value: {self.value})"


class FellerConditionViolation(Exception):
    def __init__(message: str, value: str) -> None:
        super().__init__(message)
        self.message = message
        self.value = value
    
    def __str__(self) -> str:
        return f"{self.message}, (value: {self.value})"

