
# from pydantic import dataclasses
from tortoise.models import Model
# from pydantic import BaseModel
from tortoise import fields
from datetime import datetime, date, timedelta


# class Config:
#     arbitrary_types_allowed = True


# @dataclasses.dataclass(config=Config)
class Employee(Model):
    # El campo de la llave primaria se crea automáticamente
    id = fields.IntField(pk=True)
    codigo = fields.CharField(max_length=255)
    nombre = fields.CharField(max_length=255)
    apellido1 = fields.CharField(max_length=255)
    apellido2 = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, default="user@host.com")
    fecha_incorporacion = fields.DateField(default=datetime.strftime(date.today() + timedelta(days=1), '%Y-%m-%d'))
    nif = fields.CharField(max_length=9, default="12345678Z")
    description = fields.TextField(default="")

    def __str__(self):
        return ' '.join([self.nombre, self.apellido1, self.apellido2])

    class PydanticMeta:
        pass

