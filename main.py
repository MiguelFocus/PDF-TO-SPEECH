import boto3

from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

import os

output_string = StringIO()
with open('sample.pdf', 'rb') as in_file:
    parser = PDFParser(in_file)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)

text = output_string.getvalue()
print(os.environ['AWS_KEY'])


def get_speech(text_to_speech):
    polly_client = boto3.Session(
                    aws_access_key_id="YOUR_KEY",
                    aws_secret_access_key="YOUR_SECRET_KEY",
                    region_name='YOUR_REGION').client('polly')

    response = polly_client.synthesize_speech(VoiceId='Joanna',
                                              OutputFormat='mp3',
                                              Text=text_to_speech,
                                              Engine='standard')

    file = open('speech.mp3', 'wb')
    file.write(response['AudioStream'].read())
    file.close()


get_speech(text)
