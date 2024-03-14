from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.products import crud
from api_v1.products.schemas import Product, CreateProduct
from core.models import db_helper

router = APIRouter(tags=["Products"])


@router.get("/", response_model=list[Product])
async def get_products(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_all_products(session)


@router.post("/", response_model=Product)
async def create_product(
    product_in: CreateProduct,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    product = await crud.create_product(session=session, product_in=product_in)
    return product


@router.get("/{product_id}/", response_model=Product)
async def get_product(
    product_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    product = await crud.get_product_by_id(session=session, product_id=product_id)
    if product:
        return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"These product {product_id} is not found",
    )
