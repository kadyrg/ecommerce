from pydantic import BaseModel, ConfigDict


class ProductsSchema(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image: str

    model_config = ConfigDict(from_attributes=True)

class AddProductsSchema(ProductsSchema):
    category: str

