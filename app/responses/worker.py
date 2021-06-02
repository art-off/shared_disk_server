from app import ma

class WorkerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'profession_type.id')
