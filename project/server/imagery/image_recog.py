from clarifai.rest import ClarifaiApp

import json

RECOGNITION_CONFIDENCE_THRESHOLD = 0.85

def get_tags_for_image(url):
    """
    Run recognition on a given image and get a list of descriptive
    tags that meet the confidence threshold.
    
    Params:
        url (str) location of the image to analyze

    Returns:
        (str) json dump of tag strings list
    """
    
    app = ClarifaiApp(api_key = 'a6d5bde7651a4faaaaba0e4b64976f75')
    model = app.models.get('general-v1.3')

    response = model.predict_by_url(url=url)

    concepts = response['outputs'][0]['data']['concepts']
    tags = []

    for concept in concepts:
        if concept['value'] >= RECOGNITION_CONFIDENCE_THRESHOLD:
            tags.append(concept['name'])

    return json.dumps(tags)

if __name__ == '__main__':
    test_tags = get_tags_for_image('http://runningwithmiles.img.boardingarea.com/wp-content/uploads/2017/07/deathvalley.jpeg')
    print(test_tags)
