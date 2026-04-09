from sqlalchemy import MetaData, create_engine, text
from sqlalchemy import String, Integer, Column, Text, DateTime, Date, Boolean, Numeric,Float, BigInteger
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
    Column("ticker", String(255), nullable=False),
    Column("shortName", String(255), nullable=True),
    Column("displayName", String(255), nullable=True),
    Column("type", String(255), nullable=True),
    Column("isin", String(255), nullable=True),
    Column("registrationCode", String(255), nullable=True),
    Column("issuerName", String(255), nullable=True),
    Column("tradingCurrency", String(255), nullable=True),
    Column("faceValue", String(255), nullable=True),
    Column("scale", Integer, nullable=True),
    Column("minimumStep", Numeric, nullable=True),
    Column("accruedInt", Numeric, nullable=True),
    Column("currencyStepPrice", String(255), nullable=True),
    Column("settleCode", String(255), nullable=True),
    Column("instrumentType", String(20), nullable=True),
    Column("settlementCurrency", String(20), nullable=True),
    Column("settlementDate", String(255), nullable=True),
    Column("maturityDate", String(255), nullable=True),
    Column("lotSize", Numeric, nullable=True),
    Column("isQualifiedOnly", Boolean, nullable=True),
    Column("isCanShort", Boolean, nullable=True),
    Column("baseAsset", String(255), nullable=True),
    Column("qualifiedTestId", Integer, nullable=True),
    Column("qualifiedTestIdTm", Integer, nullable=True),
    Column("availableForUnqualified", Boolean, nullable=True),
    Column("currencyNominal", String(255), nullable=True),
    Column("stepPrice", Numeric, nullable=True),
    Column("isBcsProduct", Boolean, nullable=True),
    Column("couponsPerYear", Integer, nullable=True),
    Column("couponRate", Numeric, nullable=True),
    Column("nextCoupon", String(255), nullable=True),
    Column("complexProduct", Numeric, nullable=True),
    Column("baseAssetFuture", String(255), nullable=True),
    Column("subType", String(255), nullable=True),
    Column("percentTargetCurrent", Numeric, nullable=True),
    Column("businessSector", String(255), nullable=True),
    Column("peNorm", Numeric, nullable=True),
    Column("priceTangibl", Numeric, nullable=True),
    Column("epsGrowthRate", Numeric, nullable=True),
    Column("predictedDps", Numeric, nullable=True),
    Column("dividendYield", Numeric, nullable=True),
    Column("priceChangeYear", Numeric, nullable=True),
    Column("targetPrice", Numeric, nullable=True),
    Column("mktcap", Numeric, nullable=True),
    Column("isBlocked", Boolean, nullable=True),
    Column("businessSectorId", Integer, nullable=True),
    Column("primaryBoard", String(255), nullable=True),
    Column("secondaryBoards", String(255), nullable=True),
    Column("isCanMargin", Boolean, nullable=True),
    Column("isReplacementBond", Boolean, nullable=True),
    Column("subTitle", String(255), nullable=True),
    Column("couponTypeName", String(255), nullable=True),
    Column("emissionDate", String(255), nullable=True),
    Column("creditRating", String(255), nullable=True),
    Column("liquidityRating", String(255), nullable=True),
    Column("bcsScore", Integer, nullable=True),
    Column("bcsScoreColor", String(255), nullable=True),
    Column("nrdCode", String(255), nullable=True),
    Column("strike", Numeric, nullable=True),
    Column("baseAssetSecuritySecCode", String(255), nullable=True),
    Column("baseAssetSecurityClassCode", String(255), nullable=True),
    Column("businessCountry", String(255), nullable=True),
    Column("businessCountryCode", String(255), nullable=True),
    Column("priceChangeHalfYear", Numeric, nullable=True),
    Column("priceChangeMonth", Numeric, nullable=True),
    Column("priceChangeEarlyYear", Numeric, nullable=True),
    Column("firstCurrCode", String(255), nullable=True),
    Column("amortisedMty", Boolean, nullable=True),
    Column("auditDateTime", DateTime, server_default=text("(CURRENT_TIMESTAMP AT TIME ZONE 'Europe/Moscow')"))
)

