import pytest

from conftest import DAYCARE_FIXTURE_PROFILE_PICTURE_URL_1
from .models import DayCare, Image, DAYCARE_DEFAULT_PICTURE_URL
from django.core.exceptions import ValidationError


@pytest.mark.django_db()
class TestImageModel:
    def test_get_all_images_by_daycare_id(self, create_image1, create_image2, create_daycare_user):
        images = Image.get_images_by_daycare_id(create_daycare_user.id)
        assert create_image1 in images
        assert create_image2 in images

    def test_image_is_deleted_when_daycare_is_deleted(self, create_image1, create_image2, create_daycare_user):
        DayCare.objects.get(id=create_daycare_user.id).delete()
        assert create_image1 not in Image.objects.all()
        assert create_image2 not in Image.objects.all()

    def test_image_creation_with_invalid_image_url(self, create_daycare_user):
        with pytest.raises(ValidationError,
                           match="Invalid URL image - URL should end with \'.gif\', \'.png\', \'.jpg\' or \'.jpeg\'."):
            Image.create(url="NOT_VALID_URL", daycare_id=DayCare.objects.get(id=create_daycare_user.id))

    def test_daycare_has_customized_profile_image(self, create_image1, create_image2, create_daycare_user: DayCare):
        daycare_profile_image = create_daycare_user.get_daycare_primary_image_url()
        assert daycare_profile_image != DAYCARE_DEFAULT_PICTURE_URL
        assert daycare_profile_image == DAYCARE_FIXTURE_PROFILE_PICTURE_URL_1

    def test_daycare_has_default_profile_image_when_no_customized_picture_was_found(self, create_daycare_user: DayCare):
        daycare_profile_image = create_daycare_user.get_daycare_primary_image_url()
        assert daycare_profile_image == DAYCARE_DEFAULT_PICTURE_URL
