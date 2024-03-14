from sqlalchemy import select, Result, desc
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.products.schemas import CreateProduct
from core.models import Product


async def get_all_products(session: AsyncSession) -> list[Product]:
    query = select(Product).order_by(desc(Product.id))
    result: Result = await session.execute(query)
    products = result.scalars().all()
    return list(products)


async def get_product_by_id(session: AsyncSession, product_id: int) -> Product | None:
    product = await session.get(Product, product_id)
    return product


async def create_product(session: AsyncSession, product_in: CreateProduct) -> Product:
    product = Product(**product_in.model_dump())
    session.add(product)
    await session.commit()
    return product
