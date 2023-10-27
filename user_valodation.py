from create_bot import dp, bot
from database import session, User



async def get_verified_user(telegram_id):
    user = session.query(User).get(telegram_id)
    
    if not user:
        raise Exception("User not found!")
    
    chat_member = await bot.get_chat_member(telegram_id, telegram_id)
    current_username = chat_member.user.username
    if user.username != f'@{current_username}':
        user.username = f'@{current_username}'
        session.commit()
    
    return user
