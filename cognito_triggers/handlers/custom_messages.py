from core.request import generate_web_url


def handler(event, context):
    email = event['request']['userAttributes']['email']
    trigger_source = event['triggerSource']
    code_parameter = event['request']['codeParameter']

    if trigger_source == 'CustomMessage_ForgotPassword':
        reset_password_url = generate_web_url(f"/reset-password/{email}")
        forgot_password_subject = "Caring Calendar Password Reset Requested"
        forgot_password_message = f"Your verification code is {code_parameter}.<br><br> Please go to " \
                                  f"{reset_password_url} to reset your password."

        event['response']['emailSubject'] = forgot_password_subject
        event['response']['emailMessage'] = forgot_password_message

    return event
