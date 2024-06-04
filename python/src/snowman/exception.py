from abc import abstractmethod


class snowmanException(Exception):
    @property
    @abstractmethod
    def message(self) -> str: ...

    def __str__(self) -> str:
        return self.message


class snowmanError(snowmanException):
    pass


class snowmanNotDataFrameAvailableError(snowmanError):
    @property
    def message(self) -> str:
        return "This method is not available when using DataFrame."
