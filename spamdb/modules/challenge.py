import random
from string import ascii_letters, digits
import datetime
from modules.env import env
from modules.user import User
import modules.util as util

challengedUser = "challenged"

def update_challenge_colls() -> None:
    args = env.args
    db = env.db

    if args.drop:
        db.challenge.drop()

    challenges: list[Challenge] = []
    users: list[User] = []

    if args.challenges is None:
        return

    users.append(User(challengedUser, [], [], False))

    for uid, _ in zip(env.uids, list(range(args.challenges))):
        challenge_id = ''.join(random.sample(ascii_letters + digits, 8))
        challenges.append(
            {   "_id": challenge_id,
                "status": 10,
                "variant": 1,
                "timeControl": {"d": 2},
                "mode": False,
                "colorChoice": 0,
                "finalColor": True,
                "challenger": {"id": uid, "r": {"i": 1500, "p": True}},
                "createdAt": util.time_since_days_ago(1),
                "expiresAt": datetime.datetime.now() + datetime.timedelta(days=10),
                "rules": [],
                "destUser": {"id": challengedUser, "r": {"i": 1500, "p": True}},
                "seenAt": datetime.datetime.now()
            }
        )

    if not args.no_create:
        util.bulk_write(db.challenge, challenges)
        util.bulk_write(db.user4, users)

    return challenges

class Challenge:
    def __init__(self, challenge: dict):
        self._id = challenge["_id"]
        self.status = challenge["status"]
        self.variant = challenge["variant"]
        self.timeControl = challenge["timeControl"]
        self.mode = challenge["mode"]
        self.colorChoice = challenge["colorChoice"]
        self.finalColor = challenge["finalColor"]
        self.challenger = challenge["challenger"]
        self.createAt = challenge["createAt"]
        self.expiresAt = challenge["expiresAt"]
        self.rules = challenge["rules"]
        self.destUser = challenge["destUser"]
