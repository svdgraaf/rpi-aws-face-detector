import os
import sys
import boto3

client = boto3.client('rekognition', region_name='eu-west-1')

path = sys.argv[1]
image_file = open(path, "rb")
resp = client.search_faces_by_image(
    Image={
        'Bytes': image_file.read()
    },
    CollectionId='Sentia'
)
print resp

for face in resp['FaceMatches']:
    print "%s: %s" % (face['Face']['ExternalImageId'], face['Face']['Confidence'])
else:
    print "No faces found in collection"
