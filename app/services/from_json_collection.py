def from_json_collection(data: dict, cls):
    data = data['items']
    res = []
    for i in data:
        res.append(cls.from_dict(i))
    return {'items': res, 'next': data['_links']['next'], 'prev': data['_links']['prev']}
