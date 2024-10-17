Feature: User Class

  Scenario Outline: Making a valid user
    When Making a valid user with name <name>, lastNAme <lastName>, emailAddress <emailAddress> and password <password>"
    Examples:
      | name    | lastName  | emailAddress  | password  |
      | John    | Doe       | john@doe.com  | PASSWORD  |
      | John    | Doe       | john@doe.co.uk| PASSWORD  |
      | John    | Doe       | jo.hn@doe.com | PASSWORD  |

#Scenario: Making a user without email
  Scenario: Failing to make a user without email
    When Failing to make a user without email
    Then return the error message Email address is missing.

#Scenario: Making a new user with invalid email
  Scenario Outline: Failing to make a user with invalid email
    When Failing invalid user with name <name>, lastNAme <lastName>, invalid emailAddress <emailAddress> and password <password>"
    Then return the error message <errorMessage>
    Examples:
      | name    | lastName  | emailAddress    | password  | errorMessage |
      # Missing the domain extension
      | John    | Doe       | john@doe        | PASSWORD  |Invalid e-mail address. no DOT sign found in the email domain |
      # Missing the email id
      | John    | Doe       | @doe.com        | PASSWORD  |Invalid e-mail address. No characters before the @ sign |
      # Missing the "@" symbol
      | John    | Doe       | johndoe.com     | PASSWORD  |Invalid e-mail address. no @ sign found |
      # Missing characters between the "@" symbol and the "." symbol
      | John    | Doe       | john@.doe       | PASSWORD  |Invalid e-mail address. Wrong domain |
      # Missing the "@" symbol
      | John    | Doe       | john%doe.co     | PASSWORD  |Invalid e-mail address. no @ sign found |
      # Ending the email with a "."
      | John    | Doe       | john@doe.co.uk. | PASSWORD  |Invalid e-mail address. Less than two characters after the last . sign |
      # Ending the email with a number
      | John    | Doe       | john@doe.co.u5  | PASSWORD  |Invalid e-mail address. Email does not end with a letter |
      # Ending the email with a special character, not alphabetical
      | John    | Doe       | john@doe.co.u&  | PASSWORD  |Invalid e-mail address. Email does not end with a letter |
      # Having only one character after the last "."
      | John    | Doe       | john@do.co.r    | PASSWORD  |Invalid e-mail address. Less than two characters after the last . sign |
      # Having a space at the end of the email id
      | John    | Doe       | john @doe.co    | PASSWORD  |Invalid e-mail address. Email contains space(s) |
      # Having a space in the middle of the email id
      | John    | Doe       | joh n@doe.co    | PASSWORD  |Invalid e-mail address. Email contains space(s) |
      # Having a space in the beginning of the domain name
      | John    | Doe       | john@ doe.com   | PASSWORD  |Invalid e-mail address. Email contains space(s) |
      # Having a space at the end of the domain name
      | John    | Doe       | john@doe .com   | PASSWORD  |Invalid e-mail address. Email contains space(s) |
      # Having a space in the middle of the domain name
      | John    | Doe       | john@do e.com   | PASSWORD  |Invalid e-mail address. Email contains space(s) |
      # Having a space in the beginning of the domain extension
      | John    | Doe       | john@doe. com   | PASSWORD  |Invalid e-mail address. Email contains space(s) |
      # Having a space in the middle of the domain extension
      | John    | Doe       | john@doe.c om   | PASSWORD  |Invalid e-mail address. Email contains space(s) |



#Scenario: Making a user without first name
  Scenario: Failing to make a user without first
    When Failing to make a user without first name
    Then return the error message Name must contain at least one character


#Scenario: Invalid first name
  Scenario Outline: Failing to make a user with invalid first name
    When Making user with invalid name <name>, lastNAme <lastName>, emailAddress <emailAddress> and password <password> fails"
    Then return the error message <errorMessage>
    Examples:
      | name                  | lastName  | emailAddress        | password  | errorMessage |
      # Missing the domain extension
      |6                      | Doe         | john@doe.com        | PASSWORD  | Name must contain only alphabetic characters|
      |#                      | Doe         | john@doe.com        | PASSWORD  | Name must contain only alphabetic characters|
      |abcdefghijklmnopqrstvv | Doe         | john@doe.com        | PASSWORD  | Name must contain at most 20 characters |


#Scenario: Making a user without last name
  Scenario: Failing to make a user without last name
    When Failing to make a user without last name
    Then return the error message Last name must contain at least one character


#Scenario: Invalid first name
  Scenario Outline: Failing to make a user with invalid last name
    When Failing to make a user with name <name>, invalid lastNAme <lastName>, emailAddress <emailAddress> and password <password> fails"
    Then return the error message <errorMessage>
    Examples:
      | name                  | lastName  | emailAddress        | password  | errorMessage |
      # Missing the domain extension
      |John | 6                     | john@doe.com        | PASSWORD  | Last name must contain only alphabetic characters |
      |John | ¤                     | john@doe.com        | PASSWORD  | Last name must contain only alphabetic characters |
      |Jonn | abcdefghijklmnopqrstvv| john@doe.com        | PASSWORD  | Last name must contain at most 20 characters      |
