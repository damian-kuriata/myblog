from django.utils.text import slugify


def populate_entry_slug_field(sender, instance, **kwargs):
    '''
        Populates Entry.slug with slugified Entry.title.
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    '''

    instance.slug = slugify(instance.title)

def populate_category_slug_field(sender, instance, **kwargs):
    '''
        Populates Category.slug with slugified Slug.title
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    '''

    instance.slug = slugify(instance.title)