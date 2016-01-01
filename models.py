import datetime

import itertools
import json

from playhouse.shortcuts import *
from SampleJSON import pres

mysql_db = MySQLDatabase('Prescription', user='root')


def get_pretty_print(json_object):
    return json.dumps(json_object, sort_keys=True, indent=4, separators=(',', ': '))


class MySQLModel(Model):
    """A base model that will use our MySQL database"""

    class Meta:
        database = mysql_db


class Doctor(MySQLModel):
    doctor_id = PrimaryKeyField()
    first_name = CharField(null=False, max_length=100)
    last_name = CharField(null=False, max_length=100)
    phone_number = CharField(null=False, unique=True, max_length=10)
    timestamp = DateTimeField(default=datetime.datetime.now)

    @classmethod
    def addDoctor(cls, docDict):
        with mysql_db.transaction():
            Doctor.create(**docDict)

    @classmethod
    def getDoctor(cls, id):
        x = Doctor.get(Doctor.doctor_id == id)
        # x.timestamp = str(x.timestamp)
        return x

    @classmethod
    def getAllDoctor(cls):
        res = Doctor.select()
        # for row in res:
        #    row.timestamp = str(row.timestamp)
        return res


class Patient(MySQLModel):
    patient_id = PrimaryKeyField()
    first_name = CharField(null=False, max_length=100)
    last_name = CharField(null=False, max_length=100)
    phone_number = CharField(null=False, unique=True, max_length=10)
    timestamp = DateTimeField(default=datetime.datetime.now)

    @classmethod
    def addPatient(cls, docDict):
        with mysql_db.transaction():
            Patient.create(**docDict)

    @classmethod
    def getPatient(cls, id):
        x = Patient.get(Patient.patient_id == id)
        # x.timestamp = str(x.timestamp)
        return x

    @classmethod
    def getAllPatient(cls):
        res = Patient.select()
        # for row in res:
        #    row.timestamp = str(row.timestamp)
        return res

    @classmethod
    def getPatientID(cls, name, phone_number):
        id = Patient.get(first_name=name, phone_number=phone_number)
        return id.patient_id


class Medicines(MySQLModel):
    medicine_id = PrimaryKeyField()
    name = CharField(null=False, max_length=256)
    default_morning = BooleanField(default=False)
    default_evening = BooleanField(default=False)
    default_night = BooleanField(default=False)

    @classmethod
    def addMedicine(self, name):
        with mysql_db.transaction():
            Medicines.create(name=name)

    @classmethod
    def addMedicine(self, name):
        Medicines.get(name=name)


class Prescription(MySQLModel):
    id = PrimaryKeyField()
    patient_id = ForeignKeyField(Patient, to_field="patient_id")
    prescription = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    @classmethod
    def addPrescription(cls, patientID, prescriptionJSON):
        with mysql_db.transaction():
            Prescription.create(patient_id=patientID, prescription=prescriptionJSON)

    @classmethod
    def getEveryPrescription(cls, id):
        l = []

        allPrescriptions = Prescription.select().where(Prescription.patient_id == id)
        for prescription in allPrescriptions:
            l.append(model_to_dict(prescription))
        listOfPrescriptionDict = l
        return listOfPrescriptionDict

    @classmethod
    def getLatestPrescription(cls, id):
        query = "SELECT max(id) FROM Prescription.prescription where patient_id_id = %s"
        cursor = mysql_db.execute_sql(query, id)
        latest_id = cursor.fetchall()[0][0]

        latest_prescription_row = Prescription.get(Prescription.id == latest_id)
        return model_to_dict(latest_prescription_row)



print Prescription.getLatestPrescription(1)


def initialize():
    mysql_db.connect()
    mysql_db.create_tables([Doctor, Patient, Prescription], safe=True)
    mysql_db.close()
