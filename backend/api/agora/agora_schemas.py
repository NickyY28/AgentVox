from pydantic import BaseModel, Field


class AgoraTokenRequest(BaseModel):
    channel_name: str = Field(min_length=1, max_length=100)
    uid: int = Field(gt=0)


class AgoraTokenResponse(BaseModel):
    token: str
    app_id: str
    channel_name: str
    uid: int
    expires_in: int
