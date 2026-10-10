from django.db import models

# Create your models here.
class Register(models.Model):
    name = models.CharField(max_length=25,null=True,blank=True)
    address = models.CharField(max_length=50,null=True,blank=True)
    Gender_choices =[
        ('M','male'),
        ('F','female'),
        ('O','other')
    ]
    gender = models.CharField(max_length=8,choices=Gender_choices,null=True,blank=True)
    phone = models.IntegerField(null=True,blank=True)
    email = models.EmailField(max_length=100,unique=True)
    password = models.CharField(max_length=25,null=True,blank=True)
    image = models.FileField(upload_to='images/',null=True,blank=True)


class dress(models.Model):
    name =  models.CharField(max_length=25,null=True,blank=True)
    user = models.ForeignKey('shopowner_register',on_delete=models.CASCADE,null=True,blank=True)
    price = models.IntegerField(null=True,blank=True)
    brand = models.CharField(max_length=25,null=True,blank=True)
    size = models.CharField(null=True,blank=True)
    material = models.CharField(max_length=25,null=True,blank=True)
    neckline = models.CharField(max_length=25,null=True,blank=True)
    sleeve_length = models.CharField(max_length=25,null=True,blank=True)
    length = models.CharField(null=True,blank=True)
    color = models.CharField(max_length=25,null=True,blank=True)
    pattern = models.CharField(max_length=25,null=True,blank=True)
    image = models.FileField(upload_to='images/',null=True,blank=True)
    discription =  models.CharField(max_length=150,null=True,blank=True)
    quantity = models.IntegerField(default=50)

class shopowner_register(models.Model):
    name = models.CharField(max_length=25,null=True,blank=True)
    shop_name=models.CharField(max_length=25,null=True,blank=True)
    shop_address = models.CharField(max_length=50,null=True,blank=True)
    phone = models.IntegerField(null=True,blank=True)
    place = models.CharField(max_length=25,null=True,blank=True)
    email = models.EmailField(max_length=100,unique=True)
    password = models.CharField(max_length=25,null=True,blank=True)
    image = models.FileField(upload_to='images/',null=True,blank=True)



class cart(models.Model):
    user=models.ForeignKey(Register,on_delete=models.CASCADE)
    products=models.ForeignKey(dress,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    added_at=models.DateTimeField(auto_now_add=True)
    


class order(models.Model):
    user=models.ForeignKey(Register,on_delete=models.CASCADE)
    products=models.ForeignKey(dress,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    total_price=models.IntegerField(null=True,blank=True)
    added_at=models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending',null=True,blank=True)
    ordered_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)


class feedback(models.Model):
    user = models.ForeignKey(Register,on_delete=models.CASCADE)
    product = models.ForeignKey(dress,on_delete=models.CASCADE,null=True,blank=True)
    rating = models.IntegerField(null=True,blank=True)
    feedback = models.CharField(max_length=100,null=True,blank=True)
    added_at = models.DateTimeField(auto_now_add=True)



class wishlist(models.Model):
    user=models.ForeignKey(Register,on_delete=models.CASCADE)
    product=models.ForeignKey(dress,on_delete=models.CASCADE,null=True,blank=True)
    added_at=models.DateTimeField(auto_now_add=True)



class designer(models.Model):
    name = models.CharField(max_length=25,null=True,blank=True)
    age = models.IntegerField(null=True,blank=True)
    qualification = models.CharField(max_length=25,null=True,blank=True)
    Gender_choices =[
        ('M','male'),
        ('F','female'),
        ('O','other')
    ]
    gender = models.CharField(max_length=8,choices=Gender_choices,null=True,blank=True)
    phone = models.IntegerField(null=True,blank=True)
    email = models.EmailField(max_length=100,unique=True,null=True,blank=True)
    password = models.CharField(max_length=25,null=True,blank=True)
    user = models.ForeignKey(shopowner_register,on_delete=models.CASCADE,null=True,blank=True)



class Customization(models.Model):
    user = models.ForeignKey(Register,on_delete=models.CASCADE)
    employee = models.ForeignKey(designer,on_delete=models.CASCADE)
    messege = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.BooleanField(default=False)
    rejected_at = models.BooleanField(default=False)
    