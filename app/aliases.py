from app import models

INC = 20
INCREASE_CREDIT_STICKER = "AgADAgADf3BGHA"
DECREASE_CREDIT_STICKER = "AgADAwADf3BGHA"


class Action:
    INCREASE = "increased"
    DECREASE = "decreased"


class CoolDownMessage:
    def __init__(self, user_name, replied_user_name, timeout):
        self.text = f"{user_name} can't edit social credit of {replied_user_name} for {60 - timeout} seconds"


class BotEditionMessage:
    text = "Can't edit bot social credit"


class SelfEditionMessage:
    text = "Can't edit self social credit"


class SuccessRankMessage:
    def __init__(self, user_name, action, replied_user_name, new_rank):
        self.text = f"{user_name} {action} rank of {replied_user_name}!\nNow their social credit is {new_rank} points"


class RankMessage:
    def __init__(self, message, session):
        self.text = self._gen_text(message, session)

    def _gen_text(self, message, session):
        social_rank = {}
        for user in session.query(models.User).filter_by(chat_id=message.chat.id).all():
            social_rank[user.name] = user.rank
        sorted_rank = {
            k: v
            for k, v in sorted(
                social_rank.items(), key=lambda item: item[1], reverse=True
            )
        }
        return "".join([f"{name}: {rank}\n" for name, rank in sorted_rank.items()])


class NoRankMessage:
    text = "NO RANK REPORT"
