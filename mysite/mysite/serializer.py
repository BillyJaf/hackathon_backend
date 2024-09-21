# serializers.py
from rest_framework import serializers
# myapp/serializers.py
from rest_framework import serializers

class HealthEntrySerializer(serializers.Serializer):
    cream1 = serializers.FloatField()
    cream2 = serializers.FloatField()
    tookHotShower = serializers.FloatField()
    relativeHumidity = serializers.FloatField()
    stress = serializers.FloatField()
    facewash1 = serializers.FloatField()
    facewash2 = serializers.FloatField()
    makeup = serializers.FloatField()
    soap = serializers.FloatField()
    hoursInside = serializers.FloatField()
    skinFeelRating = serializers.FloatField()

    def to_representation(self, instance):
        # Convert to the required format: list of floats and skinFeelRating
        actionsTaken = [
            instance['cream1'],
            instance['cream2'],
            instance['tookHotShower'],
            instance['relativeHumidity'],
            instance['stress'],
            instance['facewash1'],
            instance['facewash2'],
            instance['makeup'],
            instance['soap'],
            instance['hoursInside'],
        ]
        
        return {
            'x': actionsTaken,
            'y': instance['skinFeelRating']
        }


        