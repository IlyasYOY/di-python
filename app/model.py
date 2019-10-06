from dataclasses import dataclass, asdict

from bson import ObjectId


@dataclass
class Todo:
    _id: ObjectId
    title: str
    text: str
    done: bool

    def to_dict(self):
        d = asdict(self)
        d['_id'] = str(self._id)
