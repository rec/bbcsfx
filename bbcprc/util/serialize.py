"""Serialize attrs - from hardback project"""
import attr, yaml


def load(source, data):
    """Unserialize from JSON-like data (dicts, strings, etc) to a dataclass"""
    try:
        fields = attr.fields_dict(data.__class__)
    except:
        try:
            return type(data)(source)
        except:
            return source

    unknown = set(source) - set(fields)
    if unknown:
        raise ValueError('Do not understand fields:', *unknown)

    for k, v in source.items():
        subitem = getattr(data, k)
        setattr(data, k, load(v, subitem))

    return data


def save(data):
    """Serialize from a data class to JSON-like data"""
    return attr.asdict(data)


class Save:
    def __init__(self, filename, data):
        self.filename = filename
        self.data = data

    def load(self):
        try:
            with open(self.filename) as fp:
                load(yaml.safe_load(fp), self.data)
                return True
        except:
            return False

    def save(self):
        with open(self.filename, 'w') as fp:
            yaml.safe_dump(save(self.data), fp)
