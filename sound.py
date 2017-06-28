import boto3
import tempfile
import sys
import io


client = boto3.client('polly', region_name='eu-west-1')
response = client.synthesize_speech(
    OutputFormat='mp3',
    Text='Hi %s' % sys.argv[1],
    TextType='text',
    VoiceId='Joanna'
)
f = tempfile.NamedTemporaryFile(mode='w+b', delete=False, suffix='.mp3')
for block in response['AudioStream']._raw_stream:
    f.write(block)
print f.name
f.close()
