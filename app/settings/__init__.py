import sys
from typing import Literal

from loguru import logger
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

from app.lib.convert import OutSightToAToBeConfig, ReferencePlane
from app.models.common import NonEmptyStr
from app.settings.consumer import ConsumerSettings, DisabledConsumerSettings
from app.settings.sender import SenderSettings

LogLevel = Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        toml_file="config.toml",
        env_prefix="SENSOR_DATA_CONVERSION_",
        env_nested_delimiter="__",
    )

    atb_realtime_topic: NonEmptyStr = ""
    atb_history_topic: NonEmptyStr = ""

    consumer: ConsumerSettings = DisabledConsumerSettings()
    sender: SenderSettings = SenderSettings()

    converter: OutSightToAToBeConfig = OutSightToAToBeConfig(
        outsight_reference_plane=ReferencePlane(
            origin=(0, 0), point_on_positive_horizontal_axis=(0, 1)
        ),
        atobe_reference_plane=ReferencePlane(
            origin=(0, 0), point_on_positive_horizontal_axis=(0, 1)
        ),
    )

    log_level: LogLevel = "INFO"

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            env_settings,
            TomlConfigSettingsSource(settings_cls),
        )


settings = Settings()

logger.remove()
logger.add(sys.stdout, level=settings.log_level)

logger.debug(settings)
