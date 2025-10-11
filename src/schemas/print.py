from pydantic import BaseModel, Field
from enum import Enum


class SidesOption(str, Enum):
    ONE_SIDED = "one-sided"
    TWO_SIDED_LONG = "two-sided-long-edge"
    TWO_SIDED_SHORT = "two-sided-shot-edge"


class PrintOptions(BaseModel):
    copies: int = 1
    media: str = "A4"
    sides: SidesOption = SidesOption.ONE_SIDED
    fit_to_page: bool = True
    color: bool = False

    @property
    def cups_options(self) -> dict:
        """
        Convert Pydantic model fields into CUPS options dictionary.
        """
        return {
            "copies": str(self.copies),
            "media": self.media,
            "sides": self.sides,
            "fit-to-page": "true" if self.fit_to_page else "false",
            "print-color-mode": "color" if self.color else "monochrome",
        }
