from app import ma


class CustomerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'middle_name', 'last_name', 'email')
