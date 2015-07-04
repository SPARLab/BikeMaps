
from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect, JsonResponse
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

		objectSet = AlertArea.objects.filter(user=request.user)
		# Edit/Delete each object
		for pk, newGeom in zip(pks, newGeoms):
			# Edit
			if(editType == 'edit'):
				shapeEdited = get_object_or_404(objectSet, pk=pk)
				try:
					shapeEdited.geom = GEOSGeometry(newGeom)	# edit the object geometry
				except(ValueError):
					return JsonResponse({'success':False})
				shapeEdited.save()

			# Delete
			elif (editType == 'delete'):
				shapeEdited = get_object_or_404(objectSet, pk=pk)
				shapeEdited.delete()

		return JsonResponse({'success':True})
	else:
		return JsonResponse({'success':False})
