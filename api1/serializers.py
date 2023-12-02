from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import ValidationError
from .models import User



class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80)
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        
        email_exists = User.objects.filter(email=attrs['email']).exists()

        if email_exists:
            raise ValidationError('Este endereço de email já está sendo usado')

        return super().validate(attrs)


    def create(self, validated_data):
        password = validated_data.pop('password')

        user = super().create(validated_data)

        user.set_password(password)

        user.save()
        
        Token.objects.create(user=user)


        return user

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']


