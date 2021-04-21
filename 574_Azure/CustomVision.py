'''
Created on Apr 17, 2021

@author: Glory
'''
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os, time, uuid

class CustomVision(object):
    '''
    Authenticate
    Authenticates your credentials and creates a client.
    '''
    # Replace with valid values
    ENDPOINT = "https://alchamera-custom-vision-instance.cognitiveservices.azure.com/"
    ENDPOINT2 = "https://alchameracustomvis-prediction.cognitiveservices.azure.com/"
    training_key = "7cdf1c4ad1c5416389377d2940ed1a45"
    prediction_key = "f9c451de116e49de991da2d03767e4d0"
    prediction_resource_id = "/subscriptions/df7b57fe-a8c7-4296-9cb8-460b47d76ba2/resourceGroups/computer_vision_1/providers/Microsoft.CognitiveServices/accounts/alchameracustomvis-Prediction"

    def __init__(self):
        '''
        Constructor
        '''

    def runExample(self):
        # <snippet_creds>
        # Replace with valid values
        ENDPOINT = "https://alchamera-custom-vision-instance.cognitiveservices.azure.com/"
        training_key = "7cdf1c4ad1c5416389377d2940ed1a45"
        prediction_key = "7cdf1c4ad1c5416389377d2940ed1a45"
        prediction_resource_id = "/subscriptions/df7b57fe-a8c7-4296-9cb8-460b47d76ba2/resourceGroups/computer_vision_1/providers/Microsoft.CognitiveServices/accounts/alchamera-custom-vision-instance"
        # </snippet_creds>
        
        # <snippet_auth>
        credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
        trainer = CustomVisionTrainingClient(ENDPOINT, credentials)
        prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
        predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)
        # </snippet_auth>
        
        # <snippet_create>
        publish_iteration_name = "classifyModel"
        
        credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
        trainer = CustomVisionTrainingClient(ENDPOINT, credentials)
        
        # Create a new project
        print ("Creating project...")
        project_name = uuid.uuid4()
        project = trainer.create_project(project_name)
        # </snippet_create>
        
        # <snippet_tags>
        # Make two tags in the new project
        hemlock_tag = trainer.create_tag(project.id, "Hemlock")
        cherry_tag = trainer.create_tag(project.id, "Japanese Cherry")
        # </snippet_tags>
        
        # <snippet_upload>
        # You can get the images for this sample at:
        # https://github.com/Azure-Samples/cognitive-services-sample-data-files/tree/master/CustomVision/ImageClassification/Images
        base_image_location = 'C:\\Users\\Glory\\Desktop\\C# Book\\Universities\\Spring2021\\574\\cognitive-services-sample-data-files-master\\CustomVision\\ImageClassification\\Images'
        
        print("Adding images...")
        
        image_list = []
        
        for image_num in range(1, 11):
            file_name = "hemlock_{}.jpg".format(image_num)
            with open(os.path.join (base_image_location, "Hemlock", file_name), "rb") as image_contents:
                image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[hemlock_tag.id]))
        
        for image_num in range(1, 11):
            file_name = "japanese_cherry_{}.jpg".format(image_num)
            with open(os.path.join (base_image_location, "Japanese Cherry", file_name), "rb") as image_contents:
                image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[cherry_tag.id]))
        
        upload_result = trainer.create_images_from_files(project.id, ImageFileCreateBatch(images=image_list))
        if not upload_result.is_batch_successful:
            print("Image batch upload failed.")
            for image in upload_result.images:
                print("Image status: ", image.status)
            exit(-1)
        # </snippet_upload>
        
        # <snippet_train>
        print ("Training...")
        iteration = trainer.train_project(project.id)
        while (iteration.status != "Completed"):
            iteration = trainer.get_iteration(project.id, iteration.id)
            print ("Training status: " + iteration.status)
            print ("Waiting 10 seconds...")
            time.sleep(10)
        # </snippet_train>
        
        # <snippet_publish>
        # The iteration is now trained. Publish it to the project endpoint
        trainer.publish_iteration(project.id, iteration.id, publish_iteration_name, prediction_resource_id)
        print ("Done!")
        # </snippet_publish>
        
        # <snippet_test>
        # Now there is a trained endpoint that can be used to make a prediction
        prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
        predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)
        for image_num in range(1, 10):
            file_name = "test_{}.jpeg".format(image_num)
            with open(os.path.join (base_image_location, "Test", file_name), "rb") as image_contents:
                results = predictor.classify_image(project.id, publish_iteration_name, image_contents.read())
                for prediction in results.predictions:
                    print("\t" + prediction.tag_name +
                      ": {0:.2f}%".format(prediction.probability * 100))
        # </snippet_test>
        
        # <snippet_delete>
        # You cannot delete a project with published iterations, so you must first unpublish them.
        print ("Unpublishing project...")
        trainer.unpublish_iteration(project.id, iteration.id)
        
        print ("Deleting project...")
        trainer.delete_project (project.id)
        # </snippet_delete>
    
    def run(self):
        publish_iteration_name = "classifyModel"

        credentials = ApiKeyCredentials(in_headers={"Training-key": self.training_key})
        trainer = CustomVisionTrainingClient(self.ENDPOINT, credentials)
        
        # Create a new project
        print ("Creating project...")
        project_name = uuid.uuid4()
        project = trainer.create_project(project_name)
        
        # Make two tags in the new project
        hemlock_tag = trainer.create_tag(project.id, "Hemlock")
        cherry_tag = trainer.create_tag(project.id, "Japanese Cherry")
        
        # You can get the images for this sample at:
        # https://github.com/Azure-Samples/cognitive-services-sample-data-files/tree/master/CustomVision/ImageClassification/Images
        base_image_location = 'C:\\Users\\Glory\\Desktop\\C# Book\\Universities\\Spring2021\\574\\cognitive-services-sample-data-files-master\\CustomVision\\ImageClassification\\Images'
        
        print("Adding images...")
        
        image_list = []
        
        for image_num in range(1, 11):
            file_name = "hemlock_{}.jpg".format(image_num)
            with open(os.path.join (base_image_location, "Hemlock", file_name), "rb") as image_contents:
                image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[hemlock_tag.id]))
        
        for image_num in range(1, 11):
            file_name = "japanese_cherry_{}.jpg".format(image_num)
            with open(os.path.join (base_image_location, "Japanese Cherry", file_name), "rb") as image_contents:
                image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[cherry_tag.id]))
        
        upload_result = trainer.create_images_from_files(project.id, ImageFileCreateBatch(images=image_list))
        if not upload_result.is_batch_successful:
            print("Image batch upload failed.")
            for image in upload_result.images:
                print("Image status: ", image.status)
            exit(-1)
            
        print ("Training...")
        start = time.time()
        iteration = trainer.train_project(project.id)
        while (iteration.status != "Completed"):
            iteration = trainer.get_iteration(project.id, iteration.id)
