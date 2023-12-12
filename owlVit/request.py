import boto3
import json
client = boto3.client('sagemaker-runtime')

# custom_attributes = "c000b4f9-df62-4c85-a0bf-7c525f9104a4"  # An example of a trace ID.
endpoint_name = "owlvitbackend"                                       # Your endpoint name.
# content_type = "..."                                        # The MIME type of the input data in the request body.
# accept = "..."                                              # The desired MIME type of the inference in the response.
payload = {
    "image" : "https://drive.google.com/drive/folders/1TVoxeb6p_TEn0EUxVxhS_1zONfFuoUxo?usp=share_link",
    "text" : "a photo of a cat, a photo of a dog"
}
res_bytes = json.dumps(payload).encode('utf-8')
                                    
response = client.invoke_endpoint(
    EndpointName=endpoint_name, 
    # CustomAttributes=custom_attributes, 
    # ContentType=content_type,
    # Accept=accept,
    Body=res_bytes
    )

# print(response)
response_content = response['Body'].read().decode('utf-8')
parsed_response = json.loads(response_content)
print(parsed_response)