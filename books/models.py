from django.db import models

# Create your models here.
class Book(models.Model):
    title=models.CharField(max_length=250)
    author=models.CharField(max_length=250)
    price=models.FloatField(default=0)

    def __str__(self) -> str:
        return str(self.title)


class Purchase(models.Model):
    PAYMENT_METHODS=[
    ('Mpesa','Mpesa'),
    ('Card','Card'),
    ('Cash','Cash')
    ]
    customer=models.CharField(max_length=250)
    book=models.ForeignKey('Book',on_delete=models.CASCADE)
    payment_method=models.CharField(max_length=6, choices=PAYMENT_METHODS)
    time_created=models.DateTimeField(auto_now_add=True)
    is_successful=models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.book)
