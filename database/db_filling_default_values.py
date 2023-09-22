import json

from db import (
    session, Tag
)

def load_default_tags():
    with open("database/data/default_tags.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    for tag_data in data['tag']:
        existing_tag = session.query(Tag).filter_by(name_en=tag_data["name_en"]).first()
        
        if not existing_tag:
            tag = Tag(
                status="active",
                name_en=tag_data["name_en"],
                name_uk=tag_data["name_uk"],
                name_pl=tag_data["name_pl"],
                name_ru=tag_data["name_ru"],
            )
            session.add(tag)
            session.commit()


if __name__ == '__main__':
    load_default_tags()