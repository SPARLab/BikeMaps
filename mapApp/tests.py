from django.test import TestCase

from django.contrib.gis.geos import GEOSGeometry
from datetime import datetime, timedelta
import json

from django.contrib.auth import get_user_model
User = get_user_model()
from mapApp.models import *

from mapApp.utils.geofenceHelpers import retrieveFollowUpMsg

#Create your tests here.
class GetURLTests(TestCase):
    """Test getting the urls used in mapApp"""
    def setUp(self):
        self.test_user = create_user()
        self.test_superuser = create_superuser()

    def tearDown(self):
        self.test_user.delete()
        self.test_superuser.delete()

    def test_getting_root(self):
        self.assertEqual(self.client.get('/').status_code, 200)
        self.assertEqual(self.client.get('/@48.4599139,-123.3423413,15z').status_code, 200)

    def test_getting_vis(self):
        self.assertEqual(self.client.get('/vis/').status_code, 200)
        self.assertEqual(self.client.get('/vis/@48.4469666,-123.3577538,12z').status_code, 200)

    def test_getting_blog(self):
        self.assertEqual(self.client.get('/blog/').status_code, 200)
        # Test for redirect for non logged in user
        self.assertEqual(self.client.get('/blog/create/').status_code, 302)
        # Test for logged in user
        self.client.login(username="test_user", password="password")
        self.assertEqual(self.client.get('/blog/create/').status_code, 302)
        # Test for superuser
        self.client.login(username="test_superuser", password="password")
        self.assertEqual(self.client.get('/blog/create/').status_code, 200)
        self.client.logout()

    def test_getting_about(self):
        self.assertEqual(self.client.get('/about/').status_code, 200)

    def test_getting_terms_and_conditions(self):
        self.assertEqual(self.client.get('/terms_and_conditions/').status_code, 200)

    def test_getting_alerts(self):
        # Test for redirect for non logged in user
        self.assertEqual(self.client.get('/alerts/').status_code, 302)
        # Test for logged in User
        self.client.login(username="test_user", password="password")
        self.assertEqual(self.client.get('/alerts/').status_code, 200)
        self.client.logout()

    def test_getting_alerts(self):
        self.client.login(username="test_user", password="wrong_password")
        self.assertEqual(self.client.get('/alerts/').status_code, 302)

        self.client.login(username="nonexistant_user", password="password")
        self.assertEqual(self.client.get('/alerts/').status_code, 302)

        self.client.login(username="test_user", password="password")
        self.assertEqual(self.client.get('/alerts/').status_code, 200)
        self.client.logout()

    def test_getting_api(self):
        self.assertEqual(self.client.get('/collisions/').status_code, 200)
        self.assertEqual(self.client.get('/collisions.json').status_code, 200)
        self.assertEqual(self.client.get('/nearmiss/').status_code, 200)
        self.assertEqual(self.client.get('/nearmiss.json').status_code, 200)
        self.assertEqual(self.client.get('/hazards/').status_code, 200)
        self.assertEqual(self.client.get('/hazards.json').status_code, 200)
        self.assertEqual(self.client.get('/thefts/').status_code, 200)
        self.assertEqual(self.client.get('/thefts.json').status_code, 200)
        self.assertEqual(self.client.get('/official.json').status_code, 200)

        self.assertEqual(self.client.get('/collisions_tiny/').status_code, 200)
        self.assertEqual(self.client.get('/nearmisses_tiny/').status_code, 200)
        self.assertEqual(self.client.get('/hazards_tiny/').status_code, 200)
        self.assertEqual(self.client.get('/thefts_tiny/').status_code, 200)
        self.assertEqual(self.client.get('/newInfrastructures_tiny/').status_code, 200)


        self.assertEqual(self.client.get('/alertareas.json').status_code, 401)
        self.client.login(username="test_user", password="password")
        self.assertEqual(self.client.get('/alertareas.json').status_code, 401)
        # TODO: Who needs to be authenticated to access the alertareas api?
        # self.client.login(username="test_superuser", password="password")
        # self.assertEqual(self.client.get('/alertareas/.json').status_code, 200)
        self.client.logout()
        # self.assertEqual(self.client.get('/alertareas/40/').status_code, 200)

