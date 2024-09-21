from rest_framework import viewsets 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializer import HealthEntrySerializer
from mysite.network.neuralNetwork import main
from rest_framework.exceptions import ValidationError

#commands
#pip install djangorestframework

#Chethin calls get (to get data) and set (to send data)
#I call Billys function in get API
class API(APIView):
    def get(self, request): 
        health_entries = request.data
        if not health_entries:
            raise ValidationError("No data provided")
            # return Response(status=status.HTTP_400_BAD_REQUEST)
        serialized_entries = []
        for entry in health_entries:
            serializer = HealthEntrySerializer(data=entry)
            serialized_entries.append(serializer.data)
        result = main(serialized_entries)  #obtain 
        # # This handles a GET API call
        response_data = {
            'actions': result[0], #list of numbers associated with each action 
            'prediction': result[1]
        }
        new_health_entry = {
            "cream1": response_data["actions"][0],
            "cream2": response_data["actions"][1],
            "tookHotShower": response_data["actions"][2],
            "relativeHumidity": response_data["actions"][3],
            "stress": response_data["actions"][4],
            "facewash1": response_data["actions"][5],
            "facewash2": response_data["actions"][6],
            "makeup": response_data["actions"][7],
            "soap": response_data["actions"][8],
            "hoursInside": response_data["actions"][9],
            "skinFeelRating": response_data["prediction"]
        }
        return Response(new_health_entry, status=status.HTTP_200_OK)
    


    # def post(self, request):
    #     # This handles a POST API call 
    #     health_entries = request.data
    #     serialized_entries = []
    #     for entry in health_entries:
    #         serializer = HealthEntrySerializer(data=entry)
    #         serialized_entries.append(serializer.data)
    #     main(serialized_entries)
    #     return Response(status=status.HTTP_200_OK)  #TODO - add check for bad request 