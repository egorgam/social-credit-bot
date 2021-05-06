import pytest

from app import actions, aliases, models


@pytest.fixture
def message(mocker):
    message = mocker.MagicMock()
    message.chat.id = 9999
    message.from_user.id = 1
    message.from_user.username = "test1"
    message.from_user.first_name = "a"
    message.from_user.last_name = "b"
    message.reply_to_message.from_user.is_bot = False
    message.reply_to_message.from_user.id = 2
    message.reply_to_message.from_user.username = "test2"
    message.reply_to_message.from_user.first_name = "c"
    message.reply_to_message.from_user.last_name = "d"
    return message


@pytest.fixture
def user(session, message):
    user = models.User(
        id=message.from_user.id,
        name=message.from_user.username,
        chat_id=message.chat.id,
        rank=aliases.INC,
    )
    session.add(user)
    session.commit()


class TestGetSocialRank:
    def test_empty_rank(self, message, session):
        result = actions.get_report_of_social_rank(message, session)
        assert result == "NO RANK REPORT"

    @pytest.mark.usefixtures("user")
    def test_rank_exists(self, message, session):
        result = actions.get_report_of_social_rank(message, session)
        assert result == "test1: 20\n"


class TestEditSocialCredit:
    @pytest.mark.parametrize(
        "action, new_rank",
        [(aliases.Action.INCREASE, 20), (aliases.Action.DECREASE, -20)],
        ids=["increase", "decrease"],
    )
    def test_usual_case(self, message, session, action, new_rank):
        timeouts = {}
        result = actions.edit_social_credit(message, session, action, timeouts)
        stored_users = session.query(models.User).all()
        assert len(stored_users) == 1
        assert stored_users[0].name == message.reply_to_message.from_user.username
        assert result == "{} {} rank of {}!\nNow their social credit is {} points".format(
            message.from_user.username,
            action,
            message.reply_to_message.from_user.username,
            new_rank
        )

    @pytest.mark.parametrize(
        "action, new_rank", [(aliases.Action.INCREASE, 20)], ids=["increase"]
    )
    def test_without_username(self, message, session, action, new_rank):
        timeouts = {}
        message.reply_to_message.from_user.username = None
        result = actions.edit_social_credit(
            message, session, aliases.Action.INCREASE, timeouts
        )
        assert result == "test1 increased rank of c d!\nNow their social credit is 20 points"
