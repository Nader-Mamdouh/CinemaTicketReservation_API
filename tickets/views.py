from django.shortcuts import get_object_or_404, render
from django.http.response import JsonResponse
from .models import Guest, Movie, Reservation
from rest_framework.decorators import api_view
from .serializers import GuestSerializer, MovieSerializer, ReservationSerializer
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins, generics, viewsets
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# 1 No Rest No Models


def NRNM(request):
    guests = [
        {
            'id': 1,
            "name": "omar",
            "phone": "0198923"
        }
    ]
    return JsonResponse(guests, safe=False)

# 2 No Rest With Models


def NRWM(request):
    data = Guest.objects.all()
    response = {
        'guests': list(data.values('name', 'phone'))
    }
    return JsonResponse(response)


# 3
# function based view GET POST
@api_view(['GET', 'POST'])
def FBV_LIST(request):
    # GET
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)
    # POST
    elif request.method == 'POST':
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE', 'GET'])
def FBV_pk(request, pk):
    guest = get_object_or_404(Guest, pk=pk)
    # GET
    if request.method == 'GET':
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    # PUT
    elif request.method == 'PUT':
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # DELETE
    elif request.method == 'DELETE':
        guest.delete()
        return Response({'message': 'Guest deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# 4
# CBV class based view
class CBV_LIST(APIView):
    def get(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class CBV_PK(APIView):
    def get_object(self, pk):
        guest = get_object_or_404(Guest, pk=pk)
        return guest

    # GET

    def get(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    # PUT

    def put(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response({'message': 'Guest deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# 5 Mixins
# 5.1 Mixins List
class mixins_list(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)

# 5.2 Mixins get,put,delete


class mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk=pk)

    def put(self, request, pk):
        return self.update(request, pk=pk)

    def delete(self, request, pk):
        return self.delete(request, pk=pk)


# 6 Generics
# 6.1 Henerics-list
class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]  # ✅ FIXED
    permission_classes = [IsAuthenticated]

# 6.2


class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


# 7 ViewSet


class viewsets_guests(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class viewsets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


# 8
# Find Movie
@api_view(["GET"])
def find_movie(request):
    movies = Movie.objects.filter(
        hall=request.data["hall"],
        movie=request.data["movie"]
    )
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

# 9
# New Reservation


@api_view(["POST"])
def reserve(request):
    movie = Movie.objects.get(
        hall=request.data["hall"],
        movie=request.data["movie"]
    )
    guest = Guest()
    guest.name = request.data["name"]
    guest.phone = request.data["phone"]
    guest.save()
    reserve = Reservation()
    reserve.movie = movie
    reserve.guest = guest
    reserve.save()
    serializer = ReservationSerializer(reserve)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
