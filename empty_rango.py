"""
Run this script to clear your database
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page


def empty_rango():
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("Deleting page: '{0}'".format(p))
            p.delete()
        print("Deleting category: '{0}'".format(c))
        c.delete()

if __name__ == '__main__':
    print("Starting Rango empty script...")
    empty_rango()
    print("Rango empty script is finished.")