from rest_framework.serializers import ModelSerializer
from .models import Company, Establishment
from rest_framework import serializers
from product.serializers import ParcelBasicSerializer
from common.serializers import GallerySerializer
from common.models import Gallery


class EstablishmentSerializer(ModelSerializer):
    parcels = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Establishment
        fields = (
            "id",
            "name",
            "description",
            "address",
            "city",
            "zone",
            "state",
            "image",
            "parcels",
            "image",
            "country",
        )

    def get_parcels(self, establishment):
        return ParcelBasicSerializer(establishment.parcels.all(), many=True).data

    def get_image(self, establishment):
        try:
            return (
                establishment.album.images.first().image.url
                if establishment.album
                and establishment.album.images.exists()
                and establishment.album.images.first().image is not None
                else None
            )
        except:
            return None


class UpdateEstablishmentSerializer(ModelSerializer):
    album = GallerySerializer(required=False)

    class Meta:
        model = Establishment
        fields = (
            "id",
            "name",
            "city",
            "zone",
            "album",
            "state",
            "company",
            "description",
            "country",
        )

    def to_representation(self, instance):
        return EstablishmentSerializer(instance).data

    def update(self, instance, validated_data):
        album_data = self.context.get("request").FILES
        if album_data:
            gallery = instance.album
            if gallery is None:
                gallery = Gallery.objects.create()
            for image_data in album_data.values():
                gallery_image = gallery.images.create(image=image_data)
                gallery_image.save()
            validated_data["album"] = gallery
        return super().update(instance, validated_data)

    def create(self, validated_data):
        album_data = self.context.get("request").FILES
        if album_data:
            gallery = Gallery.objects.create()
            for image_data in album_data.getlist("album[images]"):
                gallery_image = gallery.images.create(image=image_data)
                gallery_image.save()
            validated_data["album"] = gallery
        return super().create(validated_data)


class RetrieveEstablishmentSerializer(ModelSerializer):
    parcels = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Establishment
        fields = "__all__"

    def get_parcels(self, establishment):
        return ParcelBasicSerializer(establishment.parcels.all(), many=True).data

    def get_images(self, establishment):
        try:
            return [
                image.image.url
                for image in establishment.album.images.all()
                if image.image is not None
            ]
        except:
            return []


class EstablishmentSeriesSerializer(serializers.Serializer):
    scans = serializers.ListField()
    sales = serializers.ListField()

    class Meta:
        fields = ["scans", "sales"]


class EstablishmentChartSerializer(serializers.Serializer):
    series = EstablishmentSeriesSerializer()
    options = serializers.SerializerMethodField()

    class Meta:
        model = Establishment
        fields = ["series", "options"]

    def get_options(self, establishment):
        period = self.context["period"]
        if period == "week":
            week_days = [
                "Sun",
                "Mon",
                "Tue",
                "Wed",
                "Thu",
                "Fri",
                "Sat",
            ]
            return [week_days[day - 1] for day in self.context["days"]]
        elif period == "month":
            return self.context["days"]
        elif period == "year":
            return [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December",
            ]
        return []


class EstablishmentProductsReputationSerializer(serializers.Serializer):
    series = serializers.ListField()
    options = serializers.ListField()

    class Meta:
        model = Establishment
        fields = ["series", "options"]


class RetrieveCompanySerializer(ModelSerializer):
    establishments = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = (
            "id",
            "name",
            "tradename",
            "address",
            "image",
            "city",
            "state",
            "country",
            "logo",
            "description",
            "establishments",
        )

    def get_establishments(self, company):
        return EstablishmentSerializer(company.establishment_set.all(), many=True).data

    def get_image(self, company):
        try:
            return (
                company.album.images.first().image.url
                if company.album
                and company.album.images.exists()
                and company.album.images.first().image is not None
                else None
            )
        except:
            return None


class CreateCompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        exclude = (
            "fiscal_id",
            "invitation_code",
        )
