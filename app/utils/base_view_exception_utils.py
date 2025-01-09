class ApplicationException(Exception):
    def __init__(self, error_info, field=None, message="Something went wrong!", child_error=None,
                 exception_type="AppException"):
        super().__init__(f"{error_info} Error: Field '{field}' - {message}")

        self.exception_type = exception_type

        self.error_info = error_info
        self.field = field

        self.message = message

        self.child_error = child_error if child_error is not None else []

    def to_dict(self):
        return {
            "exception_type": self.exception_type,
            "field": self.field,
            "message": self.message,
            "error": f"Error: {self.error_info}",
            "child_error": self.child_error,
        }

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str(self.to_dict())


class AppExceptionHelper:
    # general exception as dictionary
    def format_exception(self, exception, exception_type, field=None):
        try:
            error_data = exception.to_dict()
        except AttributeError:
            error_data = str(exception)
        except Exception as exception:
            error_data = str(exception)

        new_child_error = []
        if isinstance(error_data, dict):
            if error_data.get('child_error') in (None, []):
                error_data.pop("child_error", None)
                new_child_error = [error_data]
            else:
                new_child_error = [error_data]
        else:
            new_child_error = [{
                "exception_type": exception_type,
                "field": field,
                "error": error_data,
                "message": "Something went wrong!"
            }]
        return new_child_error

    # TODO: to use with serializer validation error
    def format_serializer_validation_error(self, exception, error_info="serializers.ValidationError",
                                           exception_type="appValidationException"):
        error_dict = dict(exception.detail)
        child_errors = []

        for field, errors in error_dict.items():
            for error in errors:
                child_errors.append({
                    "exception_type": exception_type,
                    "field": field,
                    "message": str(error),
                    "error": error_info,
                })

        return child_errors

    def raise_serializer_validate_exception(self, field, exception, exception_type="AppValidationFailure"):
        try:
            new_child_error = self.format_exception(exception, exception.exception_type)
        except:
            new_child_error = str(exception)

        raise AppSerializerException(
            field=field,
            message=f"Failed to validate {field}.",
            exception_type=exception_type,
            error_info=f"Validation error occurred for '{field}'.",
            child_error=new_child_error
        )

    def raise_serializer_error(self, field, exception, exception_type="AppSerializerFailure"):
        try:
            child_errors = self.format_serializer_validation_error(exception=exception, exception_type=field)
        except:
            child_errors = f"field: {str(field)}, exception: {str(exception)}"
        raise AppSerializerException(
            field=field,
            message=f"{field} serialization encountered an error.",
            error_info=f"An error occurred while serializing {field} in {exception_type if exception_type else self.__class__.__name__}.",
            exception_type=exception_type if exception_type else self.__class__.__name__,
            child_error=child_errors
        )

    def raise_validate_required_field_error(self, field, exception_type=None):
        raise AppValidateException(
            field=field,
            message=f"{field.capitalize()} is required.",
            error_info="Missing Field",
            exception_type=exception_type
        )

    def raise_repository_instance_not_found_exception(self, field, exception_type="AppInstanceNotFound"):
        raise AppRepositoryException(
            field=field,
            message=f"Failed to retrieved a '{field}' due to a repository error.",
            error_info=f"The specified '{field}' instance was not found in the system.",
            exception_type=exception_type
        )

    def handle_char_validator(self, attr, field, max_length, exception_type="AppValidateException"):
        if attr:
            if len(attr) > max_length:
                raise AppValidateException(
                    field=field,
                    message=f"The provided value exceeds the maximum length of {str(max_length)} characters.",
                    error_info=f"The length of the value '{field}' exceeded the maximum allowed limit of {max_length} characters.",
                    exception_type=exception_type
                )


class AppRepositoryException(ApplicationException, AppExceptionHelper):
    def __init__(self, field, message, child_error=None, error_info=None, exception_type="AppRepositoryException"):
        if child_error:
            try:
                child_error = self.format_exception(child_error, child_error.exception_type)
            except:
                child_error = str(child_error)
        if error_info:
            super().__init__(error_info, field, message, child_error, exception_type)
        else:
            super().__init__("Repository Exception", field, message, child_error, exception_type)


class AppSerializerException(ApplicationException, AppExceptionHelper):
    def __init__(self, field, message, child_error=None, error_info=None, exception_type="AppSerializerException"):
        if child_error:
            try:
                child_error = self.format_exception(child_error, child_error.exception_type)
            except:
                child_error = str(child_error)
        if error_info:
            super().__init__(error_info, field, message, child_error, exception_type)
        else:
            super().__init__("Serializer Exception", field, message, child_error, exception_type)


class AppValidateException(ApplicationException, AppExceptionHelper):
    def __init__(self, field, message, child_error=None, error_info=None, exception_type="AppValidateException"):
        if child_error:
            try:
                child_error = self.format_exception(child_error, child_error.exception_type)
            except:
                child_error = str(child_error)
        if error_info:
            super().__init__(error_info, field, message, child_error, exception_type)
        else:
            super().__init__("Validate Exception", field, message, child_error, exception_type)


class AppRequestException(ApplicationException, AppExceptionHelper):
    def __init__(self, field, message, child_error=None, error_info=None, exception_type="AppRequestException"):
        if child_error:
            try:
                child_error = self.format_exception(child_error, child_error.exception_type)
            except:
                child_error = str(child_error)
        if error_info:
            super().__init__(error_info, field, message, child_error, exception_type)
        else:
            super().__init__("Request Exception", field, message, child_error, exception_type)


class AppAuthenticationException(ApplicationException, AppExceptionHelper):
    def __init__(self, field, message, child_error=None, error_info=None, exception_type="AppAuthenticationException"):
        if child_error:
            try:
                child_error = self.format_exception(child_error, child_error.exception_type)
            except:
                child_error = str(child_error)
        if error_info:
            super().__init__(error_info, field, message, child_error, exception_type)
        else:
            super().__init__("Authentication Exception", field, message, child_error, exception_type)
