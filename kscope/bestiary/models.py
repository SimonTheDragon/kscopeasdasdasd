from django.db import models
from django.urls import reverse

# Create your models here.


class Superfamiglia(models.Model):

    nome = models.CharField(max_length=100)

    def __str__(self):

        return self.nome


class Famiglia(models.Model):

    nome = models.CharField(max_length=100)

    def __str__(self):

        return self.nome


class Sottofamiglia(models.Model):

    nome = models.CharField(max_length=100)

    def __str__(self):

        return self.nome


class Tribu(models.Model):

    nome = models.CharField(max_length=100)

    def __str__(self):

        return self.nome


class Genere(models.Model):

    nome = models.CharField(max_length=100)

    def __str__(self):

        return self.nome


class Sottogenere(models.Model):

    nome = models.CharField(max_length=100)

    def __str__(self):

        return self.nome


class Provincia(models.Model):

    nome = models.CharField(max_length=30, null=True)

    sigla = models.CharField(max_length=2, unique=True, primary_key=True)

    regione = models.ForeignKey('Regione', on_delete=models.RESTRICT)

    class Meta:
        ordering = ['sigla']

    def __str__(self):

        return f'{self.nome} ({self.sigla}) -  {self.regione.nome}'


class Regione(models.Model):

    nome = models.CharField(max_length=30)

    def __str__(self):

        return self.nome


def get_latest_superfam():
    latest_record = Farfalla.objects.values_list('Superfamiglia', flat=True)
    latest_record = list(latest_record)
    if len(latest_record) > 0:

        latest_record = latest_record[-1]
        return latest_record
    else:
        return("")


def get_latest_fam():
    if len(list(Farfalla.objects.values_list('Famiglia', flat=True))) > 0:
        return(list(Farfalla.objects.values_list('Famiglia', flat=True))[-1])
    else:
        return("")


def get_latest_sottofam():
    if len(list(Farfalla.objects.values_list('Sottofamiglia', flat=True))) > 0:
        return(list(Farfalla.objects.values_list('Sottofamiglia', flat=True))[-1])
    else:
        return("")


def get_latest_tribu():
    if len(list(Farfalla.objects.values_list('Tribu', flat=True))) > 0:
        return(list(Farfalla.objects.values_list('Tribu', flat=True))[-1])
    else:
        return("")


def find_defaults():
    pass


class Farfalla(models.Model):

    Superfamiglia = models.ForeignKey(
        'Superfamiglia', on_delete=models.RESTRICT, default=get_latest_superfam, null=True, blank=True)
    Famiglia = models.ForeignKey(
        'Famiglia', on_delete=models.RESTRICT, default=get_latest_fam, null=True, blank=True)
    Sottofamiglia = models.ForeignKey(
        'Sottofamiglia', on_delete=models.RESTRICT, default=get_latest_sottofam, null=True, blank=True)
    Tribu = models.ForeignKey(
        'Tribu', on_delete=models.RESTRICT, default=get_latest_tribu, null=True, blank=True)
    Genere = models.ForeignKey(
        'Genere', on_delete=models.RESTRICT, null=True, blank=True)
    Sottogenere = models.ForeignKey(
        'Sottogenere', on_delete=models.RESTRICT, null=True, blank=True)

    nome = models.CharField(max_length=100, null=True, blank=True)

    apertura_alare_m = models.CharField(max_length=200, null=True)

    apertura_alare_f = models.CharField(max_length=200, null=True)

    TEMPI_VOLO = (
        ('1', 'Inizio Gennaio'),
        ('2', 'Metà Gennaio'),
        ('3', 'Fine Gennaio'),
        ('4', 'Inizio Febbraio'),
        ('5', 'Metà Febbraio'),
        ('6', 'Fine Febbraio'),
        ('7', 'Inizio Marzo'),
        ('8', 'Metà Marzo'),
        ('9', 'Fine Marzo'),
        ('10', 'Inizio Aprile'),
        ('11', 'Metà Aprile'),
        ('12', 'Fine Aprile'),
        ('13', 'Inizio Maggio'),
        ('14', 'Metà Maggio'),
        ('15', 'Fine Maggio'),
        ('16', 'Inizio Giugno'),
        ('17', 'Metà Giugno'),
        ('18', 'Fine Giugno'),
        ('19', 'Inizio Luglio'),
        ('20', 'Metà Luglio'),
        ('21', 'Fine Luglio'),
        ('22', 'Inizio Agosto'),
        ('23', 'Metà Agosto'),
        ('24', 'Fine Agosto'),
        ('25', 'Inizio Settembre'),
        ('26', 'Metà Settembre'),
        ('27', 'Fine Settembre'),
        ('28', 'Inizio Ottobre'),
        ('29', 'Metà Ottobre'),
        ('30', 'Fine Ottobre'),
        ('31', 'Inizio Novembre'),
        ('32', 'Metà Novembre'),
        ('33', 'Fine Novembre'),
        ('34', 'Inizio Dicembre'),
        ('35', 'Metà Dicembre'),
        ('36', 'Fine Dicembre'),
    )

    inizio_volo = models.CharField(
        max_length=2,
        choices=TEMPI_VOLO,
        null=True, blank=True,
    )

    fine_volo = models.CharField(
        max_length=2,
        choices=TEMPI_VOLO,
        null=True, blank=True,
    )

    def __str__(self):

        return self.nome

    habitat = models.ManyToManyField(Provincia)

    nomi_comuni = models.CharField(max_length=200, null=True, blank=True)

    foto_1 = models.ImageField(upload_to='photos', null=True, blank=True)

    foto_2 = models.ImageField(upload_to='photos', null=True, blank=True)

    def get_absolute_url(self):

        return reverse('farfalla-detail', args=[str(self.id)])
