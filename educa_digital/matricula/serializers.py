# matricula/serializers.py
from rest_framework import serializers
from .models import (
    StudentProfile, ResponsibleProfile, Address, SchoolUnit,
    Enrollment, EnrollmentDocuments
)

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = '__all__'


class ResponsibleProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponsibleProfile
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class SchoolUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolUnit
        fields = '__all__'


class EnrollmentDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrollmentDocuments
        fields = '__all__'


class EnrollmentSerializer(serializers.ModelSerializer):
    student = StudentProfileSerializer()
    responsible = ResponsibleProfileSerializer()
    address = AddressSerializer()
    school_unit = SchoolUnitSerializer(required=False, allow_null=True)

    class Meta:
        model = Enrollment
        fields = '__all__'

    def create(self, validated_data):
        student_data = validated_data.pop('student')
        responsible_data = validated_data.pop('responsible')
        address_data = validated_data.pop('address')
        school_unit_data = validated_data.pop('school_unit', None)

        # Se o aluno já existir (pelo CPF), atualiza; caso contrário, cria
        student, _ = StudentProfile.objects.get_or_create(cpf=student_data['cpf'], defaults=student_data)
        responsible, _ = ResponsibleProfile.objects.get_or_create(cpf=responsible_data['cpf'], defaults=responsible_data)
        address = Address.objects.create(**address_data)
        school_unit = None
        if school_unit_data:
            school_unit, _ = SchoolUnit.objects.get_or_create(**school_unit_data)

        enrollment = Enrollment.objects.create(
            student=student,
            responsible=responsible,
            address=address,
            school_unit=school_unit,
            **validated_data
        )
        return enrollment

    def update(self, instance, validated_data):
        student_data = validated_data.pop('student', None)
        responsible_data = validated_data.pop('responsible', None)
        address_data = validated_data.pop('address', None)
        school_unit_data = validated_data.pop('school_unit', None)

        if student_data:
            for attr, value in student_data.items():
                setattr(instance.student, attr, value)
            instance.student.save()

        if responsible_data:
            for attr, value in responsible_data.items():
                setattr(instance.responsible, attr, value)
            instance.responsible.save()

        if address_data:
            for attr, value in address_data.items():
                setattr(instance.address, attr, value)
            instance.address.save()

        if school_unit_data:
            school_unit, _ = SchoolUnit.objects.get_or_create(**school_unit_data)
            instance.school_unit = school_unit

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
