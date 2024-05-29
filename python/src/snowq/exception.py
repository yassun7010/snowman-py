from abc import abstractmethod


class SnowqException(Exception):
    @property
    @abstractmethod
    def message(self) -> str: ...

    def __str__(self) -> str:
        return self.message


class SnowqError(SnowqException):
    pass


class SnowqNotDataFrameAvailableError(SnowqError):
    @property
    def message(self) -> str:
        return "This method is not available when using DataFrame."
