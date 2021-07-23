from django.db.models.deletion import ProtectedError
from django.http import JsonResponse, HttpResponse

from rest_framework.decorators import api_view
from rest_framework import status, generics
from rest_framework.mixins import DestroyModelMixin, ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin

from shapely.geometry import Point, Polygon
import geojson

from .models import Organisation, Service, Area, Cost, Grid
from .serializers import OrganisationSerializer, ServiceSerializer, AreaSerializer, CostSerializer, CoordinateSerializer


@api_view(['GET'])
def init_grid(request):
    Grid.init_grid()

    return HttpResponse('')


@api_view(['GET'])
def coordinate_info(request, latitude, longitude):
    data = {
        'latitude': latitude,
        'longitude': longitude,
    }

    serializer = CoordinateSerializer(data=data)
    serializer.is_valid(raise_exception=True)

    point = Point(float(latitude), float(longitude))
    point_cell = Grid.get_point_cell(point)

    features = []
    areas = Area.objects.filter(grid__number=point_cell)
    for area in areas:
        polygon = Polygon(area.polygon['coordinates'][0])
        if polygon.contains(point):
            geojson_polygon = geojson.Polygon(area.polygon['coordinates'])

            geojson_properties = {
                'organisation_name': area.organisation.name,
                'area_name': area.name,
            }
            costs = Cost.objects.filter(area_id=area.id)
            for cost in costs:
                geojson_properties[cost.service.name] = cost.value

            feature = geojson.Feature(geometry=geojson_polygon, properties=geojson_properties)
            features.append(feature)

    feature_collection = geojson.FeatureCollection([feature for feature in features])

    return JsonResponse(feature_collection)


class ProtectDestroyModelMixin(DestroyModelMixin):
    def destroy(self, request, *args, **kwargs):
        try:
            result = super().destroy(request, *args, **kwargs)
        except ProtectedError as e:
            return JsonResponse({'detail': str(e)}, status=status.HTTP_423_LOCKED)
        return result


class OrganisationList(ListModelMixin,
                       CreateModelMixin,
                       generics.GenericAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OrganisationDetail(RetrieveModelMixin,
                         UpdateModelMixin,
                         ProtectDestroyModelMixin,
                         generics.GenericAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ServiceList(ListModelMixin,
                  CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ServiceDetail(RetrieveModelMixin,
                    UpdateModelMixin,
                    DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class AreaList(ListModelMixin,
               CreateModelMixin,
               generics.GenericAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

    def post(self, request, *args, **kwargs):
        from rest_framework.response import Response

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        area = serializer.save()

        # Индексация пересечений области с сеткой.
        Grid.index_grid(area)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class AreaDetail(RetrieveModelMixin,
                 UpdateModelMixin,
                 DestroyModelMixin,
                 generics.GenericAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CostList(ListModelMixin,
               CreateModelMixin,
               generics.GenericAPIView):
    queryset = Cost.objects.all()
    serializer_class = CostSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CostDetail(RetrieveModelMixin,
                 UpdateModelMixin,
                 DestroyModelMixin,
                 generics.GenericAPIView):
    queryset = Cost.objects.all()
    serializer_class = CostSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
