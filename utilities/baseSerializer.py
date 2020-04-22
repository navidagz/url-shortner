"""
BaseModelSerializer and BaseSerializer is created to make all serializer
errors have the same response format as other views
"""

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from utilities.http_code_handler import response_formatter


class BaseModelSerializer(serializers.ModelSerializer):
    non_field_errors = list()

    @property
    def errors(self):
        errors = super(BaseModelSerializer, self).errors
        self.non_field_errors = errors.get("non_field_errors")
        errors.pop("non_field_errors", None)

        return errors

    def is_valid(self, raise_exception=False):
        assert not hasattr(self, 'restore_object'), (
                'Serializer `%s.%s` has old-style version 2 `.restore_object()` '
                'that is no longer compatible with REST framework 3. '
                'Use the new-style `.create()` and `.update()` methods instead.' %
                (self.__class__.__module__, self.__class__.__name__)
        )

        assert hasattr(self, 'initial_data'), (
            'Cannot call `.is_valid()` as no `data=` keyword argument was '
            'passed when instantiating the serializer instance.'
        )

        if not hasattr(self, '_validated_data'):
            try:
                self._validated_data = self.run_validation(self.initial_data)
            except ValidationError as exc:
                self._validated_data = {}
                self._errors = exc.detail
            else:
                self._errors = {}

        if self._errors and raise_exception:
            raise ValidationError(response_formatter(400, errors=self.errors,
                                                     non_field_errors=self.non_field_errors))

        return not bool(self._errors)


class BaseSerializer(serializers.Serializer):
    non_field_errors = list()

    def update(self, instance, validated_data):
        ...

    def create(self, validated_data):
        ...

    @property
    def errors(self):
        errors = super(BaseSerializer, self).errors
        self.non_field_errors = errors.get("non_field_errors")
        errors.pop("non_field_errors", None)

        return errors

    def is_valid(self, raise_exception=False):
        assert not hasattr(self, 'restore_object'), (
                'Serializer `%s.%s` has old-style version 2 `.restore_object()` '
                'that is no longer compatible with REST framework 3. '
                'Use the new-style `.create()` and `.update()` methods instead.' %
                (self.__class__.__module__, self.__class__.__name__)
        )

        assert hasattr(self, 'initial_data'), (
            'Cannot call `.is_valid()` as no `data=` keyword argument was '
            'passed when instantiating the serializer instance.'
        )

        if not hasattr(self, '_validated_data'):
            try:
                self._validated_data = self.run_validation(self.initial_data)
            except ValidationError as exc:
                self._validated_data = {}
                self._errors = exc.detail
            else:
                self._errors = {}

        if self._errors and raise_exception:
            raise ValidationError(response_formatter(400, errors=self.errors, non_field_errors=self.non_field_errors))

        return not bool(self._errors)