#             print ("Training status: " + iteration.status)
#             print ("Waiting 10 seconds...")
#             time.sleep(10)
        end = time.time()
        print("Resulting time:")
        print(end-start)
        # The iteration is now trained. Publish it to the project endpoint
        trainer.publish_iteration(project.id, iteration.id, publish_iteration_name, self.prediction_resource_id)
        print ("Done!")
        
    def predict(self):
        # Now there is a trained endpoint that can be used to make a prediction
        predictionEndpoint = "https://alchamera-custom-vision-instance.cognitiveservices.azure.com/customvision/v3.0/Prediction/33c5edf7-92c5-4b42-a306-7c04c3e2590e/classify/iterations/classifyModel/image"
        predictionKey = "f9c451de116e49de991da2d03767e4d0"
        
        prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": predictionKey})
        predictor = CustomVisionPredictionClient(predictionEndpoint, prediction_credentials)
        
        base_image_location = 'C:\\Users\\Glory\\Desktop\\C# Book\\Universities\\Spring2021\\574\\cognitive-services-sample-data-files-master\\CustomVision\\ImageClassification\\Images'
        projectId = "8beae23fc-1a07-40a8-9a56-c743c32449a5"
        iterationName = "beae23fc-1a07-40a8-9a56-c743c32449a5"
        for image_num in range(1, 10):
            file_name = "test_{}.jpeg".format(image_num)
            with open(os.path.join (base_image_location, "Test", file_name), "rb") as image_contents:
                results = predictor.classify_image(projectId, iterationName, image_contents.read())
                for prediction in results.predictions:
                    print("\t" + prediction.tag_name +
                      ": {0:.2f}%".format(prediction.probability * 100))
        
        
        
    
    
        