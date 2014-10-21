#encoding:utf-8
from django.db import models
from django.db.models import signals
from django.template.defaultfilters import slugify
#from slughifi import slughifi
from smart_selects.db_fields import ChainedForeignKey

class Ciudade(models.Model):
	nombre = models.CharField(max_length=60)
	slug = models.SlugField(max_length=100, blank=True)

	
	
	def __unicode__(self):
		return self.nombre

	def ciudad_pre_save(signal, instance, sender, **kwargs):
		instance.slug = slugify(instance.nombre)
		signals.pre_save.connect(ciudad_pre_save, sender=Ciudade)
	

class Sectore(models.Model):
	nombre = models.CharField(max_length=60)
	

	def __unicode__(self):
		return self.nombre

class Tipo(models.Model):
	nombre = models.CharField(max_length=60)
	

	def __unicode__(self):
		return self.nombre

class Restaurante(models.Model):
	nombre = models.CharField(max_length=60)
	descripcion = models.TextField(blank = True, default="descripcion")
	logo = models.ImageField(upload_to = "logos")
	ciudad = models.ForeignKey(Ciudade)
	sector = models.ManyToManyField(Sectore)
	tipo = models.ManyToManyField(Tipo)
	hora_abrir = models.TimeField()
	hora_cerrar = models.TimeField()
	precio_domicilio = models.IntegerField()

	def __unicode__(self):
		return self.nombre

class Categoria(models.Model):
	titulo = models.CharField(max_length=60)
	imagen_categoria = models.ImageField(upload_to = "categorias")
	restaurant = models.ForeignKey(Restaurante)

	
	def __unicode__(self):
		return self.titulo

class Menuesp(models.Model):
	titulo = models.CharField(max_length=60)
	descripcion = models.TextField(blank = True)
	precio = models.IntegerField()
	restaurant = models.ForeignKey(Restaurante)
	
	categoria = ChainedForeignKey(
		Categoria,
		chained_field="restaurant",
		chained_model_field="restaurant",
		show_all=False,
		auto_choose=True
		)

	
	def __unicode__(self):
		return self.titulo


class TituloAdicionale(models.Model):
	titulo = models.CharField(max_length=60,blank=True)
	restaurant = models.ForeignKey(Restaurante)
	

	menuesp = ChainedForeignKey(
		Menuesp,
		chained_field= "restaurant",
		chained_model_field= "restaurant",
		show_all=False,
		auto_choose=True
		)

	
	def __unicode__(self):
		return self.titulo

class AdiUnico(models.Model):
	nombre = models.CharField(max_length=60,blank=True)
	precio = models.IntegerField()
	restaurant = models.ForeignKey(Restaurante)
	
	menuesp = ChainedForeignKey(
		Menuesp,
		chained_field="restaurant",
		chained_model_field="restaurant",
		show_all=False,
		auto_choose=True
		)
	
	titulo =ChainedForeignKey(
		TituloAdicionale,
		chained_field="menuesp",
		chained_model_field="menuesp",
		show_all=False,
		auto_choose=True
		)
	
	def __unicode__(self):
		return self.nombre

class Adicionale(models.Model):
	nombre = models.CharField(max_length=60,blank=True)
	precio = models.IntegerField()
	restaurant = models.ForeignKey(Restaurante)
	menuesp = ChainedForeignKey(
		Menuesp,
		chained_field="restaurant",
		chained_model_field="restaurant",
		show_all=False,
		auto_choose=True
		)
	titulo =ChainedForeignKey(
		TituloAdicionale,
		chained_field="menuesp",
		chained_model_field="menuesp",
		show_all=False,
		auto_choose=True
		)
	
	def __unicode__(self):
		return self.nombre






