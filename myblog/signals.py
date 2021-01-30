from django.utils.text import slugify

def update_entry_category_visits_count(sender, instance, **kwargs):
    """
    For each category that instance belongs to, updatees its visits count
    """
    for category in instance.category_set.all():
        category.total_visits_count += 1
        category.save()

def populate_entry_slug_field(sender, instance, **kwargs):
    """ Populates instance.slug with slugified instance.title. """

    instance.slug = slugify(instance.title)

def populate_category_slug_field(sender, instance, **kwargs):
    """ Populates instance.slug with slugified instance.name """

    instance.slug = slugify(instance.name)