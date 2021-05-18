from app import ma


class File:
    def __init__(self, id: str, name: str, kind: str, mine_type: str):
        self.id = id
        self.name = name
        self.kind = kind
        self.mine_type = mine_type


class FileSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'mine_type')
