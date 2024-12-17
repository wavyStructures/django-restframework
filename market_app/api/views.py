from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MarketSerializer

@api_view(['GET', 'POST'])
def markets_view(request):
    
    
    
    if request.method == 'GET':
        return Response({"message": "Hello, world!"})
    if request.method == 'POST':
        try:
            msg = request.data['message']
            return Response({"message": msg}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({"message": "No message provided"}, status=status.HTTP_400_BAD_REQUEST)