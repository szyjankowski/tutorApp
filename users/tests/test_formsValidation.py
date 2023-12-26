from django.test import TestCase
from users.forms import CustomUserCreationForm


class CustomUserCreationFormTest(TestCase):
    def test_form_has_fields(self):
        form = CustomUserCreationForm()
        expected_fields = {"email", "first_name", "last_name", "password1", "password2"}
        self.assertEqual(set(form.fields), expected_fields)

    def test_form_validation_for_blank_items(self):
        form = CustomUserCreationForm(
            data={"email": "", "first_name": "adam", "last_name": "fagu"}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["email"], ["This field is required."])
