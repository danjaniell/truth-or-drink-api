import random
import string


def generate_id(size=5, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for x in range(size))
