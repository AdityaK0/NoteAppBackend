from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status  
from .models import Notes
from .serializers import NotesSerializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.db.models import Q

def home(request):
    return HttpResponse("<small>Api Notes Response System</small>")

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def allList(request):
    try:
        all_notes = Notes.objects.all().filter(user=request.user).order_by('-ispinned')
        serialized_notes = NotesSerializers(all_notes, many=True) 
        
        return Response(
            {"message": "All Data", "all_notes": serialized_notes.data},  
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {"error": str(e)},  
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_note(request):
    try:
        noteData = NotesSerializers(data=request.data)
        print("Current User ",request.user)
        if noteData.is_valid():
            noteData.save(user=request.user)

            return Response(noteData.data,status=status.HTTP_201_CREATED)
        return Response(noteData.errors,status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        raise Exception(e)
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_note(request, id):
    try:
        note = Notes.objects.get(id=id, user=request.user)  
        serializer = NotesSerializers(note)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Notes.DoesNotExist:
        return Response({"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["PUT","PATCH"])
@permission_classes([IsAuthenticated])
def update_note(request,id):
    try:
        note = Notes.objects.get(id=id,user=request.user)
        serializer = NotesSerializers(note,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":f"{e}"},status=status.HTTP_400_BAD_REQUEST)        


@api_view(["PUT","PATCH"])
@permission_classes([IsAuthenticated])
def pin_note(request,id):
    try:
       note = Notes.objects.get(id=id,user=request.user)
       serializer = NotesSerializers(note,data=request.data,partial=True)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data,status=status.HTTP_200_OK)
       return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)       
    except Exception as e:
        return Response({"error":f"{e}"},status=status.HTTP_400_BAD_REQUEST) 

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_note(request,id):
    try:
        note =  Notes.objects.get(id=id,user=request.user)
        note.delete()
        return Response({"message":"Note deleted successfully"},status=status.HTTP_200_OK)
    except Notes.DoesNotExist:
        return Response({"error":"Note not found"},status=status.HTTP_404_NOT_FOUND)
    


@api_view(["POST","GET"])
@permission_classes([IsAuthenticated])
def search_notes(request):
    try:
        if len(str(request.GET.get("query")).strip())>0:
            querry = request.GET.get("query")
            data = Notes.objects.filter(user=request.user).filter(
                Q(title__icontains = querry) | Q( description__icontains = querry) | Q(category__icontains = querry)
            ).order_by("-ispinned").values()
            serializer = NotesSerializers(data,many=True)
            return Response({"all_notes":serializer.data},status=status.HTTP_200_OK)
        return Response({"error":"Search Querry is required"},status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":f"Note not found {e}"},status=status.HTTP_404_NOT_FOUND) 