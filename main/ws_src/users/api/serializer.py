from rest_framework import serializers

# from ws_src.users.models import User


class UserTextSerializer(serializers.Serializer):
    text = serializers.CharField()
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
