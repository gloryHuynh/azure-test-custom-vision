'''
Created on Apr 17, 2021

@author: Glory
'''
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time

class ComputerVision:
    '''
    Authenticate
    Authenticates your credentials and creates a client.
    '''
    subscription_key = "f420a42ae90a49949daf9255f43a2aba"
    subscription_key2 = "f137d0cc53604d10887b37196e5c009a"
    endpoint = "https://alchamera-computer-vision-instance-1.cognitiveservices.azure.com/"
    
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    remote_image_url = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/landmark.jpg"

    def __init__(self):
        '''
        Constructor
        '''
    
    def getImageDescription(self):
        '''
        Describe an Image - remote
        This example describes the contents of an image with the confidence score.
        '''
        print("===== Describe an image - remote =====")
        # Call API
        description_results = self.computervision_client.describe_image(self.remote_image_url )
        
        # Get the captions (descriptions) from the response, with confidence level
        print("Description of remote image: ")
        if (len(description_results.captions) == 0):
            print("No description detected.")
        else:
            for caption in description_results.captions:
                print("'{}' with confidence {:.2f}%".format(caption.text, caption.confidence * 100))
    
    def getImageCategory(self):
        '''
        Categorize an Image - remote
        This example extracts (general) categories from a remote image with a confidence score.
        '''
        print("===== Categorize an image - remote =====")
        # Select the visual feature(s) you want.
        remote_image_features = ["categories"]
        # Call API with URL and features
        categorize_results_remote = self.computervision_client.analyze_image(self.remote_image_url , remote_image_features)
        
        # Print results with confidence score
        print("Categories from remote image: ")
        if (len(categorize_results_remote.categories) == 0):
            print("No categories detected.")
        else:
            for category in categorize_results_remote.categories:
                print("'{}' with confidence {:.2f}%".format(category.name, category.score * 100))
        
    def getImageTags(self):
        '''
        Tag an Image - remote
        This example returns a tag (key word) for each thing in the image.
        '''
        print("===== Tag an image - remote =====")
        # Call API with remote image
        tags_result_remote = self.computervision_client.tag_image(self.remote_image_url )
        
        # Print results with confidence score
        print("Tags in the remote image: ")
        if (len(tags_result_remote.tags) == 0):
            print("No tags detected.")
        else:
            for tag in tags_result_remote.tags:
                print("'{}' with confidence {:.2f}%".format(tag.name, tag.confidence * 100))
    
    def detectObjects(self):
        '''
        Detect Objects - remote
        This example detects different kinds of objects with bounding boxes in a remote image.
        '''
        print("===== Detect Objects - remote =====")
        # Get URL image with different objects
        remote_image_url_objects = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/objects.jpg"
        # Call API with URL
        detect_objects_results_remote = self.computervision_client.detect_objects(remote_image_url_objects)
        
        # Print detected objects results with bounding boxes
        print("Detecting objects in remote image:")
        if len(detect_objects_results_remote.objects) == 0:
            print("No objects detected.")
        else:
            for object in detect_objects_results_remote.objects:
                print("object at location {}, {}, {}, {}".format( \
                object.rectangle.x, object.rectangle.x + object.rectangle.w, \
                object.rectangle.y, object.rectangle.y + object.rectangle.h))
        
    def detectBrands(self):
        '''
        Detect Brands - remote
        This example detects common brands like logos and puts a bounding box around them.
        '''
        print("===== Detect Brands - remote =====")
        # Get a URL with a brand logo
        remote_image_url = "https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/images/gray-shirt-logo.jpg"
        # Select the visual feature(s) you want
        remote_image_features = ["brands"]
        # Call API with URL and features
        detect_brands_results_remote = self.computervision_client.analyze_image(remote_image_url, remote_image_features)
        
        print("Detecting brands in remote image: ")
        if len(detect_brands_results_remote.brands) == 0:
            print("No brands detected.")
        else:
            for brand in detect_brands_results_remote.brands:
                print("'{}' brand detected with confidence {:.1f}% at location {}, {}, {}, {}".format( \
                brand.name, brand.confidence * 100, brand.rectangle.x, brand.rectangle.x + brand.rectangle.w, \
                brand.rectangle.y, brand.rectangle.y + brand.rectangle.h))
    
    def detectFaces(self):
        '''
        Detect Faces - remote
        This example detects faces in a remote image, gets their gender and age, 
        and marks them with a bounding box.
        '''
        print("===== Detect Faces - remote =====")
        # Get an image with faces
        remote_image_url_faces = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/faces.jpg"
        # Select the visual feature(s) you want.
        remote_image_features = ["faces"]
        # Call the API with remote URL and features
        detect_faces_results_remote = self.computervision_client.analyze_image(remote_image_url_faces, remote_image_features)
        
        # Print the results with gender, age, and bounding box
        print("Faces in the remote image: ")
        if (len(detect_faces_results_remote.faces) == 0):
            print("No faces detected.")
        else:
            for face in detect_faces_results_remote.faces:
                print("'{}' of age {} at location {}, {}, {}, {}".format(face.gender, face.age, \
                face.face_rectangle.left, face.face_rectangle.top, \
                face.face_rectangle.left + face.face_rectangle.width, \
                face.face_rectangle.top + face.face_rectangle.height))
        
    def detectAdultRacyGoryContent(self):
        '''
        Detect Adult or Racy Content - remote
        This example detects adult or racy content in a remote image, then prints the adult/racy score.
        The score is ranged 0.0 - 1.0 with smaller numbers indicating negative results.
        '''
        print("===== Detect Adult or Racy Content - remote =====")
        # Select the visual feature(s) you want
        remote_image_features = ["adult"]
        # Call API with URL and features
        detect_adult_results_remote = self.computervision_client.analyze_image(self.remote_image_url, remote_image_features)
        
        # Print results with adult/racy score
        print("Analyzing remote image for adult or racy content ... ")
        print("Is adult content: {} with confidence {:.2f}".format(detect_adult_results_remote.adult.is_adult_content, detect_adult_results_remote.adult.adult_score * 100))
        print("Has racy content: {} with confidence {:.2f}".format(detect_adult_results_remote.adult.is_racy_content, detect_adult_results_remote.adult.racy_score * 100))
        
    def getImageColorScheme(self):
        '''
        Detect Color - remote
        This example detects the different aspects of its color scheme in a remote image.
        '''
        print("===== Detect Color - remote =====")
        # Select the feature(s) you want
        remote_image_features = ["color"]
        # Call API with URL and features
        detect_color_results_remote = self.computervision_client.analyze_image(self.remote_image_url, remote_image_features)
        
        # Print results of color scheme
        print("Getting color scheme of the remote image: ")
        print("Is black and white: {}".format(detect_color_results_remote.color.is_bw_img))
        print("Accent color: {}".format(detect_color_results_remote.color.accent_color))
        print("Dominant background color: {}".format(detect_color_results_remote.color.dominant_color_background))
        print("Dominant foreground color: {}".format(detect_color_results_remote.color.dominant_color_foreground))
        print("Dominant colors: {}".format(detect_color_results_remote.color.dominant_colors))

    def getDomainSpecificContent(self):
        '''
        Detect Domain-specific Content - remote
        This example detects celebrites and landmarks in remote images.
        '''
        print("===== Detect Domain-specific Content - remote =====")
        # URL of one or more celebrities
        remote_image_url_celebs = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/faces.jpg"
        # Call API with content type (celebrities) and URL
        detect_domain_results_celebs_remote = self.computervision_client.analyze_image_by_domain("celebrities", remote_image_url_celebs)
        
        # Print detection results with name
        print("Celebrities in the remote image:")
        if len(detect_domain_results_celebs_remote.result["celebrities"]) == 0:
            print("No celebrities detected.")
        else:
            for celeb in detect_domain_results_celebs_remote.result["celebrities"]:
                print(celeb["name"])
        # Call API with content type (landmarks) and URL
        detect_domain_results_landmarks = self.computervision_client.analyze_image_by_domain("landmarks", self.remote_image_url)
        print()
        
        print("Landmarks in the remote image:")
        if len(detect_domain_results_landmarks.result["landmarks"]) == 0:
            print("No landmarks detected.")
        else:
            for landmark in detect_domain_results_landmarks.result["landmarks"]:
                print(landmark["name"])
    
    def getImageType(self):
        '''
        Detect Image Types - remote
        This example detects an image's type (clip art/line drawing).
        '''
        print("===== Detect Image Types - remote =====")
        # Get URL of an image with a type
        remote_image_url_type = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/type-image.jpg"
        # Select visual feature(s) you want
        remote_image_features = [VisualFeatureTypes.image_type]
        # Call API with URL and features
        detect_type_results_remote = self.computervision_client.analyze_image(remote_image_url_type, remote_image_features)
        
        # Prints type results with degree of accuracy
        print("Type of remote image:")
        if detect_type_results_remote.image_type.clip_art_type == 0:
            print("Image is not clip art.")
        elif detect_type_results_remote.image_type.line_drawing_type == 1:
            print("Image is ambiguously clip art.")
        elif detect_type_results_remote.image_type.line_drawing_type == 2:
            print("Image is normal clip art.")
        else:
            print("Image is good clip art.")
        
        if detect_type_results_remote.image_type.line_drawing_type == 0:
            print("Image is not a line drawing.")
        else:
            print("Image is a line drawing")