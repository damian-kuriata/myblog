from django.utils.text import slugify

def update_entry_category_visits_count(sender, instance, **kwargs):
    for category in instance.category_set.all():
        category.total_visits_count += 1
        category.save()

def populate_entry_slug_field(sender,
                                                           instance,
                                                           **kwargs):
    '''
        Populates Entry.slug with slugified Entry.title.
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    '''

    instance.slug = slugify(instance.title)

def populate_category_slug_field(sender,
                                instance,
                                **kwargs):
    '''
        Populates Category.slug with slugified Slug.title
        Updates visits count by 1
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    '''

    instance.slug = slugify(instance.name)