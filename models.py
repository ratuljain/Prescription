import datetime
from playhouse.shortcuts import *

mysql_db = MySQLDatabase('Prescription', user='root')

class MySQLModel(Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = mysql_db


class Doctor(MySQLModel):
    doctor_id = PrimaryKeyField()
    first_name = CharField(null = False, max_length = 100)
    last_name = CharField(null = False, max_length = 100)
    phone_number = CharField(null = False, unique = True, max_length = 10)
    timestamp = DateTimeField(default=datetime.datetime.now)

    @classmethod
    def addDoctor(cls, docDict):

        with mysql_db.transaction():
            Doctor.create(**docDict)

    @classmethod
    def getDoctor(cls, id):

        x = Doctor.get(Doctor.doctor_id == id)
        x.timestamp = str(x.timestamp)
        return x

    @classmethod
    def getAllDoctor(cls):
         res = Doctor.select()
         for row in res:
            row.timestamp = str(row.timestamp)
         return res

class Patient(MySQLModel):
    patient_id = PrimaryKeyField()
    first_name = CharField(null = False, max_length = 100)
    last_name = CharField(null = False, max_length = 100)
    phone_number = CharField(null = False, unique = True, max_length = 10)
    timestamp = DateTimeField(default=datetime.datetime.now)


def initialize():
    mysql_db.connect()
    mysql_db.create_tables([Doctor], safe=True)
    mysql_db.close()