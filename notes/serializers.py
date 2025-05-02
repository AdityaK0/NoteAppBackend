from rest_framework.serializers import ModelSerializer,ReadOnlyField
from .models import Notes


class NotesSerializers(ModelSerializer):
    user = ReadOnlyField(source="user.id")  
    username = ReadOnlyField(source="user.username")
    class Meta:
        model = Notes
        fields = [  
            "id",
            "title",
            "description",
            "category",
            "ispinned",
            "tags",
            "created_at",
            "updated_at",
            "user",  
            "username"
        ]

    def create(self, validated_data):
        user = validated_data.pop("user")
        note = Notes.objects.create(user=user,**validated_data)
        return note 

