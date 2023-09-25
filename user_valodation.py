from create_bot import dp, bot
from database import session, User



async def get_verified_user(telegram_id):
    user = session.query(User).get(telegram_id)
    
    if not user:
        raise Exception("User not found!")

    # if user.status != "desired_status":
    #     raise Exception("User status is not valid!")
    
    chat_member = await bot.get_chat_member(telegram_id, telegram_id)
    current_username = chat_member.user.username
    if user.username != current_username:
        user.username = current_username
        session.commit()
    
    return user
