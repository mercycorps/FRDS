from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import Context, loader
import os
from django.http import HttpResponseRedirect
from django.db import models
from silo.models import Silo, DataField, ValueStore, Read
from django.shortcuts import render_to_response
import django_tables2 as tables
from django_tables2   import RequestConfig
from display.tables  import SiloTable
from forms import EditForm

#SILOS
def listSilos(request):
	"""
	Each silo is listed with links to details
	"""
	#get all of the silos
	get_silos = Silo.objects.all()

	return render(request, 'display/silos.html',{'get_silos':get_silos})

#SILO-SOURCES
def listSiloSources(request):
	"""
	List all of the silo sources and provide links to edit
	"""
	#get fields to display back to user for verification
	getSources = Read.objects.filter(silo_id=silo_id)
	
	#send the keys and vars from the json data to the template along with submitted feed info and silos for new form				
	return render_to_response("display/stores.html", {'getSilo':getSilo,'silo_id':silo_id})

#Display Silo
def viewSilo(request,id):
	
	silo_id = id
	#get all of the silos
	get_sources = Read.objects.all().filter(silo__id=silo_id)

	return render(request, 'display/silo-sources.html',{'get_sources':get_sources})

#SILO-DETAIL Show data from source
def siloDetail(request,id):
	"""
	Show silo source details
	"""
	silo_id = id
	getSilo = ValueStore.objects.all().filter(field__silo_id=silo_id)
	
	table = SiloTable(ValueStore.objects.all().filter(field__silo_id=silo_id))
	
	#send the keys and vars from the json data to the template along with submitted feed info and silos for new form				
	return render(request,"display/stored_values.html", {'getSilo':table})
	
#SHOW-MERGE FORM
def mergeForm(request,id):
	"""
	Merge different silos using a multistep column mapping wizard form
	"""
	getSource = Silo.objects.get(id=id)
	getSourceTo = Silo.objects.all()
	return render_to_response("display/merge-form.html", {'getSource':getSource,'getSourceTo':getSourceTo})

#SHOW COLUMNS FOR MERGE FORM
def mergeColumns(request):
	"""
	Step 2 in Merge different silos, map columns
	"""
	from_silo_id = request.POST["from_silo_id"]
	to_silo_id = request.POST["to_silo_id"]
	getSourceFrom = DataField.objects.all().filter(silo__id=from_silo_id).distinct("name")
	getSourceTo = DataField.objects.all().filter(silo__id=to_silo_id).distinct("name")
	
	return render_to_response("display/merge-column-form.html", {'getSourceFrom':getSourceFrom,'getSourceTo':getSourceTo,'from_silo_id':from_silo_id,'to_silo_id':to_silo_id})

#EDIT A SINGLE VALUE STORE
def valueEdit(request,id):
	"""
	Edit a value
	"""
	if request.method == 'POST': # If the form has been submitted...
		form = EditForm(request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			# save data to read
			update = ValueStore.objects.get(pk=id)
			form = EditForm(request.POST, instance=update)
			new = form.save(commit=True)
			return HttpResponseRedirect('/value_edit/' + id)
		else:
			print "not valid"
	else:
		value= get_object_or_404(ValueStore, pk=id)
		form = EditForm(instance=value) # An unbound form
	
	return render(request, 'read/edit_value.html', {'form': form,'value':value})
	
#DELETE-FEED 
def valueDelete(request,id):
	"""
	Delete a value
	"""
	deleteStore = ValueStore.objects.get(pk=id).delete()
	
	return render(request, 'read/delete_value.html')	

	
	