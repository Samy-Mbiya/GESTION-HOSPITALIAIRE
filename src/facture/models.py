from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    nom = models.CharField(max_length=300)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nom


class Nh(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    total_payer = models.DecimalField(max_digits=10, decimal_places=2)
    acompte = models.DecimalField(max_digits=10, decimal_places=2)
    reste = models.DecimalField(max_digits=10, decimal_places=2)
    remise = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"NH - {self.id} - {self.client}"


class Facture(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    total_payer = models.DecimalField(max_digits=10, decimal_places=2)
    acompte = models.DecimalField(max_digits=10, decimal_places=2)
    reste = models.DecimalField(max_digits=10, decimal_places=2)
    remise = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f"Facture - {self.id} - {self.client}"


class Description(models.Model):
    detail = models.TextField()
    qt = models.IntegerField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, null=True, blank=True)
    nh = models.ForeignKey(Nh, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.total = self.qt * self.prix
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.detail} - Total: {self.total}"