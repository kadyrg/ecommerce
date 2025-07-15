from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, UploadFile, Request
from starlette.responses import FileResponse
from app.models import Products, Category
from .schemas import ProductsSchema, AddProductsSchema
from app.core import settings
from pathlib import  Path
import uuid

async def get_product(request: Request, product_id: int, session: AsyncSession) -> ProductsSchema:
    result = await session.execute(
        select(Products).where(Products.id == product_id)
    )

    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    image_url = f"{request.base_url}media/{product.image}"

    return ProductsSchema(
        id = product.id,
        name = product.name,
        description = product.description,
        price = product.price,
        image = image_url
    )


async def get_products(request: Request, category: str | None, session: AsyncSession) -> list[ProductsSchema]:

    stmt = select(Products)
    if category:
        stmt = stmt.where(Products.category.has(name=category))

    result = await session.execute(stmt)

    products = result.scalars().all()

    return [ProductsSchema.model_validate(product) for product in products]

async def add_product(name: str, description: str, image: UploadFile, price: float, category_name: str, session: AsyncSession) -> ProductsSchema:
    result = await session.execute(
        select(Category).where(
            Category.name == category_name
        )
    )

    category = result.scalar_one_or_none()

    if category is None:
        category = Category(name=category_name)
        session.add(category)

    ext = Path(image.filename).suffix
    filename = f"{uuid.uuid4()}{ext}"
    file_path = settings.media_files_path / filename
    with open(file_path, "wb") as f:
        content = await image.read()
        f.write(content)

    product = Products(
        name=name,
        description=description,
        image=filename,
        price=price,
        category_id=category.id
    )
    session.add(product)
    await session.commit()
    return ProductsSchema.model_validate(product)


async def get_product_image(product_image: str, session: AsyncSession) -> FileResponse:
    image_path = settings.media_files_path / product_image

    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(path=image_path, media_type="image/jpeg", filename=product_image)
