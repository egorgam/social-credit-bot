import time
from typing import Optional

from app import aliases, models


def _calculate_rank(action, current_rank):
    if action is aliases.Action.INCREASE:
        return current_rank + aliases.INC
    else:
        return current_rank - aliases.INC


def _actualize_user(from_user, chat_id, session):
    user = (
        session.query(models.User).filter_by(chat_id=chat_id, id=from_user.id).first()
    )
    if user:
        if user.name != from_user.username:
            user.name = from_user.username
            session.commit()

    if from_user.username:
        user_name = from_user.username
    else:
        user_name = f"{from_user.first_name} {from_user.last_name}"

    return from_user.id, user_name


def edit_social_credit(message, session, action: str, timeouts) -> Optional[str]:
    if message.reply_to_message.from_user.is_bot is True:
        return aliases.BotEditionMessage().text

    user_id, user_name = _actualize_user(message.from_user, message.chat.id, session)

    replied_user_id, replied_user_name = _actualize_user(
        message.reply_to_message.from_user, message.chat.id, session
    )

    if user_id == replied_user_id:
        return aliases.SelfEditionMessage().text

    last_edition_time = int(timeouts.get(f"{user_id}{replied_user_id}", 0))
    timeout = int(time.time() - last_edition_time)
    if last_edition_time and timeout < 60:
        return aliases.CoolDownMessage(user_name, replied_user_name, timeout).text

    replied_user = (
        session.query(models.User)
        .filter_by(chat_id=message.chat.id, id=replied_user_id)
        .first()
    )
    if replied_user is None:
        new_rank = _calculate_rank(action, 0)
        user = models.User(
            id=replied_user_id,
            name=replied_user_name,
            chat_id=message.chat.id,
            rank=new_rank,
        )
        session.add(user)
    else:
        new_rank = _calculate_rank(action, replied_user.rank)
        replied_user.rank = new_rank

    timeouts[f"{user_id}|{replied_user_id}"] = time.time()

    session.commit()
    return aliases.SuccessRankMessage(
        user_name, action, replied_user_name, new_rank
    ).text


def get_report_of_social_rank(message, session):
    return aliases.RankMessage(message, session).text or aliases.NoRankMessage().text