class PointTests(TestCase):
    """Tests of Incident class points instantiation and methods"""
    def setUp(self):
        pnt_geom = GEOSGeometry('POINT(-123 48)')
        now_time = datetime.now()

        self._pnt = Incident.objects.create(geom=pnt_geom, date=now_time,
                                            i_type="Collision with moving object or vehicle",
                                            incident_with="Vehicle, side",
                                            injury="Injury, no treatment")

    def tearDown(self):
        self._pnt.delete()

    def test_latlng_list(self):
        self.assertEqual([48, -123], self._pnt.latlngList())

    def test_published_recent(self):
        self.assertTrue(self._pnt.was_published_recently())

    def test_get_absolute_url(self):
        self.assertEqual(self.client.get(self._pnt.get_absolute_url()).status_code, 200)

class IncidentTests(TestCase):
    """Tests of Incident class points instantiation and methods"""
    def setUp(self):
        pnt_geom = GEOSGeometry('POINT(-123.5 48.5)')
        now_time = datetime.now()

        # Collision
        self._collision = Incident.objects.create(geom=pnt_geom, date=now_time,
                                                  i_type="Collision with moving object or vehicle",
                                                  incident_with="Vehicle, side",
                                                  injury="Injury, no treatment")
        # Nearmiss
        self._nearmiss = Incident.objects.create(geom=pnt_geom, date=now_time,
                                                 i_type="Near collision with stationary object or vehicle",
                                                 incident_with="Vehicle, side",
                                                 injury="Injury, no treatment")
        # Fall
        self._fall = Incident.objects.create(geom=pnt_geom, date=now_time,
                                             i_type="Fall",
                                             incident_with="Vehicle, side",
                                             injury="Injury, no treatment")

    def tearDown(self):
        self._collision.delete()
        self._nearmiss.delete()
        self._fall.delete()

    def test_instances(self):
        self.assertIsInstance(self._collision, Incident)
        self.assertIsInstance(self._collision, Point)
        self.assertIsInstance(self._nearmiss, Incident)
        self.assertIsInstance(self._nearmiss, Point)
        self.assertIsInstance(self._fall, Incident)
        self.assertIsInstance(self._fall, Point)

    def test_p_type(self):
        self.assertEqual("collision", self._collision.p_type)
        self.assertEqual("nearmiss", self._nearmiss.p_type)
        self.assertEqual("collision", self._fall.p_type)

class HazardTests(TestCase):
    """Test Hazard instantiation and methods"""
    def setUp(self):
        pnt_geom = GEOSGeometry('POINT(-123.5 48.5)')
        now_time = datetime.now()

        # Create hazards that fall into different categories
        # TODO: Auto implement hazard_category or make a required field
        self._infrastructure = Hazard.objects.create(geom=pnt_geom, date=now_time,
                                                     i_type="Pothole",
                                                     hazard_category="infrastructure")
        self._environmental = Hazard.objects.create(geom=pnt_geom, date=now_time,
                                                    i_type="Wet leaves",
                                                    hazard_category="environmental")
        self._human_behaviour = Hazard.objects.create(geom=pnt_geom, date=now_time,
                                                      i_type="Driver behaviour",
                                                      hazard_category="human behaviour")

        self._environmental.save()

    def tearDown(self):
        self._environmental.delete()
        self._infrastructure.delete()
        self._human_behaviour.delete()

    def test_instances(self):
        self.assertIsInstance(self._infrastructure, Hazard)
        self.assertIsInstance(self._infrastructure, Point)
        self.assertIsInstance(self._environmental, Hazard)
        self.assertIsInstance(self._environmental, Point)
        self.assertIsInstance(self._human_behaviour, Hazard)
        self.assertIsInstance(self._human_behaviour, Point)

    def test_p_type(self):
        self.assertEqual("hazard", self._environmental.p_type)
        self.assertEqual("hazard", self._infrastructure.p_type)
        self.assertEqual("hazard", self._human_behaviour.p_type)

    def test_hazard_category(self):
        self.assertEqual("infrastructure", self._infrastructure.hazard_category)
        self.assertEqual("environmental", self._environmental.hazard_category)
        self.assertEqual("human behaviour", self._human_behaviour.hazard_category)

    def test_is_editable(self):
        self.assertTrue(self._infrastructure.is_editable())
        self.assertFalse(self._environmental.is_editable())
        self.assertFalse(self._human_behaviour.is_editable())

    def test_is_expired(self):
        # TODO implement this
        pass

