from datetime import datetime

from sqlalchemy import distinct, func
from sqlalchemy.orm import Session

from .models import Goods
from .schemas import GoodsCreate


def create_goods(db: Session, goods: GoodsCreate):
    db_goods = Goods(
        sku_id=goods.sku_id,
        name=goods.name,
        category=goods.category,
        amount=goods.amount,
        avg_cart=goods.avg_cart,
        dt=goods.dt,
        trigger=goods.trigger,
        shelve=goods.shelve,
    )
    db.add(db_goods)
    db.commit()
    db.refresh(db_goods)
    return db_goods


def get_goods_by_sku(db: Session, sku_id: str):
    return db.query(Goods).filter(Goods.sku_id == sku_id).first()


def get_goods_by_shelve(db: Session, shelve: str):
    return db.query(Goods).filter(Goods.shelve == shelve).all()


def update_goods_amount(db: Session, sku_id: str, new_amount: int):
    db_goods = db.query(Goods).filter(Goods.sku_id == sku_id).first()
    if db_goods:
        db_goods.amount = new_amount
        db.commit()
        db.refresh(db_goods)
    return db_goods


def get_all_goods(db: Session):
    return db.query(Goods).all()


def get_all_shelves(db: Session):
    return db.query(distinct(Goods.shelve)).all()


def get_all_shelves_with_avg_trigger(db: Session):
    return db.query(Goods.shelve, func.avg(Goods.trigger)).group_by(Goods.shelve).all()
