import requests
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from .s3Client.loadS3Client import get_bucket_details, get_client
from .model.loadModel import model, processor
from .googleDrive.googleDrive import list_image_files_in_folder
import torch
from PIL import Image
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
import io
import pytz
import traceback

@csrf_exempt
def invocations(request):
    if request.method == 'POST':
        try:
            json_request = json.loads(request.body)

            image_path = json_request['image']
            text = json_request['text']

            text_list = [item.strip() for item in text.split(',')]
            predictions = predict_internal(image_path, text_list)

            return JsonResponse({
                'url' : predictions[2],
                'total_images': predictions[0],
                'processed_images': predictions[1]
            })
        except Exception as e:
            tb = traceback.format_exc()
            return HttpResponseBadRequest(str(e)+ " "+ tb)
    else:
        return HttpResponseBadRequest("Invalid request method")

def predict_internal(images_url, text_list):
    url_response = check_if_url_is_openable(images_url)
    if url_response is None:
        raise Exception("Failed to fetch the URL.")
    images = list_image_files_in_folder(images_url)
    if len(images) == 0 or images is None:
        raise Exception("Failed to find images in the URL.")
    
    bucket_details = get_bucket_details()
    s3_client = get_client()
    total_images_processed = 0
    date = datetime.now(pytz.timezone('US/Pacific')).strftime('%m-%d-%Y-%H:%M:%S')
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    for img_file in images:
        image_name = img_file['title'].split('.')
        img_data = img_file.GetContentString(encoding='cp862')
        
        image = Image.open(io.BytesIO(bytearray(img_data, 'cp862')))
        inputs = processor(text=[text_list], images=image, return_tensors="pt").to(device)
        outputs = model(**inputs)

        target_sizes = torch.Tensor([image.size[::-1]])
        results = processor.post_process_object_detection(outputs=outputs, threshold = 0.5, target_sizes=target_sizes)

        boxes, scores, labels = results[0]["boxes"], results[0]["scores"], results[0]["labels"]
        
        yolo_string = ""
        for box, score, label in zip(boxes, scores, labels):
            box = [round(i, 2) for i in box.tolist()]
            literal = f"{text_list.index(text_list[label])} {box[0]} {box[1]} {box[2]} {box[3]}\n"
            yolo_string += literal

        image_key = bucket_details['baseFolder'] + date + "/" + bucket_details['images'] + image_name[0] + "."+ image_name[1]
        label_key = bucket_details['baseFolder'] + date + "/" + bucket_details['labels'] + image_name[0] + ".txt"
        
        image_byte_array = io.BytesIO()
        image.save(image_byte_array, format = "JPEG")
        image_byte_array.seek(0)

        image_upload = s3_client.put_object(Body=image_byte_array, Bucket=bucket_details['bucket'], Key =image_key)
        label_upload = s3_client.put_object(Body=yolo_string, Bucket=bucket_details['bucket'], Key = label_key)

        if image_upload is None and label_upload is not None:
            print("Could not upload file "+ image_name[0] + "."+ image_name[1])
            s3_client.delete_object(Bucket = bucket_details['bucket'], Key = label_key)
        
        if label_upload is None and image_upload is not None:
            print("Could not upload file "+ image_name[0] + ".txt")
            s3_client.delete_object(Bucket = bucket_details['bucket'], Key = image_key)
        
        if image_upload is None and label_upload is None:
            print("Could not upload file " + image_name[0] + "." + image_name[1]+", "+ image_name[0] + ".txt")
        
        if image_upload is not None and label_upload is not None:
            total_images_processed +=1
    
    return [len(images), total_images_processed, bucket_details['bucket_url']+ date+"/"]
        
def check_if_url_is_openable(url):
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        return response
    else:
        return None
    
@csrf_exempt
def health_check(request):
    if request.method == 'GET':
        print("GET ping health check")
        print(request)

    return HttpResponse(status=200)
