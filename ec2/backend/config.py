import os
from typing import Optional
from dataclasses import dataclass

@dataclass
class DatabaseConfig:
    host: str
    user: str
    password: str
    database: str
    charset: str = "utf8mb4"

    @classmethod
    def from_env(cls) -> "DatabaseConfig":
        return cls(
            host=os.getenv("DB_HOST", "db"),
            user=os.getenv("DB_USER", "user"),
            password=os.getenv("DB_PASSWORD", "pass"),
            database=os.getenv("DB_NAME", "attendance"),
        )

@dataclass
class AppConfig:
    database: DatabaseConfig
    #cors_origins: list[str]
    
    @classmethod
    def from_env(cls) -> "AppConfig":
        return cls(
            database=DatabaseConfig.from_env(),
            # cors_origins=["http://localhost:3000", "http://localhost:3001"],
        )