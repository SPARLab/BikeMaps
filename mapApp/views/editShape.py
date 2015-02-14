from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.gis.geos import GEOSGeometry

# Decorators
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from mapApp.models import Incident, Hazard, Theft, AlertArea, IncidentNotification, HazardNotification, TheftNotification

from mapApp.forms import EditForm

@require_POST
@login_required
def editShape(request):
	editForm = EditForm(request.POST)
	if editForm.is_valid():

		pks = editForm.cleaned_data['editPk'].split(';')[:-1]
		newGeoms = editForm.cleaned_data['editGeom'].split(';')[:-1]
		editType = editForm.cleaned_data['editType']
		objTypes = editForm.cleaned_data['objType'].split(';')[:-1]

		# Edit/Delete each object
		for pk, newGeom, objType in zip(pks, newGeoms, objTypes):
			# Get the correct model dataset
			if objType == 'mapApp.incident':
				objectSet = Incident.objects.all()
			elif objType == 'mapApp.theft':
				objectSet = Theft.objects.all()
			elif objType == 'mapApp.hazard':
				objectSet = Hazard.objects.all()
			elif objType == 'polygon':
				objectSet = AlertArea.objects.filter(user=request.user)
			else:
				return HttpResponseRedirect(reverse('mapApp:index'))

			# Edit
			if(editType == 'edit'):
				shapeEdited = get_object_or_404(objectSet, pk=pk)
				try:
					shapeEdited.geom = GEOSGeometry(newGeom)	# edit the object geometry
				except(ValueError):
					messages.error(request, '<strong>Error</strong><br>Invalid geometry error.')
					return HttpResponseRedirect(reverse('mapApp:index'))
				shapeEdited.save()

			# Delete
			elif (editType == 'delete'):
				shapeEdited = get_object_or_404(objectSet, pk=pk)

				# Delete associated notifications
				if objType == 'mapApp.incident':
					IncidentNotification.objects.filter(point=shapeEdited).delete()
				elif objType == 'mapApp.theft':
					TheftNotification.objects.filter(point=shapeEdited).delete()
				elif objType == 'mapApp.hazard':
					HazardNotification.objects.filter(point=shapeEdited).delete()


				shapeEdited.delete() 	# delete the object

		message = str(len(pks)) + ' ' + editType + ('s' if len(pks)>1 else '') + ' successful'
		messages.success(request, message)

	return HttpResponseRedirect(reverse('mapApp:index'))
