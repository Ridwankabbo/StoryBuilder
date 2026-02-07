from rest_framework import serializers
from .models import User
from .utils import generateOTP


""" ********************** User registration serializer *************************** """
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        
    def create(self, validate_data):
            
        try:
            user = User.objects.create_user(
            email = validate_data.get('email'),
            username = validate_data.get('username'),
            password = validate_data.get('password')
            )
            verification_otp = generateOTP()
            print('verification otp', verification_otp)
            user.otp=verification_otp
            user.save()
            # print('verificatin_otp', user.otp)
        except AttributeError:
            raise ValueError(
                {"detail":"otp not found"}
            )
                
        return user