depoLimit = Table(
    "depoLimit",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True, nullable=False),
    Column("ticker", String(255), nullable=False),
    Column("classCode", String(255), nullable=False),
    Column("exchange", String(255), nullable=False),
    Column("averagePrice", Integer, nullable=False),
    Column("quantitytype", String(255), nullable=False),
    Column("quantityvalue", Integer, nullable=False),
    Column("quantityBatchtype", String(255), nullable=False),
    Column("quantityBatchvalue", Integer, nullable=False),
    Column("instrumentType", String(255), nullable=False),
    Column("loadDate", DateTime, nullable=False),
    Column("lockedBuyValue", Integer, nullable=False),
    Column("lockedSellValue", Integer, nullable=False),
    Column("auditDateTime", DateTime, server_default=text("(CURRENT_TIMESTAMP AT TIME ZONE 'Europe/Moscow')"))
)

moneyLimits = Table(
    "moneyLimits",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True, nullable=False),
    Column("exchange", String(255), nullable=False),
    Column("currencyCode", String(255), nullable=False),
    Column("locked", Integer, nullable=False),
    Column("averagePrice", Integer, nullable=False),
    Column("instrumentType", String(255), nullable=False),
    Column("quantitytype", String(255), nullable=False),
    Column("quantityvalue", Integer, nullable=False),
    Column("loadDate", DateTime, nullable=False),
    Column("auditDateTime", DateTime, server_default=text("(CURRENT_TIMESTAMP AT TIME ZONE 'Europe/Moscow')"))
)

allBids = Table(
    "allBids",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True, nullable=False),
    Column("orderNum", BigInteger, nullable=False),
    Column("orderId", String(255), nullable=False),
    Column("clientCode", String(255), nullable=False),
    Column("executionDateTime", DateTime, nullable=False),
    Column("executedValue", Numeric, nullable=False),
    Column("orderDateTime", DateTime, nullable=False),
    Column("tradeDate", Date, nullable=False),
    Column("updateDateTime", DateTime, nullable=False),
    Column("ticker", String(255), nullable=False),
    Column("classCode", String(30), nullable=False),    
    Column("takePrice", Numeric, nullable=True),
    Column("stopPrice", Numeric, nullable=True),
    Column("price", Numeric, nullable=False),
    Column("settlementCurrency", String(5), nullable=False),
    Column("orderQuantuty", Numeric, nullable=True),
    Column("remainedQuantity", Numeric, nullable=True),
    Column("executedQuantity", Numeric, nullable=False),
    Column("rejectReason", String(255), nullable=True),
    Column("averagePrice", Numeric, nullable=False),
    Column("calculationVolume", Numeric, nullable=False),
    Column("contractSum", Numeric, nullable=False),
    Column("orderStatus", Integer, nullable=False, comment="1 - deselected, 2 - done, 3 - active"),
    Column("orderType", Integer, nullable=False, comment="1 - Рыночная, 2 - Лимитная, 3 - Айсберг, 4 - Стоп-лосс, 5 - Тейк-профит (порождает 2), 6 - Стоп-лосс, 7 - Тейк-профит и стоп-лосс, 10 - Лимит на 30 дней, 11 - Тейк-профит, 12 - Трейлинг-стоп"),
    Column("side", Integer, nullable=False, comment="1 - Buy, 2 - Sell"),
    Column("orderQuantityLots", Numeric, nullable=False),
    Column("remainedQuantityLots", Numeric, nullable=False),
    Column("executedQuantityLots", Numeric, nullable=False),
    Column("linkedOrder", String(255), nullable=True),
    Column("stopOrder", String(255), nullable=True),
    Column("visible", Numeric, nullable=True),
    Column("marketTakeProfit", Integer, nullable=True, comment="1 - Рыночная заявка, 2 - Лимитная заявка"),
    Column("marketStopLoss", Integer, nullable=True, comment="1 - Рыночная заявка, 2 - Лимитная заявка"),
    Column("positionPriceStop", Numeric, nullable=True),
    Column("positionPriceLimit", Numeric, nullable=True),
    Column("auditDateTime", DateTime, server_default=text("(CURRENT_TIMESTAMP AT TIME ZONE 'Europe/Moscow')"))
    
)

metadata_obj.create_all(engine)