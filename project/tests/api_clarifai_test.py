from clarifai.rest import ClarifaiApp
app = ClarifaiApp(api_key = 'a6d5bde7651a4faaaaba0e4b64976f75')
model = app.models.get("general-v1.3")

image = ClImage(file_obj=open('C:\Users\Ashley\Pictures\DSC_8479.jpeg', 'rb'))
model.predict([image])


model.predict_by_url(url='https://samples.clarifai.com/metro-north.jpg')
