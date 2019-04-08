"""Reports exceptions."""


class ReportsError(Exception):
    """Generic reports error."""

    def __init__(self, description) -> None:
        super().__init__(description)
        self.description = description


class TogglError(ReportsError):
    """Toggl API error."""


class SendGridError(ReportsError):
    """SendGrid API error."""
