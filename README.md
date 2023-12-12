# About the project
This project helps in object detection and annotate images based on text i.e add bounding boxes to the detected object or part based on text data.
There is no front end for this project currently. This project is based on django application and runs as a server.

### Input
The input to the server is sent as API request (Ex Postman). The request should be sent to http://localhost:< port >/owlDjango/invocations/
```
Example Request
{
    "image" : "drive folder URL that contains images",
    "text" : "a photo of a cat, a photo of a dog"
}
```
### Output
The output given is an API response that contains the S3 bucket URL where the images and their corresponding annotations are saved in YOLO format.

## Pre-requisites
```
git clone https://github.com/mkovelamudi/Text-based-image-annotation.git
cd Text-based-image-annotation/owlVit
pip install -r requirements.txt
```

## Google Auth Token Generation
1. Create project in Google Cloud Console
2. Select Google Drive API service
3. Switch to Credentials Tab and click "Create Credentials" and OAuth Client ID
4. Download client_secrets.json  and replace it with existing file in "/Text-based-image-annotation/owlVit/owlDjango/googleDrive/"
5. Copy client ID and paste it in settings.yaml (/Text-based-image-annotation/owlVit/owlDjango/googleDrive/) in client_id field
6. Copy client secret and paste it in settings.yaml (/Text-based-image-annotation/owlVit/owlDjango/googleDrive/) in client_secret field

## S3 Client
1. As the output will be stored in a AWS S3 buckt, we need to setup AWS account and s3 bucket details in the application.
2. Create AWS account and copy the Access key, secret key from account details and paste it in loadS3Client.py file in "/Text-based-image-annotation/owlVit/owlDjango/s3Client/"
3. Create an S3 bucket and make it public.
4. Copy bucket name and paste it in bucket key of bucket_details.
5. Copy bucket url and paste it in bucket_url key of bucket_details.

## Usage
After following above steps, run the application using start.sh shell script<br />
OR <br />
python3 manage.py migrate <br />
python3 manage.py runserver < port >
