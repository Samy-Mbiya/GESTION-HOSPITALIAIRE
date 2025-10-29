from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Sum, F, DecimalField

class Client(models.Model):
    nom = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    log =models.TextField(null=True,blank=True)

    def __str__(self):
        return self.nom


# ===================== BASE CLASS =====================
class BaseTransaction(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    total_payer = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    acompte = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reste = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remise = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def update_totals(self):
        """🧮 Recalcule automatiquement les totaux à partir des descriptions associées"""
        descriptions = self.description_set.all()
        total_calcule = descriptions.aggregate(
            total=Sum(F('qt') * F('prix'), output_field=DecimalField(max_digits=10, decimal_places=2))
        )['total'] or 0

        self.total_payer = total_calcule - self.remise
        self.reste = self.total_payer - self.acompte
        self.save()

    def __str__(self):
        return f"{self.__class__.__name__} - {self.id} - {self.client}"


# ===================== NH =====================
class Nh(BaseTransaction):
    pass


# ===================== FACTURE =====================
class Facture(BaseTransaction):
    pass


# ===================== DESCRIPTION =====================
class Description(models.Model):
    detail = models.TextField()
    qt = models.PositiveIntegerField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, null=True, blank=True)
    nh = models.ForeignKey(Nh, on_delete=models.CASCADE, null=True, blank=True)

    def clean(self):
        """⚖️ Empêche qu’une description soit liée à deux documents à la fois"""
        if not self.facture and not self.nh:
            raise ValidationError("La description doit être liée à une facture ou un NH.")
        if self.facture and self.nh:
            raise ValidationError("Une description ne peut pas être liée à une facture ET un NH.")

    def save(self, *args, **kwargs):
        self.full_clean()
        self.total = self.qt * self.prix

        # ✅ Si aucun document n'est lié, on attache automatiquement le dernier
        if not self.facture and not self.nh:
            last_facture = Facture.objects.last()
            last_nh = Nh.objects.last()
            if last_facture:
                self.facture = last_facture
            elif last_nh:
                self.nh = last_nh

        super().save(*args, **kwargs)

        # 🔄 Met à jour les totaux du document lié
        if self.facture:
            self.facture.update_totals()
        elif self.nh:
            self.nh.update_totals()

    def __str__(self):
        return f"{self.detail} - Total: {self.total}"