class TheftTests(TestCase):
    """Tests of Incident class points instantiation and methods"""
    def setUp(self):
        pnt_geom = GEOSGeometry('POINT(-123.5 48.5)')
        now_time = datetime.now()

        # Theft
        self._theft = Theft.objects.create(geom=pnt_geom, date=now_time,
                                           i_type="Bike (value < $1000)",
                                           how_locked="Frame locked",
                                           lock="U-Lock",
                                           locked_to="Outdoor bike rack",
                                           lighting ="Good",
                                           traffic="Very High")

    def tearDown(self):
        self._theft.delete()

    def test_instances(self):
        self.assertIsInstance(self._theft, Theft)
        self.assertIsInstance(self._theft, Point)

    def test_p_type(self):
        self.assertEqual("theft", self._theft.p_type)

class NewInfrastructureTests(TestCase):
    """Tests of Incident class points instantiation and methods"""
    def setUp(self):
        pnt_geom = GEOSGeometry('POINT(-123.5 48.5)')
        now_time = datetime.now()

        # Collision
        self._newInfrastructure = NewInfrastructure.objects.create(geom = pnt_geom,
                                                                   date = now_time,
                                                                   dateAdded = now_time,
                                                                   infra_type = "Sepperated bike lane",
                                                                   infraDetails = "New bike lane")

    def tearDown(self):
        self._newInfrastructure.delete()

    def test_instances(self):
        self.assertIsInstance(self._newInfrastructure, NewInfrastructure)

    def test_p_type(self):
        self.assertEqual("newInfrastructure", self._newInfrastructure.p_type)

class AlertAreaTests(TestCase):
    """Tests for asserting point intersection works correctly with incident points"""
    def setUp(self):
        test_user = create_user()

        poly_geom = GEOSGeometry('POLYGON((-124 48, -124 49, -123 49, -123 48, -124 48))')
        pnt_in_poly_geom = GEOSGeometry('POINT(-123.5 48.5)')
        pnt_out_poly_geom = GEOSGeometry('POINT(-122 48)')

        now = datetime.now()
        now_time = datetime.strftime(now, "%Y-%m-%d %H:%M")
        week_ago_time = datetime.strftime(now - timedelta(weeks=1), "%Y-%m-%d %H:%M")

        self._poly = AlertArea.objects.create(geom=poly_geom, user=test_user)

        # Create points inside the alert area
        self._pnt_in_poly = Incident.objects.create(geom=pnt_in_poly_geom, date=now_time,
                                                    i_type="Collision with moving object or vehicle",
                                                    incident_with="Vehicle, side",
                                                    injury="Injury, no treatment")
        # Create points outside of alert area
        self._pnt_out_poly = Incident.objects.create(geom=pnt_out_poly_geom, date=week_ago_time,
                                                     i_type="Near collision with stationary object or vehicle",
                                                     incident_with="Vehicle, side",
                                                     injury="Injury, no treatment")

    def test_point_intersection(self):
        poly = AlertArea.objects.filter(user__username="test_user")

        self.assertTrue(poly.filter(geom__intersects=self._pnt_in_poly.geom).exists())
        self.assertFalse(poly.filter(geom__intersects=self._pnt_out_poly.geom).exists())

    def tearDown(self):
        self._poly.delete()
        self._pnt_in_poly.delete()
        self._pnt_out_poly.delete()

