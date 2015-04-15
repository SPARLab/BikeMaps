from datetime import datetime

from push_notifications.models import APNSDevice, GCMDevice
from push_notifications.gcm import gcm_send_bulk_message

from mapApp.models import Incident, Hazard, Theft, AlertArea


def getGCMDevicesToNotify(users):
    devices = GCMDevice.objects.filter(user__in=users)
    return devices


def getAPNSDevicesToNotify(users):
    devices = APNSDevice.objects.filter(user__in=users)
    return devices


def pushNotification(point):
    intersectingPolys = AlertArea.objects.filter(geom__intersects=point.geom) #list of AlertArea objects
    usersToNotify = list(set([poly.user for poly in intersectingPolys])) # get list of distinct users to alert
    GCMDevices = getGCMDevicesToNotify(usersToNotify)
    # APNSDevices = getAPNSDevicesToNotify(userToNotify) # Disabled for now

    payload = payloadHelper(point)

    if payload:
        GCMDevices.send_message(None, extra=payload)
    

def payloadHelper(point):
    if point.p_type == "collision" or point.p_type == "nearmiss":
        if point.date:
            serialdt = dateSerializerHelper(point.date)
            payload = {"pk": point.pk, "type": point.p_type, "i_type": point.i_type, "incident_with": point.incident_with, "date": serialdt, "details": point.details, "lng": point.geom.coords[0], "lat": point.geom.coords[1]}
        else:
            payload = {"pk": point.pk, "type": point.p_type, "i_type": point.i_type, "incident_with": point.incident_with, "details": point.details, "lng": point.geom.coords[0], "lat": point.geom.coords[1]}

    elif point.p_type == "hazard" or point.p_type == "theft":
        if point.date:
            serialdt = dateSerializerHelper(point.date)
            payload ={"pk": point.pk, "type": point.p_type, "i_type": point.i_type, "date": serialdt, "details": point.details, "lng": point.geom.coords[0], "lat": point.geom.coords[1]}
        else:
            payload ={"pk": point.pk, "type": point.p_type, "i_type": point.i_type, "details": point.details, "lng": point.geom.coords[0], "lat": point.geom.coords[1]}

    else:
        payload = {}

    return payload


def dateSerializerHelper(dt):
    if isinstance(dt, datetime):
        serial = dt.isoformat()
        return serial

    
        
   

    
