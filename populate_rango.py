"""
Run this script to fill your database with some test data
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')
import random

import django
django.setup()
from rango.models import Category, Page


def populate():

    python_pages = [
        {"title": "Official Python Tutorial",
         "url": "*"},
        {"title": "Official Python Tutorial 2",
         "url": "*"},
        {"title": "Official Python Tutorial 3",
         "url": "*"}
    ]

    django_pages = [
        {"title": "Official Python Tutorial",
         "url": "*"},
        {"title": "Official Python Tutorial 2",
         "url": "*"},
        {"title": "Official Python Tutorial 3",
         "url": "*"}
    ]

    other_pages = [
        {"title": "Official Python Tutorial",
         "url": "*"},
        {"title": "Official Python Tutorial 2",
         "url": "*"},
        {"title": "Official Python Tutorial 3",
         "url": "*"}
    ]

    cats = {  # Category
        "Python": {"pages": python_pages, "views":128, "likes":64},
        "Django": {"pages": django_pages, "views":64, "likes":32},
        "Other": {"pages": other_pages, "views":32, "likes":16}
    }

    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data["views"], cat_data["likes"])
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"], page_views_generator())

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))


def add_page(cat, title, url, views):
    p = Page.objects.get_or_create(category=cat, title=title, views=views)[0]
    p.url = url
    p.views = views
    p.save()
    return p


def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name, views = views, likes = likes)[0]
    c.save()
    return c

def page_views_generator(start = 0, stop = 100):
    return random.randrange(start, stop)


if __name__ == '__main__':
    print("Starting Rango populate script...")
    populate()
