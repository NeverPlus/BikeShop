import os

from django.test import TestCase
from config.settings import BASE_DIR, URL_PREFIX


# Create your tests here.
def test():
    print(os.path.join(BASE_DIR, 'app\media'))

test()
