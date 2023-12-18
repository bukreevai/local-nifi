from pydantic import BaseModel


class Status(BaseModel):
    """
    Return status of application
    """
    status: str
