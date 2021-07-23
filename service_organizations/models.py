from django.db import models

from shapely.geometry import Polygon
import geojson

from PIK_test.settings import *


class Organisation(models.Model):
    name = models.CharField(max_length=256)
    email = models.EmailField()
    phone = models.CharField(max_length=11)  # TODO: валидация?
    address = models.CharField(max_length=256)

    class Meta:
        ordering = ['id']


class Service(models.Model):
    name = models.CharField(max_length=256, unique=True)


class Grid(models.Model):
    number = models.IntegerField()
    polygon = models.JSONField()

    # Инициализация сетки.
    @staticmethod
    def init_grid():
        data_exist = Grid.objects.all().exists()

        Grid.objects.all().delete()

        latitude_delta = (GRID_LATITUDE_B - GRID_LATITUDE_A) / GRID_STEP
        longitude_delta = (GRID_LONGITUDE_B - GRID_LONGITUDE_A) / GRID_STEP

        for latitude_step in range(GRID_STEP):
            for longitude_step in range(GRID_STEP):
                number = latitude_step * GRID_STEP + longitude_step
                geojson_polygon = geojson.Polygon([[
                    (GRID_LATITUDE_A + (latitude_step + 0) * latitude_delta, GRID_LONGITUDE_A + (longitude_step + 0) * longitude_delta),
                    (GRID_LATITUDE_A + (latitude_step + 1) * latitude_delta, GRID_LONGITUDE_A + (longitude_step + 0) * longitude_delta),
                    (GRID_LATITUDE_A + (latitude_step + 1) * latitude_delta, GRID_LONGITUDE_A + (longitude_step + 1) * longitude_delta),
                    (GRID_LATITUDE_A + (latitude_step + 0) * latitude_delta, GRID_LONGITUDE_A + (longitude_step + 1) * longitude_delta),
                    (GRID_LATITUDE_A + (latitude_step + 0) * latitude_delta, GRID_LONGITUDE_A + (longitude_step + 0) * longitude_delta),
                ]])

                grid = Grid(number=number, polygon=geojson_polygon)
                grid.save()

        # Если области были индексированы до этого - запуск их переиндексации.
        if data_exist:
            areas = Area.objects.all()
            for area in areas:
                Grid.index_grid(area)

    # Поиск ячеек сетки, пересекающих область.
    @staticmethod
    def get_cross_cells(geojson_area_polygon):
        cross_cells = []

        grid = Grid.objects.all()
        for cell in grid:
            cell_polygon = Polygon(cell.polygon['coordinates'][0])
            area_polygon = Polygon(geojson_area_polygon['coordinates'][0])
            if cell_polygon.intersects(area_polygon):
                cross_cells.append(cell.number)

        return cross_cells

    # Индексация пересечений области с сеткой.
    @staticmethod
    def index_grid(area):
        cross_cells = Grid.get_cross_cells(area.polygon)
        for cross_cell in cross_cells:
            cell = Grid.objects.get(number=cross_cell)
            area.grid.add(cell)

    # Получение номера ячейки сетки для точки.
    @staticmethod
    def get_point_cell(point):
        grid = Grid.objects.all()
        for cell in grid:
            cell_polygon = Polygon(cell.polygon['coordinates'][0])
            if cell_polygon.contains(point):
                return cell.number


class Area(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.PROTECT)
    name = models.CharField(max_length=256)
    polygon = models.JSONField()
    costs = models.ManyToManyField(Service, through='Cost')
    grid = models.ManyToManyField(Grid)


class Cost(models.Model):
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    area = models.ForeignKey(Area, on_delete=models.PROTECT)
    value = models.DecimalField(max_digits=6, decimal_places=2)
