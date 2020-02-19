from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import get_storage_class


# Create your models here.

def upload_pic(instance, filename):
        return 'yourspace/%s/profile_pics/%s/' % (instance.user.username, filename)



class S3PrivateFileField(models.FileField):
    """
    A FileField that gives the 'private' ACL to the files it uploads to S3, instead of the default ACL.
    """
    def __init__(self, verbose_name=None, name=None, upload_to='', storage=None, **kwargs):
        if storage is None:
            storage = get_storage_class()(acl='private')
        super(S3PrivateFileField, self).__init__(verbose_name=verbose_name,
                name=name, upload_to=upload_pic, storage=storage, **kwargs)



class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    #user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    #image = models.ImageField(default='default.jpg', upload_to='{user.username}/profile_pics', blank=True, null=True)
    
    
    #works - but not private
    image = models.ImageField(default='default.jpg', upload_to=upload_pic, blank=True, null=True)
    
    #make image private on upload
    #image = S3PrivateFileField(default='default.jpg', upload_to=upload_pic, blank=True, null=True)
    
    def __str__(self):
        return f'{self.user.username} UserProfile'

    
#    def save(self):
#        super().save()
#        
#        img = Image.open(self.image.path)
        
#        if img.height > 300 or img.width > 300:
#            output_size = (300,300)
#            img.thumbnail(output_size)
#            img.save(self.image.path)
    