# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 22:47:23 2022

@author: 김미송
"""
# =============================================================================
# 
# 여기서 각도로 좌표 계산하고. 그 각도에 주기/n을 더해서 위치 조절해야할 듯
# 매번 그날 
# =============================================================================

import matplotlib.pyplot as plt
import numpy as np

from sunpy.coordinates import get_body_heliographic_stonyhurst
from astropy.time import Time
from datetime import date, timedelta

class SolarSystem:
    def __init__(self):
        
        self.planet_list = ['Sun','Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter','Saturn','Uranus','Neptune']
        self.info_ss = np.loadtxt('SOLARSYSTEM.csv', delimiter=',', usecols=range(13))
        self.planet_info = self.info_ss[1:]

        self.planet_paths = ['image/sun.jpg','image/mercury.jpg', 'image/venus.jpg', 'image/earth.jpg', 'image/mars.jpg',
                 'image/jupiter.jpg', 'image/saturn.jpg', 'image/uranus.jpg', 'image/neptune.jpg']

        self.zoom = 1/10  #image marker 비율
        
        self.theta_earth = 360/365.2 
        self.dtime = date.today()
        
        
        
    def setZoom(self, zoom=1/7):
        self.zoom=zoom
    def getZoom(self):
        return self.zoom
    def getThetaEarth(self):
        return self.theta_earth
    def getPlanetList(self):
        return self.planet_list
    def getPlanetInfo(self):
        return self.planet_info
    def getPaths(self):
        return self.planet_paths
    
    def setTime(self, yyyy=0,mm=0,dd=0,n=0):
        if yyyy==0:
            self.dtime =date.today() + timedelta(days=n)    # dtime = date(2022,2,26)       #date.today() 
        else:
            self.dtime = date(yyyy, mm, dd)
            
        astro_time= Time(self.dtime.isoformat())    #Time.now()  # 날짜        #Time('2022-12-22')
        dt = (self.dtime - date(self.dtime.year,3,22)).days   ##-- n계산 일수 계산
        angle_earth = dt * self.getThetaEarth() #
        
        planet_coord = [get_body_heliographic_stonyhurst(this_planet, time=astro_time) for this_planet in self.getPlanetList()]
        angle = [this_coord.lon for this_coord in planet_coord]  # 오늘, 지구 기준 좌표
        return (angle_earth, angle)
    
    def getTime(self):
        return dtime
    
    def getXnY(self, yyyy=0,mm=0,dd=0,n=0):
        (angle_earth, angle) = self.setTime(yyyy, mm, dd, n)
        Radius = np.arange(2,18,2)
        Xs = [r*cos(np.deg2rad(180+angle_earth),a) for r, a in zip(Radius, angle)]
        Ys = [r*sin(np.deg2rad(180+angle_earth),a) for r, a in zip(Radius, angle)]
        Xs.insert(0, 0)
        Ys.insert(0, 0)
        return (Xs, Ys)

    
def cos(alpha, beta):   # cos(x+y) = cos(x)cos(y)-sin(x)sin(y)
    return (np.cos(alpha)*np.cos(beta)-np.sin(alpha)*np.sin(beta))
def sin(alpha, beta):   # sin(x+y)=sin(x)cos(y)+cos(x)sin(y)
    return (np.sin(alpha)*np.cos(beta)+np.cos(alpha)*np.sin(beta))

if __name__ == '__main__':
    ss = SolarSystem()
    (xs, ys) = ss.getXnY(n=-11)
    
    # CEHCK coordinates
    coord = [[x, y] for x, y in zip(xs,ys)]
    # for n in coord:
    #     print(n)
    
    #CHECK AND DRAW ORBIT AND PLANETS
    plt.figure(figsize=(5,5))
    a = np.linspace(0,2*np.pi, 1000)
    x_c = np.sin(a)
    y_c = np.cos(a)
    for r in np.arange(2,18,2):
        plt.plot(r*x_c, r*y_c, color="gray")    # -- 궤도 그리기
    
    for this_planet, x,y in zip(ss.getPlanetList(), xs, ys):
        #plt.plot(r*cos(np.deg2rad(180+(theta_earth*dt)),a), r*sin(np.deg2rad(180+(theta_earth*dt)),a), 'o', label=this_planet)
        plt.plot(x, y, 'o', label=this_planet) # 180은 춘분점이 180도에 오도록.
    plt.legend()
    plt.show()
    
    # TEST
    # #print(type(getTime()))
    print(ss.dtime)
    
    # for planet, info in zip(ss.getPlanetList(), ss.getPlanetInfo()):
    #     print(f"Name : {planet}\n\
    # Mass : {info[0]} x 10^24 kg\n\
    # Diameter : {info[1]} x 10^6 km\n\
    # Density : {info[2]} kg/m^3\n\
    # Gravity : {info[3]} m/s^2\n\
    # Length of Day : {info[4]} h\n\
    # Distance from Sun : {info[5]} km\n\
    # Orbital Period : {info[6]} days\n\
    # Orbital Eccentricity : {info[7]}°\n\
    # Axial tilt :  {info[8]}°\n\
    # Mean Temperature : {info[9]}°C\n\
    # Number of Moons : {int(info[10])}\n\
    # Ring System : {bool(info[10])}\n\
    # Global Magnetic Field : {bool(info[11])}\n\
    # =========================")

# =============================================================================
# No MORE USE
# =============================================================================

# dt(날짜수)* 지구 이동 각도(춘분점기준) == 지구 위치
#print(f"{dt} * {theta_earth} = {dt*theta_earth}")

# dtime = date(2022,2,26)
# print((date.today() + timedelta(days=0)).isoformat()) 
#date의 type == <datetime.time>
# date.today().isoformat()의 type == <str>


# fig = plt.figure()
# ax = fig.add_subplot(projection='polar')
# for this_planet, this_coord in zip(planet_list, planet_coord):
#     ax.plot(this_coord.lon.to('rad'), r, 'o', label=this_planet)
#     ax.legend()
# #    ax.plot(this_coord.lon.to('rad'), r, 'o', label=this_planet)
# plt.show()


# x = [r*np.sin(this_coord.lon) for this_coord in planet_coord]
# y = [r*np.cos(this_coord.lon) for this_coord in planet_coord]

# x = [r*np.sin(this_coord.lon) for r, this_coord in zip(Radius, planet_coord)]
# y = [r*np.cos(this_coord.lon) for r, this_coord in zip(Radius, planet_coord)]