from django.http import HttpResponse
from django.shortcuts import render
import ee
ee.Initialize()

import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import date

alert1info = []
alert2info = "No"
alert3info = "No"
# reducer =""

# Create your views here.
def index(request):
    # code for webscraping data from hydology.gov.np 
    # url = 'http://hydrology.gov.np/#/basin/183?_k=ijwf2r'
    # driver = webdriver.Chrome(executable_path='c:/chromedriver.exe')
    # driver.get(url)
    # driver.implicitly_wait(10)
    # soup = BeautifulSoup(driver.page_source, 'lxml')
    # tables = soup.find_all('table')
    # dfs = pd.read_html(str(tables))

    # date1 = dfs[1][1][0]
    # water_level = dfs[1][1][1]
    # trend = dfs[1][1][2]
    # status = dfs[1][1][3]


    
    context = {
        "tile" : get_DEM(1),
        # "tile" : get_DEM(),
        "band_viz" : vis_params(),
        # "form" : form,
        "title" : "RPD Challenge",
        
        # "date1" : date1,
        # "water_level" : water_level,
        # "trend": trend,
        # "status" : status,
        # "alert1info" : get_DEM(1)[1],
        # "alert2info" : alert2info,
        # "alert3info" : alert3info,

        # -- fake --
        "date1" : date.today(),
        "water_level" : "1.43 m",
        "trend": "Steady",
        "status" : "Below Warning Level",
    
    }
    return render(request, 'index.html', {"context": context})
    

def get_DEM(water_level):
    
    geometry = ee.Geometry.Polygon([[[83.94842649653192,28.303914550815765],
        [83.93014455988641,28.304443533880793],
        [83.9294579143786,28.288119416443855],
        [83.94937063410516,28.287968255509785],
        [83.94842649653192,28.303914550815765],
       ]])
    
    #dem
    dem = ee.Image("USGS/SRTMGL1_003")
    elev = dem.clip(geometry).select('elevation')

    elevLt = elev.lt(1040+water_level)

    elevLt.updateMask(elevLt)
    map_id_dict = ee.Image(elevLt).getMapId(vis_params())
    tile = str(map_id_dict['tile_fetcher'].url_format)

    return tile
    

def vis_params():
    band_viz ={
        "bands" : ['elevation'],
        "min" : 0,
        "max" : 1,
        "palette" :['#ffffff00','blue'],
        "opacity":0.5
        # "gamma" :1
    }
    return band_viz