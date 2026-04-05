from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime

from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, create_engine
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

engine = create_engine("jdbc:postgresql://94.156.102.232:5432/exchange", echo=True)

class Base(DeclarativeBase):
    pass

Base.metadata.create_all(engine)

class DepoLimit(Base):
    __tablename__ = 'portfolio'

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(15))
    subaccid: Mapped[str] = mapped_column(String(36))
    agreementid: Mapped[str] = mapped_column(String(36))
    account: Mapped[str] = mapped_column(String(10))
    exchange: Mapped[str] = mapped_column(String(30))
    ticker: Mapped[str] = mapped_column(String(30))
    displayName: Mapped[str] = mapped_column(String(255))
    baseAssetTicker: Mapped[str] = mapped_column(String(255))
    currency: Mapped[str] = mapped_column(String(3))
    upperType: Mapped[str] = mapped_column(String(9))
    instrumentType: Mapped[str] = mapped_column(String(19))
    term: Mapped[str] = mapped_column(String(4))
    quantity: Mapped[Numeric] = mapped_column(Numeric(precision=20, scale=2))
    locked: Mapped[Numeric] = mapped_column(Numeric(precision=20, scale=2))
    balancePrice: Mapped[Numeric] = mapped_column(Numeric(precision=20, scale=4))
    currentPrice: Mapped[Numeric] = mapped_column(Numeric(precision=20, scale=4))
    balanceValue: Mapped[Numeric] = mapped_column(Numeric(precision=20, scale=4))
    balanceValueRub: Mapped[Numeric] = mapped_column(Numeric(precision=20, scale=4))
    balanceValueUsd: Mapped[Numeric] = mapped_column(Numeric(precision=20, scale=4))
    balanceValueEur: Mapped[Numeric] = mapped_column(Numeric(precision=20, scale=4))
    cuurentValue: Mapped[Numeric] = mapped_column(Numeric(precision=20, scale=4))
    cuurentValueRub: Mapped[Numeric] = mapped_column(Numeric(precision=20, scale=4))
    cuurentValueUsd: Mapped[Numeric] = mapped_column(Numeric(precision=20, scale=4))
    currentValueEur: Mapped[Numeric] = mapped_column(Numeric(precision=20, scale=4))
    unrealizedPL: Mapped[Numeric] = mapped_column(Numeric(precision=20, scale=4))
    unrealizedPercentPL: Mapped[Numeric] = mapped_column(Numeric(precision=20, scale=4))
    dailyPL: Mapped[Numeric] = mapped_column(Numeric(precision=20, scale=4))
    dailyPercentPL: Mapped[Numeric] = mapped_column(Numeric(precision=20, scale=4))
    portfolioShare: Mapped[Numeric] = mapped_column(Numeric(precision=20, scale=4))
    scale: Mapped[int] = mapped_column(Integer(32))
# minimumStep -> 0.5
# board -> TQBR
# priceUnit ->
# faceValue -> 1164.26
# accruedIncome -> 0.0
# logoLink -> https://mybroker.storage.bcs.ru/FinInstrumentLogo/RU000A108X38.png
# isBlocked -> False
# isBlockedTradeAccount -> False
# lockedForFutures -> 0.0
# ratioQuantity -> 0.0
# expireDate ->


