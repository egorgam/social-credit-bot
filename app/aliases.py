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
        self.text = f"{user_name} {action} rank of {replied_user_name}!\nNow they social credit are {new_rank} points"


class RankMessage:
    def __init__(self, sorted_rank):
        self.sorted_rank = sorted_rank
        self.result = ""
        self.text = self._gen_text()

    def _gen_text(self):
        for name, rank in self.sorted_rank.items():
            self.result = self.result + name + ": " + str(rank) + "\n"
        return self.result


class NoRankMessage:
    text = "NO RANK REPORT"
