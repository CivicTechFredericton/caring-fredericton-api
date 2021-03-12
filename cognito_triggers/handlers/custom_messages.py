import os


def generate_web_url(path: str) -> str:
    """
    Generates a web url, path must start with / or empty string if you only want the web url
    """
    return f"{os.getenv('UI_DOMAIN_NAME')}{path}"


def handler(event, context):
    email = event['request']['userAttributes']['email']
    trigger_source = event['triggerSource']
    code_parameter = event['request']['codeParameter']

    if trigger_source == 'CustomMessage_ForgotPassword':
        reset_password_url = generate_web_url(f"/reset-password/{email}")
        forgot_password_subject = "Caring Calendar - Password Reset"
        forgot_password_message = f"Your verification code is {code_parameter}.<br><br> Please go to " \
                                  f"{reset_password_url} to reset your password."

        event['response']['emailSubject'] = forgot_password_subject
        event['response']['emailMessage'] = forgot_password_message

    # if trigger_source == 'CustomMessage_AdminCreateUser':
    #     signin_url = generate_web_url("/signin")
    #     create_user_subject = "Caring Calendar - Your Temporary Password"
    #     create_user_message = f"Your username is {email} and temporary password is {code_parameter}.<br><br> " \
    #                           f"Please sign in with your temporary credentials at {signin_url} to change your password."
    #
    #     event['response']['emailSubject'] = create_user_subject
    #     event['response']['emailMessage'] = create_user_message

    return event
