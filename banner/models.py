from django.db import models


# Create your models here.

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    discription = models.CharField(max_length=1000)
    author_id = models.CharField(max_length=50, blank=True)
    image = models.ImageField(null= True, blank=True,upload_to='images/')


class Banner(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(null= True, blank=True,upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)



# Create your models here.

# this model Stores the data of the Phones Verified
class phoneModel(models.Model):
    Mobile = models.IntegerField(blank=False)
    isVerified = models.BooleanField(blank=False, default=False)
    counter = models.IntegerField(default=0, blank=False)  # For HOTP Verification

    def __str__(self):
        return str(self.Mobile)
