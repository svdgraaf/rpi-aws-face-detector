import os
import sys
import boto3

client = boto3.client('rekognition', region_name='eu-west-1')

path = sys.argv[1]
who = sys.argv[2]

for filename in os.listdir(path):

    print "Going for: %s/%s" % (path, filename)
    image_file = open("%s/%s" % (path, filename), "rb")
    resp = client.index_faces(
        Image={
            'Bytes': image_file.read()
        },
        CollectionId='Sentia',
        ExternalImageId=who
    )
    print resp
