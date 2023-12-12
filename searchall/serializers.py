from rest_framework import serializers
from accounts.models import Course
#course search serializer
class CourseSearch(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'