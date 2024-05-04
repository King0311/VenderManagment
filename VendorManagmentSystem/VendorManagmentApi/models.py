from django.db import models

# Create your models here.
class Vendor(models.Model):
    vendor_code = models.IntegerField(primary_key=True,unique=True)
    name = models.CharField(max_length=50)
    contact_detail = models.TextField()
    address = models.TextField()
    on_time_del_rate = models.FloatField(null=True,blank=True)
    avg_quality_rating = models.FloatField(null=True,blank=True)
    avg_response_time = models.FloatField(null=True,blank=True)
    fulfillment_rate = models.FloatField(null=True,blank=True)

    def __str__(self):
        return self.name

class Purchase_Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )
    RATING = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    po_number = models.IntegerField(primary_key=True,unique=True)
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    del_date = models.DateField(auto_now_add=False)
    items = models.JSONField(blank=True,null=True)
    quantity = models.IntegerField()
    status = models.CharField(choices=STATUS, max_length=50)
    rating = models.CharField(choices=RATING, max_length=50,blank=True,null=True)
    issue_date = models.DateField(auto_now_add=False)
    ack_date = models.DateField(auto_now_add=False,blank=True,null=True)

    def __str__(self):
        return str(self.po_number) + " " + str(self.vendor)


class Vendor_Performance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    on_time_del_rate = models.FloatField(null=True,blank=True)
    avg_quality_rating = models.FloatField(null=True,blank=True)
    avg_response_time = models.FloatField(null=True,blank=True)
    fulfillment_rate = models.FloatField(null=True,blank=True)

    def __str__(self):
        return str(self.vendor)
   

 







