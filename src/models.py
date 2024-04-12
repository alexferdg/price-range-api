# Models for the API requests and responses
from pydantic import BaseModel, Field, field_validator
from typing import Optional

# Request model
class MobileCharacteristics(BaseModel):
    battery_power: int = Field(2400, description="Battery power in mAh")
    blue: Optional[int] = Field(0, description="Bluetooth support: 1 if supported, 0 otherwise")
    clock_speed: float = Field(2.2, description="Processor clock speed in GHz")
    dual_sim: Optional[int] = Field(0, description="Dual SIM support: 1 if supported, 0 otherwise")
    fc: Optional[int] = Field(1, description="Front camera megapixels")
    four_g: Optional[int] = Field(0, description="4G support: 1 if supported, 0 otherwise")
    int_memory: int = Field(7, description="Internal memory in GB")
    m_dep: float = Field(0.6, description="Mobile depth in cm")
    mobile_wt: int = Field(188, description="Mobile weight in grams")
    n_cores: int = Field(2, description="Number of CPU cores")
    pc: Optional[int] = Field(2, description="Primary camera megapixels")
    px_height: int = Field(20, description="Pixel resolution height")
    px_width: int = Field(756, description="Pixel resolution width")
    ram: int = Field(2549, description="RAM in MB")
    sc_h: int = Field(9, description="Screen height in cm")
    sc_w: int = Field(7, description="Screen width in cm")
    talk_time: int = Field(19, description="Talk time in hours")
    three_g: Optional[int] = Field(0, description="3G support: 1 if supported, 0 otherwise")
    touch_screen: Optional[int] = Field(0, description="Touch screen: 1 if touch enabled, 0 otherwise")
    wifi: Optional[int] = Field(1, description="WiFi: 1 if supported, 0 otherwise")

    @field_validator("clock_speed", mode="before")
    @classmethod
    def clock_speed_must_be_valid(cls, v):
        if v <= 0:
            raise ValueError("Clock speed must be a positive value")
        return v

    class Config:
        schema_extra = {
            "example": {
                "battery_power": 3000,
                "blue": 1,
                "clock_speed": 2.5,
                "dual_sim": 1,
                "fc": 12,
                "four_g": 1,
                "int_memory": 64,
                "m_dep": 0.8,
                "mobile_wt": 200,
                "n_cores": 8,
                "pc": 16,
                "px_height": 1080,
                "px_width": 1920,
                "ram": 4096,
                "sc_h": 15,
                "sc_w": 10,
                "talk_time": 24,
                "three_g": 1,
                "touch_screen": 1,
                "wifi": 1
            }
        }

# Response model
class PricePredictionResponse(BaseModel):
    price_range: str
    model_used: str