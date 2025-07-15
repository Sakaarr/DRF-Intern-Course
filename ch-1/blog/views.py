from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Blog
from .serializers import BlogSerializer
from drf_spectacular.utils import extend_schema
from rest_framework import generics

# Create your views here.
#API VIEW =  DRF's way of building class based views


# CRUD  - Create(POST), Read(GET), Update(PUT(All fields edit)/PATCH(Particular Fields Edit)), Delete(DELETE)

# username , email, password, first_name, last_name

# class BlogList(APIView):
#     @extend_schema(
#         summary="List all blogs",
#         responses={200: BlogSerializer(many=True), 201: BlogSerializer, 400: "Bad Request"}
#     )
#     def get(self,request):
#         blogs = Blog.objects.all()
#         serializer = BlogSerializer(blogs, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK) 
    
     
#     @extend_schema(
#         summary="Create a new Blog",
#         request=BlogSerializer,
#         responses=BlogSerializer
#     )
#     def post(self,request):
#         serializer = BlogSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()#Save to database
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@extend_schema(request=BlogSerializer, responses=BlogSerializer)           
class BlogListCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    
@extend_schema(request=BlogSerializer, responses=BlogSerializer)  
class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer