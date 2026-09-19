from pydantic import BaseModel, Field
import os

class Settings(BaseModel):
    aws_region: str = Field(default_factory=lambda: os.getenv("AWS_REGION", "ap-south-1"))
    dry_run: bool = Field(default_factory=lambda: os.getenv("DRY_RUN", "true").lower() == "true")
    max_scale_tasks: int = Field(default_factory=lambda: int(os.getenv("MAX_SCALE_TASKS", "10")))

settings = Settings()
