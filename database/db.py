from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, JSON, Float, DateTime, DECIMAL
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()
engine = create_engine('sqlite:///db.sqlite3', echo=True)


class User(Base):
    __tablename__ = 'user'
    
    telegram_id = Column(Integer, primary_key=True, autoincrement=False)
    username = Column(String)
    language = Column(String)
    status = Column(String)
    address = Column(String)
    long_itude = Column(Float)
    lat_itude = Column(Float)
    data = Column(JSON)
    rating = Column(JSON)
    created_at = Column(DateTime)
    
    def __init__(
        self, telegram_id, language,
        status, data, rating, username,
        address, long_itude, lat_itude
        ):
        self.telegram_id = telegram_id
        self.username = username
        self.language = language
        self.status = status
        self.address = address
        self. long_itude = long_itude
        self.lat_itude = lat_itude
        self.data = data
        self.rating = rating
        self.created_at = datetime.now()
        super().__init__()


class Tag(Base):
    __tablename__ = 'tag'
    
    id = Column(Integer, autoincrement=True, primary_key=True)
    status = Column(String)
    name_en = Column(String)
    name_uk = Column(String)
    name_pl = Column(String)
    name_ru = Column(String)
    
    def __init__(self, status, name_en, name_uk, name_pl,
        name_ru
        ):
        self.status = status
        self.name_en = name_en
        self.name_uk = name_uk
        self.name_pl = name_pl
        self.name_ru = name_ru
        super().__init__()


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, autoincrement=True, primary_key=True)
    user = Column(Integer, ForeignKey('user.telegram_id'))
    name = Column(String)
    media = Column(JSON)
    description = Column(String)
    status = Column(String)
    created_at = Column(DateTime)

    def __init__(
        self, user, name, media, description, status 
        ):
        self.user = user
        self.name = name
        self.media = media
        self.description = description
        self.status = status
        self.created_at = datetime.now()
        super().__init__()


class Favorite(Base):
    __tablename__ = 'favorite'
    
    id = Column(Integer, autoincrement=True, primary_key=True)
    user = Column(Integer, ForeignKey('user.telegram_id'))
    item = Column(Integer, ForeignKey('item.id'))
    
    def __init__(
        self, user, item
        ):
        self.user = user
        self.item = item
        super().__init__()


class ItemTag(Base):
    __tablename__ = 'item_tag'
    
    id = Column(Integer, autoincrement=True, primary_key=True)
    item = Column(Integer, ForeignKey('item.id'))
    tag = Column(Integer, ForeignKey('tag.id'))
    
    def __init__(
        self, item, tag
        ):
        self.item = item
        self.tag = tag
        super().__init__()



Base.metadata.create_all(engine)
Session = sessionmaker(engine)
session = Session()