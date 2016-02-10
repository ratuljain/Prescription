import json
import requests

# response = requests.get("http://localhost:5000/Prescription/api/v1.0/prescription/all/3")
response = requests.get("http://104.131.46.2:5000/Prescription/api/v1.0/patients/1")


# response = requests.get("http://localhost:5000/Prescription/api/v1.0/prescription/3")
# print str(response.text)

json_data = json.loads(response.text)
x = json_data["patients"]
print x["phone_number"]
# print (json_data).items()

# print json_data.
# actual = json.loads(x)
# # print medicines
# print json_data["Prescription"]
# next = json_data['Prescription']
# for i in next:
#     print i['id']
# # print next[""]
# # lol = json.loads(next['prescription'])
# #
# # lol2 = next['Medicines']
# for key, value in medicines.items():
#     print key, value
#     print ""

