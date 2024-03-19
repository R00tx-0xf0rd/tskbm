from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    __abstract__ = True
    # __table_args__ = {"extend_existing": True}
    #
    # def __tablename__(cls) -> str:
    #     return f"{cls.__name__.lower()}s"
    # id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    tabnum: Mapped[int] = mapped_column()
    column: Mapped[int]
    lname: Mapped[str]
    fname: Mapped[str]
    pname: Mapped[str]
    last_checkout: Mapped[datetime]
    watch_id: Mapped[int] = mapped_column(ForeignKey("watches.id"))
    watch: Mapped["Watch"] = relationship(lazy="selectin", uselist=False)
    times: Mapped[list["Times"]] = relationship(lazy="selectin", uselist=True)


class Watch(Base):
    __tablename__ = "watches"
    id: Mapped[int] = mapped_column(primary_key=True)
    ser_num: Mapped[str]
    # user: Mapped[User] = relationship(uselist=False)
    # user: Mapped[int] = mapped_column(ForeignKey("users.id"))


class Times(Base):
    __tablename__ = "times"
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    checkout_time: Mapped[datetime]
