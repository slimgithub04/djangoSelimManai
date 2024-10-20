from django.db import models
from categories.models import category 
from django.core.validators import MaxValueValidator,FileExtensionValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
# Create your models here.


class conference(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    start_date=models.DateField()
    end_date=models.DateField()
    location=models.CharField(max_length=255)
    price=models.FloatField()
    capacity=models.IntegerField(validators=[MaxValueValidator(limit_value=900,message="capacite under 900 must")])
    program=models.FileField(upload_to='files/',validators=[FileExtensionValidator(allowed_extensions=['PNG','jpg','pdf'],message="invalide extension")])
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    category=models.ForeignKey(category,on_delete=models.CASCADE,related_name="conferences")
    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError('end date must be greater than start')
    class Meta:
        constraints=[
            models.CheckConstraint(
                check=models.Q(
                    start_date__gte=
                    timezone.now().date()),name="the start date must be greater or equal then today"
                    )]
        

        get_latest_by = 'title'
    def __str__(self):
        return f'title conference {self.title}'