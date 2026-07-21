from sqlalchemy.orm import Session


class BaseRepository:
    """Base class for all repositories."""

    def __init__(self, session: Session) -> None:
        self.session = session

