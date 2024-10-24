from behave import *

use_step_matcher("re")

#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
@when(
    'Making a valid user with name (?P<name>.+),'
    ' lastNAme (?P<lastName>.+),'
    ' emailAddress (?P<emailAddress>.+)'
    ' and password (?P<password>.+)"')
def userSuccessful(context, name, lastName, emailAddress, password):
    """
    :type context: behave.runner.Context
    :param context:
    :param name:
    :param lastName:
    :param emailAddress:
    :param password:
    :return:
    """
    from Model.Entity.User import User
    try:
        context.user = User(name=name, lastName=lastName, emailAddress=emailAddress, password=password)
        # if the user can be created, then the user is valid and the test is passed.
        assert context.user is not None
    except ValueError as e:
        # if the user cannot be created, then the user is invalid and the test is failed.
        raise AssertionError(e)

#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
@when(
    'Failing invalid user with name (?P<name>.+),'
    ' lastNAme (?P<lastName>.+),'
    ' invalid emailAddress (?P<emailAddress>.+)'
    ' and password (?P<password>.+)"')
def invalidEmailAddress(context, name, lastName, emailAddress, password):
    """
    :type context: behave.runner.Context
    :type name: str
    :type lastName: str
    :type emailAddress: str
    :type password: str
    """
    try:
        from Model.Entity.User import User
        context.user = User(name=name, lastName=lastName, emailAddress=emailAddress, password=password)
        # if the user can be created, then the user is valid and the test is failed.
        raise AssertionError("Failed to identify that the emailAddress is invalid.")
    except ValueError as e:
        context.error = str(e)
        # if the user cannot be created, then the user is invalid and the test is passed.
        assert "Invalid e-mail address" in str(e)


#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
@then('return the error message (?P<errorMessage>.+)')
def controlErrorMessage(context, errorMessage):
    """
    :type context: behave.runner.Context
    :type errorMessage: str
    """
    print(context.error)
    print(errorMessage)
    assert str(context.error) == errorMessage


#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
@when(
    'Making user with invalid name (?P<name>.+),'
    ' lastNAme (?P<lastName>.+),'
    ' emailAddress (?P<emailAddress>.+)'
    ' and password (?P<password>.+) fails"')
def invalidFirstName(context, name, lastName, emailAddress, password):
        """
        :type context: behave.runner.Context
        :type name: str
        :type lastName: str
        :type emailAddress: str
        :type password: str
        """
        try:
            from Model.Entity.User import User
            context.user = User(name=name, lastName=lastName, emailAddress=emailAddress, password=password)
            # if the user can be created, then the user is valid and the test is failed.
            raise AssertionError("Failed to identify that the name is invalid.")
        except ValueError as e:
            # if the user cannot be created, then the user is invalid and the test is passed.
            context.error = str(e)


#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
@when("Failing to make a user without email")
def userWithoutEmail(context):
    """
    :type context: behave.runner.Context
    """
    from Model.Entity.User import User
    try:
        context.USER = User(name="John", lastName="Doe", emailAddress="", password="password")
        raise AssertionError("Failed to identify that the email is missing.")
    except ValueError as e:
        context.error = str(e)
        assert len(str(e)) > 0



#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
@when("Failing to make a user without first name")
def userWithoutFirsName(context):
    """
    :type context: behave.runner.Context
    """
    from Model.Entity.User import User
    try:
        context.USER = User(name="", lastName="Doe", emailAddress="john@doe.com", password="password")
        raise AssertionError("Failed to identify that the first name is missing.")
    except ValueError as e:
        context.error = str(e)
        assert len(str(e)) > 0

#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
@when("Failing to make a user without last name")
def userWithoutLastName(context):
    """
    :type context: behave.runner.Context
    """
    from Model.Entity.User import User
    try:
        context.USER = User(name="John", lastName="", emailAddress="john@doe.com", password="password")
        raise AssertionError("Failed to identify that the last name is missing.")
    except ValueError as e:
        context.error = str(e)
        assert len(str(e)) > 0


#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
@when(
    'Failing to make a user with name (?P<name>.+),'
    ' invalid lastNAme (?P<lastName>.+),'
    ' emailAddress (?P<emailAddress>.+)'
    ' and password (?P<password>.+) fails"')
def invalidLastName(context, name, lastName, emailAddress, password):
    """
    :type context: behave.runner.Context
    :type name: str
    :type lastName: str
    :type emailAddress: str
    :type password: str
    """
    try:
        from Model.Entity.User import User
        context.user = User(name=name, lastName=lastName, emailAddress=emailAddress, password=password)
        # if the user can be created, then the user is valid and the test is failed.
        raise AssertionError("Failed to identify that the last name is invalid.")
    except ValueError as e:
        # if the user cannot be created, then the user is invalid and the test is passed.
        context.error = str(e)