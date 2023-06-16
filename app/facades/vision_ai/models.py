from typing import List, Union
from pydantic import BaseModel, Field


class WebDetectionDto(BaseModel):
    best_guess_labels: str = Field("", description="推測されたラベル")

    full_math_url: List[str] = Field([], description="完全一致する画像が見つかった場合のURL(最大5件)")
    partial_math_urls: List[str] = Field([], description="部分一致する画像が見つかった場合のURL(最大5件)")
    similar_urls: List[str] = Field([], description="類似画像のURL(最大5件)")
