from clarifai.rest import ClarifaiApp
app = ClarifaiApp(api_key = 'a6d5bde7651a4faaaaba0e4b64976f75')
model = app.models.get("general-v1.3")

response = model.predict_by_url(url='http://runningwithmiles.img.boardingarea.com/wp-content/uploads/2017/07/deathvalley.jpeg')

concepts = response['outputs'][0]['data']['concepts']
for concept in concepts:
    print(str(concept['name']), concept['value'])