from typing import List, Optional

from pydantic import BaseModel, Field


class ExtractedFeatures(BaseModel):
    gr_liv_area: Optional[float] = Field(None, description="Above-ground living area in square feet")
    bedroom_abvgr: Optional[int] = Field(None, description="Number of bedrooms above ground")
    full_bath: Optional[int] = Field(None, description="Number of full bathrooms")
    neighborhood: Optional[str] = Field(None, description="Neighborhood name from Ames dataset")
    overall_qual: Optional[int] = Field(None, description="Overall material and finish quality, typically 1 to 10")
    garage_cars: Optional[int] = Field(None, description="Garage capacity in number of cars")
    year_built: Optional[int] = Field(None, description="Original construction year")
    lot_area: Optional[float] = Field(None, description="Lot size in square feet")
    house_style: Optional[str] = Field(None, description="House style such as 1Story, 2Story, 1.5Fin")
    totrms_abvgrd: Optional[int] = Field(None, description="Total rooms above ground")

    extracted_fields: List[str]
    missing_fields: List[str]
    is_complete: bool
