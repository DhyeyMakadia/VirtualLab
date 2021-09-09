from rest_framework import serializers

from User.models import Account


class RegistrationSerializer(serializers.ModelSerializer):
    # Another password attribute for two time password verification.
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        # Model to be serialized
        model = Account
        # fields of the serializer.
        fields = ['email', 'password', 'password2', 'is_admin']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        # Getting an instance of the model with validated data.
        # university = University.objects.get(id=self.validated_data['university'])
        account = Account(
            email=self.validated_data['email'],
            is_admin=self.validated_data['is_admin']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        # Checking whether the two passwords match.
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        # Setting the password if two passwords match
        account.set_password(password)
        # Saving the instance to the database, and return it.
        account.save()
        return account
