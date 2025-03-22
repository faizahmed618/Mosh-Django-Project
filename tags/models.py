from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# from store.models import Product

class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type) # obj_type is class like Product
        return TaggedItem.objects.select_related("tag").filter(content_type = content_type, object_id = obj_id)

# Create your models here.
class Tag(models.Model):
    label = models.CharField(max_length=255)
    
    def __str__(self):
        return self.label
    
class TaggedItem(models.Model):
    objects = TaggedItemManager()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # Basically we want to do above but it depend on class so we making a generic
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    contnet_object = GenericForeignKey()
    
    