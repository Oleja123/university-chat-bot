def from_json_collection(data: dict, cls):
    res = []
    for i in data['items']:
        res.append(cls.from_dict(i))
    return {'items': res, '_meta': data['_meta']}
