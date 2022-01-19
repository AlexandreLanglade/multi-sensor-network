from google.cloud import firestore

# $env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\Devel\Downloads\??"
db = firestore.Client(project='multi-sensor-network-api')

doc_temperatures = db.collection(u'datas').document(u'temperatures')
doc_devices = db.collection(u'datas').document(u'devices')
doc_presences = db.collection(u'datas').document(u'presences')
doc_weathers = db.collection(u'datas').document(u'weathers')
"""
doc_devices.set({
    u'd1': u'Iphone',
    u'd2': u'Oppo'
})"""
doc_temperatures.set({})
doc_devices.set({})
doc_presences.set({})
doc_weathers.set({})
print(doc_devices.get().to_dict()) #to dict retourne une copie
