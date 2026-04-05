from sqlalchemy import MetaData, create_engine 
from sqlalchemy import String, Integer, Column, Text, DateTime, Boolean, Numeric,Float,  text
from sqlalchemy import Table, ForeignKey
from sqlalchemy import insert, update, delete

from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")


engine = create_engine(f"{DB_URL}", echo=True)

metadata_obj = MetaData()

test_table = Table(
    "test_table",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("username", String(16), nullable=False),
    Column("regdate", DateTime, server_default=text("NOW()"))
)

portfolio = Table(
    "portfolio",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True, nullable=False),
    Column("type", String(15), nullable=False),                        # type -> depoLimit -> <class 'str'>
    Column("subAccountId", String(36), nullable=False),                    # subAccountId -> 7723e0e4-6254-4a26-a16a-467e1fc574cb -> <class 'str'>
    Column("agreementId", String(36), nullable=False),                  # agreementId -> 3d2ad6ef-fadb-4b2b-b04a-7b364b798c26 -> <class 'str'>
    Column("account", String(10), nullable=False),                     # account -> 3105694/24 -> <class 'str'>
    Column("exchange", String(255), nullable=False),                   # exchange -> MOEX -> <class 'str'>
    Column("ticker", String(255), nullable=False),                     # ticker -> X5 -> <class 'str'>
    Column("displayName", String(255), nullable=False),                # displayName -> КЦ ИКС 5 -> <class 'str'>
    Column("baseAssetTicker", String(255), nullable=True),             # baseAssetTicker ->  -> <class 'str'>
    Column("currency", String(3), nullable=False),                     # currency -> RUB -> <class 'str'>
    Column("upperType", String(255), nullable=False),                  # upperType -> RUSSIA -> <class 'str'>
    Column("instrumentType", String(255), nullable=False),              # instrumentType -> STOCK -> <class 'str'>
    Column("term", String(4), nullable=False),                         # term -> T365 -> <class 'str'>
    Column("quantity", Float(precision=4), nullable=False),            # quantity -> 2.0 -> <class 'float'>
    Column("locked", Float(precision=4), nullable=False),              # locked -> 0.0 -> <class 'float'>
    Column("balancePrice", Float(precision=4), nullable=False),        # balancePrice -> 2465.75 -> <class 'float'>
    Column("currentPrice", Float(precision=4), nullable=False),        # currentPrice -> 2427.0 -> <class 'float'>
    Column("balanceValue", Float(precision=4), nullable=False),        # balanceValue -> 4931.5 -> <class 'float'>
    Column("balanceValueRub", Float(precision=4), nullable=False),     # balanceValueRub -> 4931.5 -> <class 'float'>
    Column("balanceValueUsd", Float(precision=4), nullable=False),     # balanceValueUsd -> 62.8906 -> <class 'float'>
    Column("balanceValueEur", Float(precision=4), nullable=False),     # balanceValueEur -> 54.577 -> <class 'float'>
    Column("currentValue", Float(precision=4), nullable=False),        # currentValue -> 4854.0 -> <class 'float'>
    Column("currentValueRub", Float(precision=4), nullable=False),     # currentValueRub -> 4854.0 -> <class 'float'>
    Column("currentValueUsd", Float(precision=4), nullable=False),     # currentValueUsd -> 61.9022 -> <class 'float'>
    Column("currentValueEur", Float(precision=4), nullable=False),     # currentValueEur -> 53.7194 -> <class 'float'>
    Column("unrealizedPL", Float(precision=4), nullable=False),        # unrealizedPL -> -77.5 -> <class 'float'>
    Column("unrealizedPercentPL", Float(precision=4), nullable=False), # unrealizedPercentPL -> -1.5715 -> <class 'float'>
    Column("dailyPL", Float(precision=4), nullable=False),             # dailyPL -> 0.0 -> <class 'float'>
    Column("dailyPercentPL", Float(precision=4), nullable=False),      # dailyPercentPL -> 0.0 -> <class 'float'>
    Column("portfolioShare", Float(precision=4), nullable=False),      # portfolioShare -> 0.0 -> <class 'float'>
    Column("scale", Integer, nullable=False),                       # scale -> 1 -> <class 'int'>
    Column("minimumStep", Float(precision=4), nullable=False),         # minimumStep -> 0.5 -> <class 'float'>
    Column("board", String(10), nullable=True),                        # board -> TQBR -> <class 'str'>
    Column("priceUnit", String(255), nullable=True),                   # priceUnit ->  -> <class 'str'>
    Column("faceValue", Float(precision=4), nullable=False),           # faceValue -> 1164.26 -> <class 'float'>
    Column("accruedIncome", Float(precision=4), nullable=False),       # accruedIncome -> 0.0 -> <class 'float'>
    Column("isBlocked", Boolean, nullable=True),                     # isBlocked -> False -> <class 'bool'>
    Column("isBlockedTradeAccount", Boolean, nullable=True),          # isBlockedTradeAccount -> False -> <class 'bool'>
    Column("lockedForFutures", Float(precision=4), nullable=False),    # lockedForFutures -> 0.0 -> <class 'float'>
    Column("ratioQuantity", Float(precision=4), nullable=False),       # ratioQuantity -> 0.0 -> <class 'float'>
    Column("expireDate", String(255), nullable=True),                 # expireDate ->  -> <class 'str'>
    Column("auditDateTime", DateTime, server_default=text("(CURRENT_TIMESTAMP AT TIME ZONE 'Europe/Moscow')"))
)

instruments = Table(
    "instruments",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True, nullable=False),
    Column("shortName", String(255)),
    Column("displayName", String(255)),
    Column("isin", String(255)),
    Column("issuerName", String(255)),
    Column("auditDateTime", DateTime, server_default=text("(CURRENT_TIMESTAMP AT TIME ZONE 'Europe/Moscow')"))
)


metadata_obj.create_all(engine)