from dotenv import load_dotenv
import os
class Email:
    def __init__(self, email):
        if self.isValidEmailAddress(email):
            self.email = email
        else:
            raise ValueError("Invalid email address")


    @staticmethod
    def isValidEmailAddress(email):
        load_dotenv()
        verbose: bool = os.getenv("VERBOSE") == "True"

        if verbose: print(f"Validating Email address: {email}")

        # check if the email is empty
        if email == "":
            if verbose : print("0")
            raise ValueError("Email address is missing.")

        domain: str = ""
        # check if the email contains "@" and "."
        if "@" in email:
            domain = email[email.index("@"):]
        else:
            if verbose : print("1")
            raise ValueError("Invalid e-mail address. no @ sign found")

        # check if the domain contains "."
        if "." not in domain:
            if verbose : print("2")
            raise ValueError("Invalid e-mail address. no DOT sign found in the email domain")

        # check if the email contains only one "@"
        if email.count("@") != 1:
            if verbose : print("3")
            raise ValueError("Invalid e-mail address. More than one @ sign found")

        # check if the domain contains at least one "." after the "@" and there is at least two character between them
        # We already know that domain starts with "@" so index of "@" is 0
        # Therefore . must be at least at index 3 of the domain
        if domain.index(".") < 2:
            if verbose : print("4")
            raise ValueError("Invalid e-mail address. Wrong domain")

        # check if there is at least one character before the "@"
        if email.index("@") == 0:
            if verbose : print("5")
            raise ValueError("Invalid e-mail address. No characters before the @ sign")

        # check if there is at least two character after the last ".", We already know that domain must contain at least one "."
        # First find the index of the last "." by going from the end of the email
        for i in range(len(domain) - 1, 0, -1):
            # check if the character is a "."
            if domain[i] == ".":
                # check if there are at least two characters after the last "."
                if len(domain) - i <= 2:
                    raise ValueError("Invalid e-mail address. Less than two characters after the last . sign")

        # Check that the email does not contain any spaces
        if " " in email:
            if verbose : print("8")
            raise ValueError("Invalid e-mail address. Email contains space(s)")

        # Check that the last character of the email is a letter
        if not email[-1].isalpha():
            if verbose : print("9")
            raise ValueError("Invalid e-mail address. Email does not end with a letter")

        if verbose : print("Email is valid.")
        return True