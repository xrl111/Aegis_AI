"""Aegis AI — Custom Exceptions.

Mọi error handling trong project dùng các exception này.
KHÔNG dùng bare except hoặc return giá trị mặc định khi thiếu data.
"""


class AegisError(Exception):
    """Base exception for all Aegis AI errors."""


class InsufficientDataError(AegisError):
    """Raised when there is not enough data to compute a signal or baseline.

    Hệ thống KHÔNG suy đoán khi thiếu dữ liệu — raise error này
    và để caller xử lý (hiển thị "Chưa đủ dữ liệu").
    """

    def __init__(
        self,
        student_id: str,
        signal: str,
        available: int,
        required: int,
    ) -> None:
        self.student_id = student_id
        self.signal = signal
        self.available = available
        self.required = required
        super().__init__(
            f"Student {student_id}: signal '{signal}' cần ít nhất {required} "
            f"data points, hiện có {available}."
        )


class ValidationError(AegisError):
    """Raised when input data fails validation checks."""

    def __init__(self, field: str, value: object, reason: str) -> None:
        self.field = field
        self.value = value
        self.reason = reason
        super().__init__(f"Validation failed — {field}={value!r}: {reason}")


class ConfigError(AegisError):
    """Raised when configuration is missing or invalid."""
