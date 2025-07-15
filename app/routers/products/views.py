from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Path, Query, Form, File, UploadFile, Request

from .schemas import ProductsSchema, AddProductsSchema
from app.db import get_db_session
from . import crud

router = APIRouter()


@router.post(
    path="/products",
    summary="Add product",
    description="Add product",
    response_model=ProductsSchema
)
async def add_product(
        name: Annotated[str, Form()],
        description: Annotated[str, Form()],
        image: Annotated[UploadFile, File()],
        price: Annotated[float, Form()],
        category_name: Annotated[str, Form()],
        session: AsyncSession = Depends(get_db_session)
):
    return await crud.add_product(name, description, image, price, category_name, session)


@router.get(
    path="/products",
    summary="Get Filtered products by category",
    description="Get Filtered products by category",
    response_model=list[ProductsSchema]
)
async def get_products(
        request: Request,
        category: Annotated[str | None, Query()] = None,
        session: AsyncSession = Depends(get_db_session)
):
    return await crud.get_products(request, category, session)



@router.get(
    path="/products{product_id}",
    summary="Get Product by ID",
    description="Get Product by ID",
    response_model=ProductsSchema
)
async def get_product(
        request: Request,
        product_id: Annotated[int, Path(ge=1)],
        session: AsyncSession = Depends(get_db_session)
):
    return await crud.get_product(request, product_id, session)


@router.get(
    path="/media/{product_image}",
    summary="Get Image",
    description="Get Image",
    response_model=ProductsSchema
)
async def get_product_image(
        product_image: Annotated[str, Path()],
        session: AsyncSession = Depends(get_db_session)
):
    return await crud.get_product_image(product_image, session)




