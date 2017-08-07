from datetime import datetime

from push_notifications.models import APNSDevice, GCMDevice
# from push_notifications.gcm import gcm_send_bulk_message

from mapApp.models import Incident, Hazard, Theft, AlertArea

# Google cloud messaging devices/Android devices
def getGCMDevicesToNotify(users):
    devices = GCMDevice.objects.filter(user__in=users)
    return devices

# Apple Push Notification Service devices/iOS devices
def getAPNSDevicesToNotify(users):
    devices = APNSDevice.objects.filter(user__in=users)
    return devices

# Push a notification to all users where the new point falls within their alert areas
def pushNotification(point):
    intersectingPolys = AlertArea.objects.filter(geom__intersects=point.geom) #list of AlertArea objects
    usersToNotify = list(set([poly.user for poly in intersectingPolys])) # get list of distinct users to alert
    GCMDevices = getGCMDevicesToNotify(usersToNotify) # Android devices
    APNSDevices = getAPNSDevicesToNotify(usersToNotify) # iOS devices

    payload = payloadHelper(point)

    if payload:
        if point.p_type == "collision":
            GCMDevices.send_message("Collision reported.", extra=payload)
            APNSDevices.send_message("Collision reported.", extra=payload)
        elif point.p_type == "nearmiss":
            GCMDevices.send_message("Near miss reported.", extra=payload)
            APNSDevices.send_message("Near miss reported.", extra=payload)
        elif point.p_type == "hazard":
            GCMDevices.send_message("Hazard reported.", extra=payload)
            APNSDevices.send_message("Hazard reported.", extra=payload)
        elif point.p_type == "theft":
            GCMDevices.send_message("Theft reported.", extra=payload)
            APNSDevices.send_message("Theft reported.", extra=payload)
        else:
            GCMDevices.send_message("New incident reported.", extra=payload)
            APNSDevices.send_message("New incident reported.", extra=payload)

# Payload includes data for push notifications
def payloadHelper(point):
    if point.p_type == "collision" or point.p_type == "nearmiss":
        if point.date:
            serialdt = dateSerializerHelper(point.date)
            payload = {"pk": point.pk, "type": point.p_type, "i_type": point.i_type, "incident_with": point.incident_with, "date": serialdt, "details": point.details, "lng": point.geom.coords[0], "lat": point.geom.coords[1], "sound":"default"}
        else:
            payload = {"pk": point.pk, "type": point.p_type, "i_type": point.i_type, "incident_with": point.incident_with, "details": point.details, "lng": point.geom.coords[0], "lat": point.geom.coords[1], "sound":"default"}

    elif point.p_type == "hazard" or point.p_type == "theft":
        if point.date:
            serialdt = dateSerializerHelper(point.date)
            payload ={"pk": point.pk, "type": point.p_type, "i_type": point.i_type, "date": serialdt, "details": point.details, "lng": point.geom.coords[0], "lat": point.geom.coords[1], "sound":"default"}
        else:
            payload ={"pk": point.pk, "type": point.p_type, "i_type": point.i_type, "details": point.details, "lng": point.geom.coords[0], "lat": point.geom.coords[1], "sound":"default"}

    else:
        payload = {}

    return payload


def dateSerializerHelper(dt):
    if isinstance(dt, datetime):
        serial = dt.isoformat()
        return serial

    
        
   

    
