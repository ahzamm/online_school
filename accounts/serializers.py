from rest_framework import serializers
from accounts.models import Admin, Student, Teacher, User


class AdminRegisterationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Admin
        fields = ['email', 'name', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match")
        return data

    def create(self, validated_data):
        return Admin.objects.create_user(**validated_data)


class TeacherRegisterationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Teacher
        fields = ['email', 'name', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match")
        return data

    def create(self, validated_data):
        return Teacher.objects.create_user(**validated_data)


class StudentRegisterationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Student
        fields = ['email', 'name', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match")
        return data

    def create(self, validated_data):
        return Student.objects.create_user(**validated_data)


class AdminLoginSerializer(serializers.ModelSerializer):
    # serializer only see that we are sending post request so it throw "email is
    # already register" thats why we have to initilize extra email field
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = Admin
        fields = ['email', 'password']


class TeacherLoginSerializer(serializers.ModelSerializer):
    # serializer only see that we are sending post request so it throw "email is
    # already register" thats why we have to initilize extra email field
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = Teacher
        fields = ['email', 'password']


class StudentLoginSerializer(serializers.ModelSerializer):
    # serializer only see that we are sending post request so it throw "email is
    # already register" thats why we have to initilize extra email field
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = Student
        fields = ['email', 'password']


class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id', 'email', 'name']


class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'email', 'name']


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'email', 'name']


class AdminChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')

        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match")
        user = self.context.get('user')
        user.set_password(password)
        user.save()
        return data


class TeacherChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')

        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match")
        user = self.context.get('user')
        user.set_password(password)
        user.save()
        return data


class StudentChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')

        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match")
        user = self.context.get('user')
        user.set_password(password)
        user.save()
        return data


class AdminChangeTeacherStudentPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        password2 = data.get('password2')

        user = User.objects.filter(email=email).first()
        if user is None:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match")

        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match")

        user.set_password(password)
        user.save()
        return data
