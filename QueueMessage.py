from typing import Optional, Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Extra:
    color: Optional[str]
    text: Optional[str]

    def __init__(self, color: Optional[str], text: Optional[str]) -> None:
        self.color = color
        self.text = text

    @staticmethod
    def from_dict(obj: Any) -> 'Extra':
        assert isinstance(obj, dict)
        color = from_union([from_str, from_none], obj.get("color"))
        text = from_union([from_str, from_none], obj.get("text"))
        return Extra(color, text)

    def to_dict(self) -> dict:
        result: dict = {}
        result["color"] = from_union([from_str, from_none], self.color)
        result["text"] = from_union([from_str, from_none], self.text)
        return result


class QueueMessage:
    extra: Optional[List[Extra]]
    text: Optional[str]

    def __init__(self, extra: Optional[List[Extra]], text: Optional[str]) -> None:
        self.extra = extra
        self.text = text

    @staticmethod
    def from_dict(obj: Any) -> 'QueueMessage':
        assert isinstance(obj, dict)
        extra = from_union([lambda x: from_list(Extra.from_dict, x), from_none], obj.get("extra"))
        text = from_union([from_str, from_none], obj.get("text"))
        return QueueMessage(extra, text)

    def to_dict(self) -> dict:
        result: dict = {}
        result["extra"] = from_union([lambda x: from_list(lambda x: to_class(Extra, x), x), from_none], self.extra)
        result["text"] = from_union([from_str, from_none], self.text)
        return result


def queue_message_from_dict(s: Any) -> QueueMessage:
    return QueueMessage.from_dict(s)


def queue_message_to_dict(x: QueueMessage) -> Any:
    return to_class(QueueMessage, x)