class PostDataTests(TestCase):
    def setUp(self):
        self.test_user = create_user()
        self.pnt_geom = '{"type": "Point", "coordinates": [-123, 48]}'
        self.poly_geom = '{"type": "Polygon", "coordinates": [[[-124,48],[-124,49],[-123,49],[-123,48],[-124,48]]]}'
        self.now_time = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M")

    def tearDown(self):
        Incident.objects.all().delete()
        Hazard.objects.all().delete()
        Theft.objects.all().delete()

    def test_incident_post(self):
        response = self.client.post("/incident_submit/", {"geom": self.pnt_geom, "date": self.now_time, "i_type": "Collision with moving object or vehicle", "incident_with": "Vehicle, side", "injury": "Injury, no treatment", "impact": "None", "personal_involvement": "Yes"})
        json_string = response.content
        data = json.loads(json_string)

        self.assertTrue(data['success'])
        self.assertEqual(data['point_type'], "collision")

    def test_hazard_post(self):
        response = self.client.post("/hazard_submit/", {"geom": self.pnt_geom, "date": self.now_time,
                                                        "i_type": "Pothole",
                                                        "hazard_category": "infrastructure"})
        json_string = response.content
        data = json.loads(json_string)

        self.assertTrue(data['success'])
        self.assertEqual(data['point_type'], "hazard")

    def test_theft_post(self):
        response = self.client.post("/theft_submit/", {"geom": self.pnt_geom, "date": self.now_time,
                                                       "i_type": "Bike (value < $1000)",
                                                       "how_locked": "Frame locked",
                                                       "lock": "U-Lock",
                                                       "locked_to": "Outdoor bike rack",
                                                       "lighting ": "Good",
                                                       "traffic": "Very High"})
        json_string = response.content
        data = json.loads(json_string)

        self.assertTrue(data['success'])
        self.assertEqual(data['point_type'], "theft")

    def test_alert_area_post(self):
        self.client.login(username="test_user", password="password")
        response = self.client.post("/poly_submit/", {"geom": self.poly_geom,
                                                      "user": self.test_user.id,
                                                      "email": self.test_user.email})
        json_string = response.content
        data = json.loads(json_string)

        self.assertTrue(data['success'])

def create_user():
    return User.objects.create_user("test_user", email="user@bikemaps.org", password="password")

def create_superuser():
    return User.objects.create_superuser("test_superuser", email="super_user@bikemaps.org", password="password")

class RetrieveMessagesForSpecialAreasTests(TestCase):

    def test_hazard_no_special_area(self):
        """
        retrieveFollowUpMsg() returns message of None for locations not in a special area
        """
        annArbor = {'geom': [-83.743034,42.280827]}
        followUpMsg = retrieveFollowUpMsg("hazard", annArbor);
        self.assertEqual(followUpMsg, None)

    def test_hazard_area_within_greater_van(self):
        """
        retrieveFollowUpMsg() returns the burnaby message for coordinates that are within burnaby
        """
        burnaby = {'geom': [-122.980507,49.248810]}
        followUpMsg = retrieveFollowUpMsg("hazard", burnaby);
        self.assertEqual(followUpMsg, "Report this hazard to Burnaby authorities by calling 1-604-294-7440")

    def test_hazard_area_outside_greater_van(self):
        """
        retrieveFollowUpMsg() returns the kelowna message for coordinates that are within kelowna
        """
        kelowna = {'geom': [-119.493500,49.884491]}
        followUpMsg = retrieveFollowUpMsg("hazard", kelowna);
        self.assertEqual(followUpMsg, "Report this hazard online to Kelowna authorities <a href='https://apps.kelowna.ca/iService_Requests/request.cfm?id=265&sid=97' target='_blank' rel='noopener noreferrer'>here</a>")

    def test_incident_no_special_area(self):
        """
        retrieveFollowUpMsg() returns message of None for locations not in a special area
        """
        annArbor = {'geom': [-83.743034,42.280827]}
        followUpMsg = retrieveFollowUpMsg("incident", annArbor);
        self.assertEqual(followUpMsg, None)

    def test_incident_area_within_ontario(self):
        """
        retrieveFollowUpMsg() returns the ontario message for coordinates that are within ontario
        """
        hamilton = {'geom': [-79.8711,43.2557]}
        followUpMsg = retrieveFollowUpMsg("incident", hamilton);
        self.assertEqual(followUpMsg, "If you have been involved in a collision with a vehicle in Ontario, consider reviewing <a href='https://www.thebikinglawyer.ca/post/the-biking-lawyer-s-crash-guide' target='_blank' rel='noopener noreferrer'>this legal guide</a>")
