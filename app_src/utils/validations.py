# Password and e-mail with at least 6 characters
MINIMUM_CREDENTIAL_SIZE = 6

def is_invalid_credential(received_credential: str) -> bool:
    """
        Given a credential, checks for characters thant can't be entered through the designed template, detecting possible threats

        If credential is invalid, returns True, otherwise it returns False
    """
    INVALID_CHARS = [' ', '\n', '\r']
    has_invalid_chars = any([char in INVALID_CHARS for char in received_credential])
    has_invalid_size = len(received_credential) < MINIMUM_CREDENTIAL_SIZE

    return has_invalid_chars or has_invalid_size