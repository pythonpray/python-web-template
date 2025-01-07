from contextvars import ContextVar
from sqlalchemy.orm import Session

from src.infra.seedwork.repo.session import get_session


class RequestContext:
    _db_session: ContextVar[Session] = ContextVar("_db_session", default=None)
    _is_in_transaction: ContextVar[bool] = ContextVar(
        "_is_in_transaction", default=False
    )
    _user_session: ContextVar = ContextVar("_user_session", default={})

    @property
    def db_session(self) -> ContextVar[Session]:
        """Get current db session as ContextVar"""
        return self._db_session

    @property
    def is_in_transaction(self):
        return self._is_in_transaction.get()

    @is_in_transaction.setter
    def is_in_transaction(self, value):
        self._is_in_transaction.set(value)

    @property
    def user_session(self):
        return self._user_session.get()

    @user_session.setter
    def user_session(self, session_info):
        self._user_session.set(session_info)

    def begin_request(self):
        session = get_session()
        session.begin()
        self._db_session.set(session)

    def end_request(self, commit=False):
        session = self.db_session.get()
        if session:
            if commit:
                session.commit()
            else:
                session.rollback()

    def __enter__(self):
        self.begin_request()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        commit = exc_type is None
        self.end_request(commit=commit)


request_context = RequestContext()
