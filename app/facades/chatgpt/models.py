from pydantic import BaseModel, Field


class CreateChatTitle(BaseModel):
    title: str = Field("", description="タイトル")
