from django.db import models
from django.contrib.auth.models import User



# Create your models here.

def upload_pic(instance, filename):
        return 'profile_pics/%s/%s' % (instance.user.username, filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    #user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    #image = models.ImageField(default='default.jpg', upload_to='{user.username}/profile_pics', blank=True, null=True)
    image = models.ImageField(default='default.jpg', upload_to=upload_pic, blank=True, null=True)
    
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
    