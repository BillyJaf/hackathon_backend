from rest_framework import viewsets 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializer import HealthEntrySerializer

#commands
#pip install djangorestframework

#Chethin calls get (to get data) and set (to send data)
#I call Billys function in get API
class ModelAPIView(APIView):
    def get(self, request): 
        # This handles a GET API call
        result = main() #TODO - fix 
        response_data = {
            'actions': result[0], #list of numbers associated with each action 
            'prediction': result[1]
        }
        health_entry = {
            "id": null,
            "cream1": actions[0],
            "cream2": actions[1],
            "tokHotShower": actions[2],
            "relativeHumidity": actions[3],
            "stress": actions[4],
            "facewash1": actions[5],
            "facewash2": actions[6],
            "makeup": actions[7],
            "soap": actions[8],
            "hoursInside": actions[9],
            "skinFeelRating": prediction
        }
        return Response(health_entry, status=status.HTTP_200_OK)
    def post(self, request):
        # This handles a POST API call 
        health_entries = request.data
        serialized_entries = []
        for entry in health_entries:
            serializer = HealthEntrySerializer(data=entry)
            serialized_entries.append(serializer.data)
        main(serialized_entries)
        return Response(status=status.HTTP_200_OK)  #TODO - add check for bad request 