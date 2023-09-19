from pypdf import PdfReader

number_of_resume = int(input("Enter the number of resumes: "))
PAT = '5cae2492009e4903b6ee196cf618df60'
USER_ID = 'openai'
APP_ID = 'chat-completion'
MODEL_ID = 'GPT-4'
MODEL_VERSION_ID = 'ad16eda6ac054796bf9f348ab6733c72'

arr = []

for i in range(0, number_of_resume):
  reader = PdfReader("Profile"+str(i)+".pdf")
  number_of_pages = len(reader.pages)
  page = reader.pages[0]
  text = page.extract_text()
  arr.append(text)
  
arr.append('''I am a recruiter and i have a few resumes, and i want you to make sure that the conditions i specify are satisfied in it. and then rate it out of 10 and specify the best.
Conditions are:
1.) Skills
2.) Education
3.) Certification
4.) Projects
5.) Extra-Curriculur''')

for i in arr:
  RAW_TEXT = RAW_TEXT + i

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)

metadata = (('authorization', 'Key ' + PAT),)

userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

def func(raw_text) -> str:
  post_model_outputs_response = stub.PostModelOutputs(
      service_pb2.PostModelOutputsRequest(
          user_app_id=userDataObject,
          model_id=MODEL_ID,
          version_id=MODEL_VERSION_ID,
          inputs=[
              resources_pb2.Input(
                  data=resources_pb2.Data(
                      text=resources_pb2.Text(
                          raw=raw_text
                      )
                  )
              )
          ]
      ),
      metadata=metadata
  )
  if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
      print(post_model_outputs_response.status)
      raise Exception(f"Post model outputs failed, status: {post_model_outputs_response.status.description}")

  output = post_model_outputs_response.outputs[0]

  return output.data.text.raw

print(func(RAW_TEXT))
