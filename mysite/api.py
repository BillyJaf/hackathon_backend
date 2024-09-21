from rest_framework import viewsets 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializer import HealthEntrySerializer
from mysite.network.neuralNetwork import main
from rest_framework.exceptions import ValidationError

class API(APIView):
    def post(self, request): 
        health_entries = request.data
        if not health_entries:
            raise ValidationError("No data provided")
        print("Input: ", health_entries)
        serialized_entries = []
        for entry in health_entries:
            serializer = HealthEntrySerializer(data=entry)
            if not serializer.is_valid():
                return Response(serializer.errors, status=400)
            serialized_entries.append(serializer.data)
        print("Processed Data: ", serialized_entries)
        result = main(serialized_entries) 
        print("Result: ", result)
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