from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Tag(models.Model):
    tag = models.CharField(max_length=128, primary_key=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.tag)
        super(Tag, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.tag


class Photo(models.Model):
    id = models.IntegerField(primary_key=True)
    approved = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='tree_photo', blank=True)
    comm = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.id)


class Tree(models.Model):

    # Data pulled from data.vancouver.ca/datacatalogue/streetTrees.htm
    treeId = models.IntegerField(primary_key=True)
    neighbourhood = models.CharField(max_length=128, blank=True)
    commonName = models.CharField(max_length=128, blank=True)
    diameter = models.FloatField(null=True, blank=True)
    streetNumber = models.PositiveSmallIntegerField(null=True, blank=True)
    street = models.CharField(max_length=128, blank=True)

    # Populated by sending street address to google and receiving lat lon output
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)

    photo = models.ManyToManyField(Photo, blank=True)

    def save(self, *args, **kwargs):
                super(Tree, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.treeId)


class FoodTree(models.Model):

    name = models.CharField(max_length=128, unique=True)
    address = models.CharField(max_length=1024, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    numOfFT = models.PositiveSmallIntegerField(null=True, blank=True)
    typesOfFT = models.CharField(max_length=1024, blank=True)
    neighbourhood = models.CharField(max_length=128, null=True, blank=True)
    slug = models.SlugField(primary_key=True, unique=True)

    photo = models.ManyToManyField(Photo, blank=True)

    def save(self, *args, **kwargs):
                self.slug = slugify(self.name)
                super(FoodTree, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Park(models.Model):

    parkId = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128, blank=True)
    address = models.CharField(max_length=128, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    neighbourhood = models.CharField(max_length=128, null=True, blank=True)

    photo = models.ManyToManyField(Photo, blank=True)

    def save(self, *args, **kwargs):
                super(Park, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.parkId)


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include for a user.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # fields are used to store user's favourite trees, foodtrees, and parks
    tree = models.ManyToManyField(Tree, blank=True)
    foodtree = models.ManyToManyField(FoodTree, blank=True)
    park = models.ManyToManyField(Park, blank=True)

    def __unicode__(self):
        return self.user.username