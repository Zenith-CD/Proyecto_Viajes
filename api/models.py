from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


class Persona(models.Model):
    rut = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(
            regex=r'^\d{7,8}-[\dkK]$',
            message='El RUT debe tener el formato 12345678-9 (sin puntos y con guion).'
        )],
    )
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    fecha_nacimiento = models.DateField()
    foto = models.ImageField(upload_to='personas/', blank=True, null=True)

    class Meta:
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f'{self.nombre} {self.apellido} ({self.rut})'


class Lugar(models.Model):
    nombre = models.CharField(max_length=150)
    pais = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    descripcion = models.TextField()
    foto = models.ImageField(upload_to='lugares/', blank=True, null=True)

    class Meta:
        ordering = ['nombre']
        verbose_name_plural = 'Lugares'

    def __str__(self):
        return f'{self.nombre} - {self.ciudad}, {self.pais}'


class Viaje(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='viajes')
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE, related_name='visitas')
    fecha_visita = models.DateField()
    titulo = models.CharField(max_length=200)
    relato = models.TextField()
    foto = models.ImageField(upload_to='viajes/', blank=True, null=True)
    calificacion = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='De 1 a 5 estrellas',
    )
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado']  # del más reciente al más antiguo

    def __str__(self):
        return f'{self.titulo} ({self.persona})'