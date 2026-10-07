import re
import logging
from functools import wraps


# ==========================================================
# LOGGING CONFIGURATION
# ==========================================================

logging.basicConfig(
    filename="validation.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ==========================================================
# CUSTOM VALIDATION EXCEPTION
# ==========================================================

class ValidationError(Exception):
    pass


# ==========================================================
# BASE VALIDATOR
# ==========================================================

class Validator:

    def validate(self, value):

        raise NotImplementedError(
            "Child classes must implement validate()."
        )


# ==========================================================
# EMAIL VALIDATOR
# ==========================================================

class EmailValidator(Validator):

    def validate(self, value):

        pattern = (
            r"^[\w\.-]+@[\w\.-]+\.\w+$"
        )

        return bool(
            re.match(pattern, value)
        )


# ==========================================================
# PHONE VALIDATOR
# ==========================================================

class PhoneValidator(Validator):

    def validate(self, value):

        pattern = r"^[6-9]\d{9}$"

        return bool(
            re.match(pattern, value)
        )


# ==========================================================
# URL VALIDATOR
# ==========================================================

class URLValidator(Validator):

    def validate(self, value):

        pattern = (
            r"^(https?://)"
            r"([\w\-]+\.)+[\w\-]+"
            r"(/[^\s]*)?$"
        )

        return bool(
            re.match(pattern, value)
        )


# ==========================================================
# VALIDATION DECORATOR
# ==========================================================

def validate_input(validator):

    def decorator(function):

        @wraps(function)
        def wrapper(value):

            if not validator.validate(value):

                logging.error(
                    f"Validation failed: {value}"
                )

                raise ValidationError(
                    f"Invalid value: {value}"
                )

            logging.info(
                f"Validation successful: {value}"
            )

            return function(value)

        return wrapper

    return decorator


# ==========================================================
# FUNCTIONS USING DECORATORS
# ==========================================================

@validate_input(EmailValidator())
def process_email(email):

    print(
        f"Valid email: {email}"
    )


@validate_input(PhoneValidator())
def process_phone(phone):

    print(
        f"Valid phone number: {phone}"
    )


@validate_input(URLValidator())
def process_url(url):

    print(
        f"Valid URL: {url}"
    )


# ==========================================================
# TEST FUNCTION
# ==========================================================

def main():

    print("==============================")
    print(" DATA VALIDATOR FRAMEWORK")
    print("==============================")

    # ------------------------------
    # Email
    # ------------------------------

    email = input(
        "\nEnter email: "
    ).strip()

    try:

        process_email(email)

    except ValidationError as error:

        print(
            f"Validation Error: {error}"
        )

    # ------------------------------
    # Phone
    # ------------------------------

    phone = input(
        "\nEnter phone number: "
    ).strip()

    try:

        process_phone(phone)

    except ValidationError as error:

        print(
            f"Validation Error: {error}"
        )

    # ------------------------------
    # URL
    # ------------------------------

    url = input(
        "\nEnter URL: "
    ).strip()

    try:

        process_url(url)

    except ValidationError as error:

        print(
            f"Validation Error: {error}"
        )


# ==========================================================
# START PROGRAM
# ==========================================================

if __name__ == "__main__":

    main()