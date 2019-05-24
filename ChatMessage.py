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


class ClickEvent:
    action: Optional[str]
    value: Optional[str]

    def __init__(self, action: Optional[str], value: Optional[str]) -> None:
        self.action = action
        self.value = value

    @staticmethod
    def from_dict(obj: Any) -> 'ClickEvent':
        assert isinstance(obj, dict)
        action = from_union([from_str, from_none], obj.get("action"))
        value = from_union([from_str, from_none], obj.get("value"))
        return ClickEvent(action, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["action"] = from_union([from_str, from_none], self.action)
        result["value"] = from_union([from_str, from_none], self.value)
        return result


class ExtraExtra:
    color: Optional[str]
    text: Optional[str]

    def __init__(self, color: Optional[str], text: Optional[str]) -> None:
        self.color = color
        self.text = text

    @staticmethod
    def from_dict(obj: Any) -> 'ExtraExtra':
        assert isinstance(obj, dict)
        color = from_union([from_str, from_none], obj.get("color"))
        text = from_union([from_str, from_none], obj.get("text"))
        return ExtraExtra(color, text)

    def to_dict(self) -> dict:
        result: dict = {}
        result["color"] = from_union([from_str, from_none], self.color)
        result["text"] = from_union([from_str, from_none], self.text)
        return result


class Value:
    extra: Optional[List[ExtraExtra]]
    text: Optional[str]

    def __init__(self, extra: Optional[List[ExtraExtra]], text: Optional[str]) -> None:
        self.extra = extra
        self.text = text

    @staticmethod
    def from_dict(obj: Any) -> 'Value':
        assert isinstance(obj, dict)
        extra = from_union([lambda x: from_list(ExtraExtra.from_dict, x), from_none], obj.get("extra"))
        text = from_union([from_str, from_none], obj.get("text"))
        return Value(extra, text)

    def to_dict(self) -> dict:
        result: dict = {}
        result["extra"] = from_union([lambda x: from_list(lambda x: to_class(ExtraExtra, x), x), from_none], self.extra)
        result["text"] = from_union([from_str, from_none], self.text)
        return result


class HoverEvent:
    action: Optional[str]
    value: Optional[List[Value]]

    def __init__(self, action: Optional[str], value: Optional[List[Value]]) -> None:
        self.action = action
        self.value = value

    @staticmethod
    def from_dict(obj: Any) -> 'HoverEvent':
        assert isinstance(obj, dict)
        action = from_union([from_str, from_none], obj.get("action"))
        value = from_union([lambda x: from_list(Value.from_dict, x), from_none], obj.get("value"))
        return HoverEvent(action, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["action"] = from_union([from_str, from_none], self.action)
        result["value"] = from_union([lambda x: from_list(lambda x: to_class(Value, x), x), from_none], self.value)
        return result


class ChatMessageExtra:
    extra: Optional[List[ExtraExtra]]
    click_event: Optional[ClickEvent]
    hover_event: Optional[HoverEvent]
    text: Optional[str]

    def __init__(self, extra: Optional[List[ExtraExtra]], click_event: Optional[ClickEvent], hover_event: Optional[HoverEvent], text: Optional[str]) -> None:
        self.extra = extra
        self.click_event = click_event
        self.hover_event = hover_event
        self.text = text

    @staticmethod
    def from_dict(obj: Any) -> 'ChatMessageExtra':
        assert isinstance(obj, dict)
        extra = from_union([lambda x: from_list(ExtraExtra.from_dict, x), from_none], obj.get("extra"))
        click_event = from_union([ClickEvent.from_dict, from_none], obj.get("clickEvent"))
        hover_event = from_union([HoverEvent.from_dict, from_none], obj.get("hoverEvent"))
        text = from_union([from_str, from_none], obj.get("text"))
        return ChatMessageExtra(extra, click_event, hover_event, text)

    def to_dict(self) -> dict:
        result: dict = {}
        result["extra"] = from_union([lambda x: from_list(lambda x: to_class(ExtraExtra, x), x), from_none], self.extra)
        result["clickEvent"] = from_union([lambda x: to_class(ClickEvent, x), from_none], self.click_event)
        result["hoverEvent"] = from_union([lambda x: to_class(HoverEvent, x), from_none], self.hover_event)
        result["text"] = from_union([from_str, from_none], self.text)
        return result


class ChatMessage:
    extra: Optional[List[ChatMessageExtra]]
    text: Optional[str]

    def __init__(self, extra: Optional[List[ChatMessageExtra]], text: Optional[str]) -> None:
        self.extra = extra
        self.text = text

    @staticmethod
    def from_dict(obj: Any) -> 'ChatMessage':
        assert isinstance(obj, dict)
        extra = from_union([lambda x: from_list(ChatMessageExtra.from_dict, x), from_none], obj.get("extra"))
        text = from_union([from_str, from_none], obj.get("text"))
        return ChatMessage(extra, text)

    def to_dict(self) -> dict:
        result: dict = {}
        result["extra"] = from_union([lambda x: from_list(lambda x: to_class(ChatMessageExtra, x), x), from_none], self.extra)
        result["text"] = from_union([from_str, from_none], self.text)
        return result


def chat_message_from_dict(s: Any) -> ChatMessage:
    return ChatMessage.from_dict(s)


def chat_message_to_dict(x: ChatMessage) -> Any:
    return to_class(ChatMessage, x)

