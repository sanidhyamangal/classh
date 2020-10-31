import random
from datetime import datetime


def generate_token() -> str:
    """
    Function to generate token for the miscellaneous tasks.
    """
    return ''.join(
        str(random.randint(0, 99)).zfill(2) + datetime.now().strftime('%H%S'))
