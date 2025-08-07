# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Consultation(models.Model):
    id_consultation = models.AutoField(db_column='Id_consultation', primary_key=True)  # Field name made lowercase.
    id_pr = models.ForeignKey('Personnel', models.DO_NOTHING, db_column='Id_pr')  # Field name made lowercase.
    id_pa = models.ForeignKey('Patient', models.DO_NOTHING, db_column='Id_pa')  # Field name made lowercase.
    s = models.TextField(blank=True, null=True)
    atcd = models.TextField(db_column='ATCD', blank=True, null=True)  # Field name made lowercase.
    hma = models.TextField(db_column='HMA', blank=True, null=True)  # Field name made lowercase.
    ca = models.TextField(db_column='CA', blank=True, null=True)  # Field name made lowercase.
    ep = models.TextField(db_column='EP', blank=True, null=True)  # Field name made lowercase.
    a = models.TextField(db_column='A', blank=True, null=True)  # Field name made lowercase.
    cat = models.TextField(db_column='CAT', blank=True, null=True)  # Field name made lowercase.
    date = models.TextField(db_column='Date')  # Field name made lowercase.
    heure = models.CharField(db_column='Heure', max_length=10)  # Field name made lowercase.
    fac = models.CharField(db_column='Fac', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'consultation'


class Covid(models.Model):
    id_covid = models.AutoField(db_column='Id_covid', primary_key=True)  # Field name made lowercase.
    date = models.DateField()
    id_pa = models.IntegerField(db_column='Id_pa')  # Field name made lowercase.
    id_user_labo = models.CharField(max_length=50, blank=True, null=True)
    id_user_rec = models.CharField(max_length=50)
    description = models.CharField(db_column='Description', max_length=50, blank=True, null=True)  # Field name made lowercase.
    resultat = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'covid'


class Evolution(models.Model):
    id_ev = models.AutoField(db_column='Id_ev', primary_key=True)  # Field name made lowercase.
    s = models.TextField(db_column='S', blank=True, null=True)  # Field name made lowercase.
    hma = models.TextField(db_column='HMA', blank=True, null=True)  # Field name made lowercase.
    ca = models.TextField(db_column='CA', blank=True, null=True)  # Field name made lowercase.
    ep = models.TextField(db_column='EP', blank=True, null=True)  # Field name made lowercase.
    a = models.TextField(db_column='A', blank=True, null=True)  # Field name made lowercase.
    date = models.TextField(db_column='Date')  # Field name made lowercase.
    id_pr = models.IntegerField(db_column='Id_pr')  # Field name made lowercase.
    id_pa = models.IntegerField(db_column='Id_pa')  # Field name made lowercase.
    id_con = models.IntegerField(db_column='Id_con')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'evolution'


class Imagerie(models.Model):
    id_im = models.AutoField(db_column='Id_im', primary_key=True)  # Field name made lowercase.
    exs = models.TextField(db_column='Exs', blank=True, null=True)  # Field name made lowercase.
    exd = models.TextField(db_column='Exd')  # Field name made lowercase.
    rec = models.TextField(db_column='Rec', blank=True, null=True)  # Field name made lowercase.
    but = models.TextField(db_column='But', blank=True, null=True)  # Field name made lowercase.
    date = models.CharField(db_column='Date', max_length=20, blank=True, null=True)  # Field name made lowercase.
    dr_in = models.CharField(db_column='Dr_in', max_length=20, blank=True, null=True)  # Field name made lowercase.
    interpretation = models.TextField(db_column='Interpretation', blank=True, null=True)  # Field name made lowercase.
    id_cons = models.IntegerField(db_column='Id_cons')  # Field name made lowercase.
    id_ev = models.IntegerField(db_column='Id_ev', blank=True, null=True)  # Field name made lowercase.
    sorte = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'imagerie'


class Labo(models.Model):
    id_la = models.AutoField(db_column='Id_la', primary_key=True)  # Field name made lowercase.
    id_pa = models.ForeignKey('Patient', models.DO_NOTHING, db_column='Id_pa')  # Field name made lowercase.
    id_cons = models.ForeignKey(Consultation, models.DO_NOTHING, db_column='Id_cons')  # Field name made lowercase.
    id_ev = models.IntegerField(db_column='Id_ev', blank=True, null=True)  # Field name made lowercase.
    id_per = models.IntegerField(db_column='Id_per', blank=True, null=True)  # Field name made lowercase.
    nom_ex = models.CharField(db_column='Nom_ex', max_length=25)  # Field name made lowercase.
    type_ex = models.CharField(db_column='Type_ex', max_length=25)  # Field name made lowercase.
    valeur = models.CharField(db_column='Valeur', max_length=80, blank=True, null=True)  # Field name made lowercase.
    sorte = models.CharField(max_length=50, blank=True, null=True)
    val_normal = models.CharField(db_column='Val_normal', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'labo'


class Patient(models.Model):
    id_pa = models.AutoField(primary_key=True)
    nom = models.CharField(db_column='Nom', max_length=80)  # Field name made lowercase.
    post_nom = models.CharField(db_column='Post_nom', max_length=80)  # Field name made lowercase.
    prenom = models.CharField(db_column='Prenom', max_length=80)  # Field name made lowercase.
    sexe = models.CharField(db_column='Sexe', max_length=80)  # Field name made lowercase.
    dn = models.CharField(db_column='DN', max_length=80)  # Field name made lowercase.
    ec = models.CharField(db_column='EC', max_length=80)  # Field name made lowercase.
    adresse = models.CharField(db_column='Adresse', max_length=80)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=80, blank=True, null=True)  # Field name made lowercase.
    profession = models.CharField(db_column='Profession', max_length=80, blank=True, null=True)  # Field name made lowercase.
    employeur = models.CharField(db_column='Employeur', max_length=80, blank=True, null=True)  # Field name made lowercase.
    atcd = models.TextField(db_column='ATCD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'patient'


class Personnel(models.Model):
    id_pr = models.AutoField(db_column='Id_pr', primary_key=True)  # Field name made lowercase.
    nom = models.CharField(db_column='Nom', max_length=80)  # Field name made lowercase.
    post_nom = models.CharField(db_column='Post_nom', max_length=80)  # Field name made lowercase.
    prenom = models.CharField(db_column='Prenom', max_length=80)  # Field name made lowercase.
    sexe = models.CharField(db_column='Sexe', max_length=80)  # Field name made lowercase.
    adresse = models.CharField(db_column='Adresse', max_length=80)  # Field name made lowercase.
    fonction = models.CharField(db_column='Fonction', max_length=80)  # Field name made lowercase.
    mot_de_passe = models.CharField(db_column='Mot_de_passe', max_length=25)  # Field name made lowercase.
    cnom = models.CharField(db_column='CNOM', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'personnel'


class Sv(models.Model):
    id_sv = models.AutoField(db_column='Id_sv', primary_key=True)  # Field name made lowercase.
    id_pa = models.IntegerField(db_column='Id_pa')  # Field name made lowercase.
    date = models.CharField(db_column='Date', max_length=25)  # Field name made lowercase.
    heure = models.CharField(db_column='Heure', max_length=25)  # Field name made lowercase.
    tc = models.CharField(db_column='TC', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tas = models.CharField(db_column='TAS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tad = models.CharField(db_column='TAD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fc = models.CharField(db_column='FC', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fr = models.CharField(db_column='FR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    o = models.CharField(db_column='O', max_length=80, blank=True, null=True)  # Field name made lowercase.
    poid = models.IntegerField(db_column='Poid')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sv'


class TarifImagerie(models.Model):
    id_imagerie = models.AutoField(db_column='Id_imagerie', primary_key=True)  # Field name made lowercase.
    exploration = models.CharField(db_column='Exploration', max_length=100)  # Field name made lowercase.
    prix = models.IntegerField(db_column='Prix')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tarif_imagerie'


class Traitement(models.Model):
    id_tr = models.AutoField(db_column='Id_tr', primary_key=True)  # Field name made lowercase.
    medicament = models.CharField(db_column='Medicament', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    qt_prise = models.CharField(db_column='Qt_prise', max_length=25, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=25, blank=True, null=True)  # Field name made lowercase.
    mode_emploi = models.CharField(max_length=100, blank=True, null=True)
    prix = models.FloatField(db_column='Prix', blank=True, null=True)  # Field name made lowercase.
    source = models.CharField(db_column='Source', max_length=10, blank=True, null=True)  # Field name made lowercase.
    id_ev = models.IntegerField(db_column='Id_ev', blank=True, null=True)  # Field name made lowercase.
    id_pa = models.IntegerField(db_column='Id_pa', blank=True, null=True)  # Field name made lowercase.
    id_cons = models.IntegerField(db_column='Id_cons', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'traitement'
