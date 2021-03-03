import responses

from shapely.geometry import Polygon
from datetime import datetime
from rasterio.crs import CRS

from src.sac_stac.domain.operations import obtain_date_from_filename, get_bands_from_product_keys, \
    get_geometry_from_cog, get_projection_from_cog
from src.sac_stac.util import get_files_from_dir


def valid_cog_url():
    url = 'https://s3-uk-1.sa-catapult.co.uk/public-eo-data/common_sensing/fiji/sentinel_2/' \
          'S2A_MSIL2A_20151022T222102_T01KBU/S2A_MSIL2A_20151022T222102_T01KBU_B01_60m.tif'
    with open('tests/data/sentinel_2/S2A_MSIL2A_20151022T222102_T01KBU/'
              'S2A_MSIL2A_20151022T222102_T01KBU_B01_60m.tif', "rb") as cog_file:
        responses.add(
            responses.GET,
            url,
            status=200,
            stream=True,
            body=cog_file.read(),
            headers={
                'Content-Type': 'binary/octet-stream',
                'Accept-Ranges': 'bytes',
                'Server': 'CloudianS3'
            }
        )
    return url


def test_obtain_date_from_filename_sentinel():
    date = obtain_date_from_filename(
        file='tests/data/sentinel_2/S2A_MSIL2A_20151022T222102_T01KBU/S2A_MSIL2A_20151022T222102_T01KBU_B01_60m.tif',
        regex='(\d{8}T\d{6})',
        date_format='%Y%m%dT%H%M%S')
    assert date == datetime(2015, 10, 22, 22, 21, 2)


def test_obtain_date_from_filename_s3_url():
    date = obtain_date_from_filename(
        file='s3://public-eo-data/common_sensing/fiji/sentinel_2/S2A_MSIL2A_20151022T222102_T01KBU/'
             'S2A_MSIL2A_20151022T222102_T01KBU_B01_60m.tif',
        regex='(\d{8}T\d{6})',
        date_format='%Y%m%dT%H%M%S')
    assert date == datetime(2015, 10, 22, 22, 21, 2)


def test_obtain_date_from_filename_http_url():
    date = obtain_date_from_filename(
        file='http://s3-uk-1.sa-catapult.co.uk/public-eo-data/common_sensing/fiji/sentinel_2/'
             'S2A_MSIL2A_20151022T222102_T01KBU/S2A_MSIL2A_20151022T222102_T01KBU_B01_60m.tif',
        regex='(\d{8}T\d{6})',
        date_format='%Y%m%dT%H%M%S')
    assert date == datetime(2015, 10, 22, 22, 21, 2)


def test_obtain_date_from_filename_landsat():
    date = obtain_date_from_filename(
        file='http://s3-uk-1.sa-catapult.co.uk/public-eo-data/common_sensing/fiji/landsat_8/LC08_L1TP_076071_20200622/',
        regex='(\d{8})',
        date_format='%Y%m%d')
    assert date == datetime(2020, 6, 22, 0, 0, 0)


@responses.activate
def test_get_geometry_from_cog():

    url = 'https://s3-uk-1.sa-catapult.co.uk/public-eo-data/common_sensing/fiji/sentinel_2/' \
          'S2A_MSIL2A_20151022T222102_T01KBU/S2A_MSIL2A_20151022T222102_T01KBU_B01_60m.tif'

    geometry, crs = get_geometry_from_cog(valid_cog_url())

    assert geometry == Polygon(
        [(309780, 7790200), (309780, 7900000), (199980, 7900000), (199980, 7790200), (309780, 7790200)])
    assert crs == CRS.from_user_input(32701)


@responses.activate
def test_get_geometry_from_offline():

    url = 'https://s3-uk-1.sa-catapult.co.uk/public-eo-data/nothing/here'

    geometry, crs = get_geometry_from_cog(url)

    assert not geometry
    assert not crs


@responses.activate
def test_get_projection_from_cog():

    url = 'https://s3-uk-1.sa-catapult.co.uk/public-eo-data/common_sensing/fiji/sentinel_2/' \
          'S2A_MSIL2A_20151022T222102_T01KBU/S2A_MSIL2A_20151022T222102_T01KBU_B01_60m.tif'

    proj_shp, proj_tran = get_projection_from_cog(valid_cog_url())

    assert proj_shp == [1830, 1830]
    assert proj_tran == [60.0, 0.0, 199980.0, 0.0, -60.0, 7900000.0, 0.0, 0.0, 1.0]


@responses.activate
def test_get_projection_from_cog_offline():

    url = 'https://s3-uk-1.sa-catapult.co.uk/public-eo-data/nothing/here'

    proj_shp, proj_tran = get_projection_from_cog(url)

    assert not proj_shp
    assert not proj_tran


def test_get_bands_from_product_keys():
    assets = get_files_from_dir('tests/data/sentinel_2/S2A_MSIL2A_20151022T222102_T01KBU', 'tif')
    bands = get_bands_from_product_keys(assets)

    assert bands == ['B01_60m', 'B03_10m', 'SCL_20m', 'B09_60m', 'B02_10m', 'B11_20m', 'B12_20m', 'B08_10m',
                     'B04_10m', 'B07_20m', 'B8A_20m', 'AOT_10m', 'B06_20m', 'WVP_10m', 'B05_20m']
