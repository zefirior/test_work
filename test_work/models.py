import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship


__all__ = [
    "db",
    "Ticker",
    "Price",
    "Insider",
    "InsiderTicker",
    "TransactionType",
    "Trade",
]

db = SQLAlchemy()


class _BaseModel(db.Model):
    __abstract__ = True

    def marshall(self) -> dict:
        raise NotImplementedError


class Ticker(_BaseModel):
    __tablename__ = "ticker"

    id = sa.Column(sa.Integer, primary_key=True)
    code = sa.Column(sa.String, nullable=False, unique=True)

    def marshall(self) -> dict:
        return dict(
            id=self.id,
            code=self.code,
        )


class Price(_BaseModel):
    __tablename__ = "price"

    id = sa.Column(sa.Integer, primary_key=True)
    ticker_id = sa.Column(
        sa.Integer, sa.ForeignKey('ticker.id'), nullable=False)
    price_date = sa.Column(sa.Date, nullable=False)
    start = sa.Column(sa.DECIMAL)
    high = sa.Column(sa.DECIMAL)
    low = sa.Column(sa.DECIMAL)
    last = sa.Column(sa.DECIMAL)
    volume = sa.Column(sa.Integer)

    ticker = relationship(Ticker)

    def marshall(self) -> dict:
        return dict(
            id=self.id,
            ticker=self.ticker.code,
            price_date=self.price_date,
            start=self.start,
            high=self.high,
            low=self.low,
            last=self.last,
        )


class Insider(_BaseModel):
    __tablename__ = "insider"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False, unique=True)

    def marshall(self) -> dict:
        return dict(
            id=self.id,
            name=self.name,
        )


class InsiderTicker(_BaseModel):
    __tablename__ = "insider_ticker"

    id = sa.Column(sa.Integer, primary_key=True)
    insider_id = sa.Column(
        sa.Integer, sa.ForeignKey("insider.id"), nullable=False)
    ticker_id = sa.Column(
        sa.Integer, sa.ForeignKey("ticker.id"), nullable=False)
    relation = sa.Column(sa.String)
    owner_type = sa.Column(sa.String)

    insider = relationship(Insider)
    ticker = relationship(Ticker, backref="insider_ticker")

    def marshall(self) -> dict:
        return dict(
            id=self.id,
            insider=self.insider.marshall(),
            ticker=self.ticker.marshall(),
            relation=self.relation,
            owner_type=self.owner_type,
        )


class TransactionType(_BaseModel):
    __tablename__ = "transaction_type"

    id = sa.Column(sa.Integer, primary_key=True)
    code = sa.Column(sa.String, nullable=False, unique=True)

    def marshall(self) -> dict:
        return dict(
            id=self.id,
            code=self.code,
        )


class Trade(_BaseModel):
    __tablename__ = "trade"

    id = sa.Column(sa.Integer, primary_key=True)
    insider_ticker_id = sa.Column(
        sa.Integer, sa.ForeignKey("insider_ticker.id"), nullable=False)
    transaction_type_id = sa.Column(
        sa.Integer, sa.ForeignKey("transaction_type.id"), nullable=False)
    shares_traded = sa.Column(sa.Integer)
    last_price = sa.Column(sa.DECIMAL)
    shares_held = sa.Column(sa.Integer)

    insider_ticker = relationship(InsiderTicker)
    transaction_type = relationship(TransactionType)

    def marshall(self) -> dict:
        return dict(
            id=self.id,
            insider=self.insider_ticker.insider.name,
            ticker=self.insider_ticker.ticker.code,
            transaction_type=self.transaction_type.code,
            shares_traded=self.shares_traded,
            last_price=self.last_price,
            shares_held=self.shares_held,
        )
