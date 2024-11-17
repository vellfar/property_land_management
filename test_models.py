from django.test import TestCase
from django.contrib.auth import get_user_model
from properties.models import LandProperty, Location, Document, OwnershipTransfer
from users.models import User


class UserModelTestCase(TestCase):
    # okay
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password123",
            role=3,
            nin="123456789"
        )

    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.role, 3)
        self.assertEqual(self.user.nin, "123456789")

    def test_user_str(self):
        self.assertEqual(str(self.user), "testuser")

    def test_user_details(self):
        details = self.user.details()
        self.assertEqual(details["username"], "testuser")
        self.assertEqual(details["role"], 3)
        self.assertEqual(details["properties"], [])  # Assuming no properties initially


class LandPropertyModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="owner", password="password")
        self.location = Location.objects.create(
            village="Village A",
            parish="Parish B",
            sub_county="Sub C",
            county="County D",
            district="District E",
            country="Country F",
        )
        self.property = LandProperty.objects.create(
            name="Test Property",
            PID="PID12345",
            owner=self.user,
            location=self.location,
            size=10.5,
            valuation=1000000.00,
            added_by=self.user,
        )

    def test_land_property_creation(self):
        self.assertEqual(LandProperty.objects.count(), 1)
        self.assertEqual(self.property.name, "Test Property")
        self.assertEqual(self.property.owner, self.user)

    def test_land_property_str(self):
        self.assertEqual(str(self.property), f"Test Property - {self.location}")

    def test_land_property_location(self):
        self.assertEqual(self.property.location.village, "Village A")


class DocumentModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="uploader", password="password")
        self.land_property = LandProperty.objects.create(
            name="Test Property",
            owner=self.user,
            added_by=self.user,
            size=5.0,
            valuation=50000.00,
        )
        self.document = Document.objects.create(
            land_property=self.land_property,
            store_name="doc1.pdf",
            original_name="Document 1",
            document_type="pdf",
            purpose="Ownership Document",
            uploaded_by=self.user,
        )

    def test_document_creation(self):
        self.assertEqual(Document.objects.count(), 1)
        self.assertEqual(self.document.store_name, "doc1.pdf")
        self.assertEqual(self.document.uploaded_by, self.user)

    def test_document_land_property_relationship(self):
        self.assertEqual(self.document.land_property, self.land_property)

    def test_document_str(self):
        self.assertEqual(str(self.document), "doc1.pdf")


class OwnershipTransferModelTestCase(TestCase):
    def setUp(self):
        self.current_owner = User.objects.create_user(username="current_owner", password="password")
        self.new_owner = User.objects.create_user(username="new_owner", password="password")
        self.land_property = LandProperty.objects.create(
            name="Transfer Property",
            owner=self.current_owner,
            added_by=self.current_owner,
            size=7.5,
            valuation=75000.00,
        )
        self.transfer = OwnershipTransfer.objects.create(
            land_property=self.land_property,
            current_owner=self.current_owner,
            new_owner=self.new_owner,
            status=1,
            added_by=self.current_owner,
        )

    def test_transfer_creation(self):
        self.assertEqual(OwnershipTransfer.objects.count(), 1)
        self.assertEqual(self.transfer.status, 1)
        self.assertEqual(self.transfer.land_property, self.land_property)
        self.assertEqual(self.transfer.current_owner, self.current_owner)
        self.assertEqual(self.transfer.new_owner, self.new_owner)

    def test_transfer_str(self):
        self.assertEqual(str(self.transfer), f"Transfer {self.land_property} - {self.transfer.status}")
