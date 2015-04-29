import Tkinter as tk
from ScrolledText import ScrolledText as st
import tkFont
from PIL import ImageTk, Image
from urllib2 import urlopen, quote
import io
import json
import math
import networkx
import psycopg2
import psycopg2.extras
import string
from googlemaps import Client
from google import search
import webbrowser

"""
This is not a working version:
    OAuth 2.0 key has been removed
    Database connection strings are empty
"""

class Map(object):
    # OAuth 2.0 key has been replaced with an empty string for security
    gmaps = Client("")
    # Url with the static Google map
    url = "http://maps.googleapis.com/maps/api/staticmap?center="+\
          "39.8282,-95.9755&zoom=4&scale=false&size=640x500&maptype="+\
          "roadmap&format=png&visual_refresh=true"

    def __init__(self):
        # Create a graph and add edges
        self.graph = networkx.Graph()

        # Create the list that will hold the shortest path
        self.d_path = []

        # Connection string information replaced with "" for security
        conn_str = ""

        print "Attempting to connect to db"
        # Connect to db
        conn = psycopg2.connect(conn_str)

               
        # Alabama
        mobile_list = [("Mobile, AL", "New Orleans, LA",
                        self.distance(self.get_coords(conn,"Mobile, AL"),
                                 self.get_coords(conn,"New Orleans, LA"))),
                       ("Mobile, AL", "Jacksonville, FL",
                        self.distance(self.get_coords(conn,"Mobile, AL"),
                                      self.get_coords(conn,"Jacksonville, FL")))]
        # Arkansas
        lr_list = [("Little Rock, AR", "Nashville, TN",
                        self.distance(self.get_coords(conn,"Little Rock, AR"),
                                      self.get_coords(conn,"Nashville, TN"))),
                   ("Little Rock, AR", "St. Louis, MO",
                        self.distance(self.get_coords(conn,"Little Rock, AR"),
                                      self.get_coords(conn,"St. Louis, MO")))]
        
        # Arizona
        px_list = [("Phoenix, AZ", "Los Angeles, CA",
                        self.distance(self.get_coords(conn,"Phoenix, AZ"),
                                      self.get_coords(conn,"Los Angeles, CA"))),
                   ("Phoenix, AZ", "Tucson, AZ",
                        self.distance(self.get_coords(conn,"Phoenix, AZ"),
                                      self.get_coords(conn,"Tucson, AZ"))),
                   ("Tucson, AZ", "Yuma, AZ",
                    self.distance(self.get_coords(conn,"Tucson, AZ"),
                                  self.get_coords(conn,"Yuma, AZ"))),
                   ("Yuma, AZ", "San Diego, CA",
                    self.distance(self.get_coords(conn,"Yuma, AZ"),
                                  self.get_coords(conn,"San Diego, CA"))),
                   ("Flagstaff, AZ", "Phoenix, AZ",
                    self.distance(self.get_coords(conn,"Flagstaff, AZ"),
                                  self.get_coords(conn,"Phoenix, AZ")))]
        # California
        sf_list = [("Eugene, OR", "San Francisco, CA",
                        self.distance(self.get_coords(conn,"Eugene, OR"),
                                      self.get_coords(conn,"San Francisco, CA"))),
                   ("Los Angeles, CA", "San Francisco, CA",
                        self.distance(self.get_coords(conn,"Los Angeles, CA"),
                                      self.get_coords(conn,"San Francisco, CA")))]
        # California
        la_list = [("Los Angeles, CA", "Las Vegas, NV",
                        self.distance(self.get_coords(conn,"Los Angeles, CA"),
                                      self.get_coords(conn,"Las Vegas, NV"))),
                   ("San Diego, CA", "Los Angeles, CA",
                        self.distance(self.get_coords(conn,"San Diego, CA"),
                                      self.get_coords(conn,"Los Angeles, CA"))),
                   ("Los Angeles, CA", "Fresno, CA",
                        self.distance(self.get_coords(conn,"Los Angeles, CA"),
                                      self.get_coords(conn,"Fresno, CA"))),
                   ("Fresno, CA", "Sacramento, CA",
                        self.distance(self.get_coords(conn,"Fresno, CA"),
                                      self.get_coords(conn,"Sacramento, CA"))),
                   ("Sacramento, CA", "Reno, NV",
                        self.distance(self.get_coords(conn,"Sacramento, CA"),
                                      self.get_coords(conn,"Reno, NV"))),
                   ("San Francisco, CA", "Sacramento, CA",
                    self.distance(self.get_coords(conn,"San Francisco, CA"),
                                  self.get_coords(conn,"Sacramento, CA")))]
        
        # Colorado
        den_list = [("Pueblo, CO", "Wichita, KS",
                        self.distance(self.get_coords(conn,"Pueblo, CO"),
                                      self.get_coords(conn,"Wichita, KS"))),
                    ("Denver, CO", "Casper, WY",
                        self.distance(self.get_coords(conn,"Denver, CO"),
                                      self.get_coords(conn,"Casper, WY"))),
                    ("Denver, CO", "Pueblo, CO",
                     self.distance(self.get_coords(conn,"Denver, CO"),
                                   self.get_coords(conn,"Pueblo, CO")))]
        # Connecticut
        n_hav_list = [("New Haven, CT", "Providence, RI",
                       self.distance(self.get_coords(conn,"New Haven, CT"),
                                     self.get_coords(conn,"Providence, RI"))),
                      ("New Haven, CT", "New York City, NY",
                       self.distance(self.get_coords(conn,"New Haven, CT"),
                                     self.get_coords(conn,"New York City, NY")))]
        # Delaware
        wilm_list = [("Wilmington, DE", "Baltimore, MD",
                      self.distance(self.get_coords(conn,"Wilmington, DE"),
                                    self.get_coords(conn,"Baltimore, MD"))),
                     ("Wilmington, DE", "Philadelphia, PA",
                      self.distance(self.get_coords(conn,"Wilmington, DE"),
                                    self.get_coords(conn,"Philadelphia, PA")))]
        # Florida
        orl_list = [("Orlando, FL", "Jacksonville, FL",
                     self.distance(self.get_coords(conn,"Orlando, FL"),
                                   self.get_coords(conn,"Jacksonville, FL"))),
                    ("Orlando, FL", "Atlanta, GA",
                     self.distance(self.get_coords(conn,"Orlando, FL"),
                                   self.get_coords(conn,"Atlanta, GA")))]
        # Georgia
        atl_list = [("Atlanta, GA", "Greenville, SC",
                     self.distance(self.get_coords(conn,"Atlanta, GA"),
                                   self.get_coords(conn,"Greenville, SC"))),
                    ("Atlanta, GA", "Nashville, TN",
                     self.distance(self.get_coords(conn,"Atlanta, GA"),
                                   self.get_coords(conn,"Nashville, TN")))]
        # Iowa
        d_moi_list = [("Des Moines, IA", "Minneapolis, MN",
                       self.distance(self.get_coords(conn,"Des Moines, IA"),
                                     self.get_coords(conn,"Minneapolis, MN"))),
                      ("Des Moines, IA", "Omaha, NE",
                       self.distance(self.get_coords(conn,"Des Moines, IA"),
                                     self.get_coords(conn,"Omaha, NE"))),
                      ("Des Moines, IA", "Cedar Rapids, IA",
                       self.distance(self.get_coords(conn,"Des Moines, IA"),
                                     self.get_coords(conn,"Cedar Rapids, IA"))),
                      ("Cedar Rapids, IA", "Chicago, IL",
                       self.distance(self.get_coords(conn,"Cedar Rapids, IA"),
                                     self.get_coords(conn,"Cedar Rapids, IA")))]
        # Idaho
        bois_list = [("Boise, ID", "Portland, OR",
                     self.distance(self.get_coords(conn,"Boise, ID"),
                                   self.get_coords(conn,"Portland, OR"))),
                     ("Pocatello, ID", "Bozeman, MT",
                     self.distance(self.get_coords(conn,"Pocatello, ID"),
                                   self.get_coords(conn,"Bozeman, MT"))),
                     ("Pocatello, ID", "Boise, ID",
                      self.distance(self.get_coords(conn,"Pocatello, ID"),
                                    self.get_coords(conn, "Boise, ID"))),
                     ("Pocatello, ID", "Provo, UT",
                      self.distance(self.get_coords(conn,"Pocatello, ID"),
                                    self.get_coords(conn, "Provo, UT")))]
        # Illinois
        chi_list = [("Chicago, IL", "Grand Rapids, MI",
                     self.distance(self.get_coords(conn,"Chicago, IL"),
                                   self.get_coords(conn,"Grand Rapids, MI"))),
                    ("Chicago, IL", "Milwaukee, WI",
                     self.distance(self.get_coords(conn,"Chicago, IL"),
                                   self.get_coords(conn,"Milwaukee, WI"))),
                    ("Chicago, IL", "Cleveland, OH",
                     self.distance(self.get_coords(conn,"Chicago, IL"),
                                   self.get_coords(conn,"Cleveland, OH"))),
                    ("Chicago, IL", "Lexington, KY",
                     self.distance(self.get_coords(conn,"Chicago, IL"),
                                   self.get_coords(conn,"Lexington, KY"))),
                    ("Chicago, IL", "Indianapolis, IN",
                     self.distance(self.get_coords(conn,"Chicago, IL"),
                                   self.get_coords(conn,"Indianapolis, IN")))]
        # Indiana
        ind_list = [("Indianapolis, IN", "Cleveland, OH",
                     self.distance(self.get_coords(conn,"Indianapolis, IN"),
                                   self.get_coords(conn,"Cleveland, OH"))),
                    ("Indianapolis, IN", "Lexington, KY",
                     self.distance(self.get_coords(conn,"Indianapolis, IN"),
                                   self.get_coords(conn,"Lexington, KY"))),
                    ("Indianapolis, IN", "St. Louis, MO",
                     self.distance(self.get_coords(conn,"Indianapolis, IN"),
                                   self.get_coords(conn,"St. Louis, MO")))]
        # Kansas
        wich_list = [("Wichita, KS", "Oklahoma City, OK",
                      self.distance(self.get_coords(conn,"Wichita, KS"),
                                    self.get_coords(conn,"Oklahoma City, OK")))]
        # Kentucky
        lex_list = [("Lexington, KY", "Columbus, OH",
                     self.distance(self.get_coords(conn,"Lexington, KY"),
                                   self.get_coords(conn,"Columbus, OH"))),
                    ("Lexington, KY", "Charleston, WV",
                     self.distance(self.get_coords(conn,"Lexington, KY"),
                                   self.get_coords(conn,"Charleston, WV")))]
        # Louisiana
        nola_list = [("New Orleans, LA", "Jackson, MS",
                      self.distance(self.get_coords(conn,"New Orleans, LA"),
                                    self.get_coords(conn,"Jackson, MS"))),
                     ("New Orleans, LA", "Houston, TX",
                      self.distance(self.get_coords(conn,"New Orleans, LA"),
                                    self.get_coords(conn,"Houston, TX")))]
        # Massachusetts
        bos_list = [("Boston, MA", "Nashua, NH",
                     self.distance(self.get_coords(conn,"Boston, MA"),
                                   self.get_coords(conn,"Nashua, NH"))),
                    ("Boston, MA", "Portland, ME",
                     self.distance(self.get_coords(conn,"Boston, MA"),
                                   self.get_coords(conn,"Portland, ME"))),
                    ("Boston, MA", "Providence, RI",
                     self.distance(self.get_coords(conn,"Boston, MA"),
                                   self.get_coords(conn,"Providence, RI"))),
                    ("Boston, MA", "New Haven, CT",
                     self.distance(self.get_coords(conn,"Boston, MA"),
                                   self.get_coords(conn,"New Haven, CT")))]
        # Maryland
        balt_list = [("Baltimore, MD", "Philadelphia, PA",
                      self.distance(self.get_coords(conn,"Baltimore, MD"),
                                    self.get_coords(conn,"Philadelphia, PA"))),
                     ("Baltimore, MD", "Richmond, VA",
                      self.distance(self.get_coords(conn,"Baltimore, MD"),
                                    self.get_coords(conn,"Richmond, VA")))]
        # Maine
        port_list = [("Portland, ME", "Nashua, NH",
                      self.distance(self.get_coords(conn,"Portland, ME"),
                                    self.get_coords(conn,"Nashua, NH")))]
        # Michigan
        grap_list = [("Grand Rapids, MI", "Cleveland, OH",
                      self.distance(self.get_coords(conn,"Grand Rapids, MI"),
                                    self.get_coords(conn,"Cleveland, OH"))),
                     ("Grand Rapids, MI", "Indianapolis, IN",
                      self.distance(self.get_coords(conn,"Grand Rapids, MI"),
                                    self.get_coords(conn,"Indianapolis, IN")))]
        # Minnesota
        min_list = [("Minneapolis, MN", "Fargo, ND",
                     self.distance(self.get_coords(conn,"Minneapolis, MN"),
                                   self.get_coords(conn,"Fargo, ND"))),
                    ("Minneapolis, MN", "Eau Claire, WI",
                     self.distance(self.get_coords(conn,"Minneapolis, MN"),
                                   self.get_coords(conn,"Eau Claire, WI"))),
                    ("Minneapolis, MN", "Pierre, SD",
                     self.distance(self.get_coords(conn,"Minneapolis, MN"),
                                   self.get_coords(conn,"Pierre, SD"))),
                    ("Minneapolis, MN", "Rochester, MN",
                     self.distance(self.get_coords(conn,"Minneapolis, MN"),
                                   self.get_coords(conn,"Rochester, MN"))),
                    ("Rochester, MN", "Cedar Rapids, IA",
                     self.distance(self.get_coords(conn,"Rochester, MN"),
                                   self.get_coords(conn,"Cedar Rapids, IA")))]
        # Missouri
        stl_list = [("St. Louis, MO", "Lexington, KY",
                     self.distance(self.get_coords(conn,"St. Louis, MO"),
                                   self.get_coords(conn,"Lexington, KY"))),
                    ("St. Louis, MO", "Oklahoma City, OK",
                     self.distance(self.get_coords(conn,"St. Louis, MO"),
                                   self.get_coords(conn,"Oklahoma City, OK"))),
                    ("St. Louis, MO", "Wichita, KS",
                     self.distance(self.get_coords(conn,"St. Louis, MO"),
                                   self.get_coords(conn,"Wichita, KS")))]
        # Mississippi
        jax_list = [("Jackson, MS", "Mobile, AL",
                     self.distance(self.get_coords(conn,"Jackson, MS"),
                                   self.get_coords(conn,"Mobile, AL"))),
                    ("Jackson, MS", "Nashville, TN",
                     self.distance(self.get_coords(conn,"Jackson, MS"),
                                   self.get_coords(conn,"Nashville, TN"))),
                    ("Jackson, MS", "Little Rock, AR",
                     self.distance(self.get_coords(conn,"Jackson, MS"),
                                   self.get_coords(conn,"Little Rock, AR")))]
        # Montana
        boze_list = [("Bozeman, MT", "Casper, WY",
                      self.distance(self.get_coords(conn,"Bozeman, MT"),
                                    self.get_coords(conn,"Casper, WY"))),
                     ("Bozeman, MT", "Billings, MT",
                      self.distance(self.get_coords(conn,"Bozeman, MT"),
                                    self.get_coords(conn,"Billings, MT"))),
                     ("Kalispell, MT", "Spokane, WA",
                      self.distance(self.get_coords(conn,"Kalispell, MT"),
                                    self.get_coords(conn,"Spokane, WA"))),
                     ("Kalispell, MT", "Bozeman, MT",
                      self.distance(self.get_coords(conn,"Kalispell, MT"),
                                    self.get_coords(conn,"Bozeman, MT")))]
        # North Carolina
        faye_list = [("Fayetteville, NC", "Greenville, SC",
                      self.distance(self.get_coords(conn,"Fayetteville, NC"),
                                    self.get_coords(conn,"Greenville, SC"))),
                     ("Fayetteville, NC", "Nashville, TN",
                      self.distance(self.get_coords(conn,"Fayetteville, NC"),
                                    self.get_coords(conn,"Nashville, TN"))),
                     ("Fayetteville, NC", "Richmond, VA",
                      self.distance(self.get_coords(conn,"Fayetteville, NC"),
                                    self.get_coords(conn,"Richmond, VA")))]
        # North Dakota
        farg_list = [("Fargo, ND", "Pierre, SD",
                      self.distance(self.get_coords(conn,"Fargo, ND"),
                                    self.get_coords(conn,"Pierre, SD"))),
                     ("Fargo, ND", "Bismarck, ND",
                      self.distance(self.get_coords(conn,"Fargo, ND"),
                                    self.get_coords(conn,"Bismarck, ND"))),
                     ("Bismarck, ND", "Dickinson, ND",
                      self.distance(self.get_coords(conn,"Bismarck, ND"),
                                    self.get_coords(conn,"Dickinson, ND"))),
                     ("Dickinson, ND", "Billings, MT",
                      self.distance(self.get_coords(conn,"Dickinson, ND"),
                                    self.get_coords(conn,"Billings, MT")))]
        # Nebraska
        omah_list = [("Omaha, NE", "Pierre, SD",
                      self.distance(self.get_coords(conn,"Omaha, NE"),
                                    self.get_coords(conn,"Pierre, SD"))),
                     ("Omaha, NE", "Wichita, KS",
                      self.distance(self.get_coords(conn,"Omaha, NE"),
                                    self.get_coords(conn,"Wichita, KS"))),
                     ("Omaha, NE", "Denver, CO",
                      self.distance(self.get_coords(conn,"Omaha, NE"),
                                    self.get_coords(conn,"Denver, CO")))]
        # New Hampshire
        shua_list = [("Nashua, NH", "Burlington, VT",
                      self.distance(self.get_coords(conn,"Nashua, NH"),
                                    self.get_coords(conn,"Burlington, VT")))]
        # New Jersey
        atlc_list = [("Atlantic City, NJ", "New York City, NY",
                      self.distance(self.get_coords(conn,"Atlantic City, NJ"),
                                    self.get_coords(conn,"New York City, NY"))),
                     ("Atlantic City, NJ", "Wilmington, DE",
                      self.distance(self.get_coords(conn,"Atlantic City, NJ"),
                                    self.get_coords(conn,"Wilmington, DE")))]
        # New Mexico
        albu_list = [("Albuquerque, NM", "Denver, CO",
                      self.distance(self.get_coords(conn,"Albuquerque, NM"),
                                    self.get_coords(conn,"Denver, CO"))),
                     ("Albuquerque, NM", "Amarillo, TX",
                      self.distance(self.get_coords(conn,"Albuquerque, NM"),
                                    self.get_coords(conn,"Amarillo, TX"))),
                     ("Albuquerque, NM", "Las Cruces, NM",
                      self.distance(self.get_coords(conn,"Albuquerque, NM"),
                                    self.get_coords(conn,"Las Cruces, NM")))]
      
        # Nevada
        lv_list = [("Reno, NV", "Provo, UT",
                    self.distance(self.get_coords(conn,"Reno, NV"),
                                  self.get_coords(conn,"Provo, UT")))]
        # New York
        nyc_list = [("New York City, NY", "Philadelphia, PA",
                      self.distance(self.get_coords(conn,"New York City, NY"),
                                    self.get_coords(conn,"Philadelphia, PA")))]
        # Ohio
        clev_list = [("Cleveland, OH", "Charleston, WV",
                      self.distance(self.get_coords(conn,"Cleveland, OH"),
                                    self.get_coords(conn,"Charleston, WV"))),
                     ("Cleveland, OH", "Columbus, OH",
                      self.distance(self.get_coords(conn,"Cleveland, OH"),
                                    self.get_coords(conn,"Columbus, OH")))]
        # Oklahoma
        okc_list = [("Oklahoma City, OK", "Little Rock, AR",
                      self.distance(self.get_coords(conn,"Oklahoma City, OK"),
                                    self.get_coords(conn,"Little Rock, AR"))),
                    ("Oklahoma City, OK", "Austin, TX",
                      self.distance(self.get_coords(conn,"Oklahoma City, OK"),
                                    self.get_coords(conn,"Austin, TX")))]
        # Oregon
        eug_list = [("Eugene, OR", "Seattle, WA",
                      self.distance(self.get_coords(conn,"Eugene, OR"),
                                    self.get_coords(conn,"Seattle, WA"))),
                    ("Eugene, OR", "Boise, ID",
                      self.distance(self.get_coords(conn,"Eugene, OR"),
                                    self.get_coords(conn,"Boise, ID")))]

        # Pennsylvania
        penn_list = [("Pittsburgh, PA", "Philadelphia, PA",
                      self.distance(self.get_coords(conn,"Pittsburgh, PA"),
                                    self.get_coords(conn,"Philadelphia, PA"))),
                     ("Pittsburgh, PA", "Cleveland, OH",
                      self.distance(self.get_coords(conn,"Pittsburgh, PA"),
                                    self.get_coords(conn,"Cleveland, OH")))]

        # Rhode Island doesn't get a list right now; it has a lot of edges

        # South Carolina
        grvl_list = [("Greenville, SC", "Nashville, TN",
                      self.distance(self.get_coords(conn,"Greenville, SC"),
                                    self.get_coords(conn,"Nashville, TN")))]
        # South Dakota
        pier_list = [("Pierre, SD", "Casper, WY",
                      self.distance(self.get_coords(conn,"Pierre, SD"),
                                    self.get_coords(conn,"Casper, WY")))]
        # Tennessee doesn't get a list right now; it has a lot of edges
        tenn_list = [("Nashville, TN", "Knoxville, TN",
                      self.distance(self.get_coords(conn,"Nashville, TN"),
                                    self.get_coords(conn,"Knoxville, TN"))),
                     ("Knoxville, TN", "Lexington, KY",
                      self.distance(self.get_coords(conn,"Knoxville, TN"),
                                    self.get_coords(conn,"Lexington, KY")))]
        
        # Texas
        tx_list = [("Amarillo, TX", "Oklahoma City, OK",
                    self.distance(self.get_coords(conn,"Amarillo, TX"),
                                  self.get_coords(conn,"Oklahoma City, OK"))),
                   ("Austin, TX", "Houston, TX",
                    self.distance(self.get_coords(conn,"Austin, TX"),
                                  self.get_coords(conn,"Houston, TX"))),
                   ("Austin, TX", "El Paso, TX",
                    self.distance(self.get_coords(conn,"Austin, TX"),
                                  self.get_coords(conn,"El Paso, TX"))),
                   ("El Paso, TX", "Las Cruces, NM",
                    self.distance(self.get_coords(conn,"El Paso, TX"),
                                  self.get_coords(conn,"Las Cruces, NM"))),
                   ("Austin, TX", "Dallas, TX",
                    self.distance(self.get_coords(conn,"Austin, TX"),
                                  self.get_coords(conn,"Dallas, TX"))),
                   ("Houston, TX", "Dallas, TX",
                    self.distance(self.get_coords(conn,"Houston, TX"),
                                  self.get_coords(conn,"Dallas, TX")))]
        # Utah
        """
        prov_list = [("Provo, UT", "Phoenix, AZ",
                      self.distance(self.get_coords(conn,"Provo, UT"),
                                    self.get_coords(conn,"Phoenix, AZ")))]
        """
        # Virginia
        """
        rmnd_list = [("Richmond, VA", "Charleston, WV",
                      self.distance(self.get_coords(conn,"Richmond, VA"),
                                    self.get_coords(conn,"Charleston, WV")))]
        """

        # Washington
        wash_list = [("Seattle, WA", "Spokane, WA",
                      self.distance(self.get_coords(conn,"Seattle, WA"),
                                    self.get_coords(conn,"Spokane, WA")))]
        # Wisconsin
        wisc_list = [("Eau Claire, WI", "Madison, WI",
                      self.distance(self.get_coords(conn,"Eau Claire, WI"),
                                    self.get_coords(conn,"Madison, WI"))),
                     ("Madison, WI", "Milwaukee, WI",
                      self.distance(self.get_coords(conn,"Madison, WI"),
                                    self.get_coords(conn,"Milwaukee, WI")))]

        # Park list
        park_list = [("Saguaro", "Tucson, AZ",
                      self.distance(self.get_coords(conn,"Saguaro"),
                                    self.get_coords(conn,"Tucson, AZ"))),
                     ("Saguaro", "Las Cruces, NM",
                      self.distance(self.get_coords(conn,"Saguaro"),
                                    self.get_coords(conn,"Las Cruces, NM"))),
                     ("Petrified Forest", "Albuquerque, NM",
                      self.distance(self.get_coords(conn,"Petrified Forest"),
                                    self.get_coords(conn,"Albuquerque, NM"))),
                     ("Petrified Forest", "Flagstaff, AZ",
                      self.distance(self.get_coords(conn,"Petrified Forest"),
                                    self.get_coords(conn,"Flagstaff, AZ"))),
                     ("Hot Springs", "Little Rock, AR",
                      self.distance(self.get_coords(conn,"Hot Springs"),
                                    self.get_coords(conn,"Little Rock, AR"))),

                     ("Hot Springs", "Dallas, TX",
                      self.distance(self.get_coords(conn,"Hot Springs"),
                                    self.get_coords(conn,"Dallas, TX"))),
                     ("Mammoth Cave", "Lexington, KY",
                      self.distance(self.get_coords(conn,"Mammoth Cave"),
                                    self.get_coords(conn,"Lexington, KY"))),
                     ("Mammoth Cave", "Nashville, TN",
                      self.distance(self.get_coords(conn,"Mammoth Cave"),
                                    self.get_coords(conn,"Nashville, TN"))),
                     ("Cuyahoga Valley", "Cleveland, OH",
                      self.distance(self.get_coords(conn,"Cuyahoga Valley"),
                                    self.get_coords(conn,"Cleveland, OH"))),
                     ("Cuyahoga Valley", "Pittsburgh, PA",
                      self.distance(self.get_coords(conn,"Cuyahoga Valley"),
                                    self.get_coords(conn,"Pittsburgh, PA"))),
                     ("Cuyahoga Valley", "Columbus, OH",
                      self.distance(self.get_coords(conn,"Cuyahoga Valley"),
                                    self.get_coords(conn,"Columbus, OH"))),
                     ("Shenandoah", "Richmond, VA",
                      self.distance(self.get_coords(conn,"Shenandoah"),
                                    self.get_coords(conn,"Richmond, VA"))),
                     ("Shenandoah", "Charleston, WV",
                      self.distance(self.get_coords(conn,"Shenandoah"),
                                    self.get_coords(conn,"Charleston, WV"))),
                     ("Congaree", "Atlanta, GA",
                      self.distance(self.get_coords(conn,"Congaree"),
                                    self.get_coords(conn,"Atlanta, GA"))),
                     ("Congaree", "Fayetteville, NC",
                      self.distance(self.get_coords(conn,"Congaree"),
                                    self.get_coords(conn,"Fayetteville, NC"))),
                     ("Congaree", "Greenville, SC",
                      self.distance(self.get_coords(conn,"Congaree"),
                                    self.get_coords(conn,"Greenville, SC"))),
                     ("Great Smoky Mountains", "Greenville, SC",
                      self.distance(self.get_coords(conn,"Great Smoky Mountains"),
                                    self.get_coords(conn,"Greenville, SC"))),
                     ("Great Smoky Mountains", "Knoxville, TN",
                      self.distance(self.get_coords(conn,"Great Smoky Mountains"),
                                    self.get_coords(conn,"Knoxville, TN"))),
                     ("Grand Canyon", "Las Vegas, NV",
                      self.distance(self.get_coords(conn,"Grand Canyon"),
                                    self.get_coords(conn,"Las Vegas, NV"))),
                     ("Grand Canyon", "Provo, UT",
                      self.distance(self.get_coords(conn,"Grand Canyon"),
                                    self.get_coords(conn,"Provo, UT"))),
                     ("Grand Canyon", "Flagstaff, AZ",
                      self.distance(self.get_coords(conn,"Grand Canyon"),
                                    self.get_coords(conn,"Flagstaff, AZ"))),
                     ("Arches", "Provo, UT",
                      self.distance(self.get_coords(conn,"Arches"),
                                    self.get_coords(conn,"Provo, UT"))),
                     ("Arches", "Canyonlands",
                      self.distance(self.get_coords(conn,"Arches"),
                                    self.get_coords(conn,"Canyonlands"))),
                     ("Canyonlands", "Capitol Reef",
                      self.distance(self.get_coords(conn,"Canyonlands"),
                                    self.get_coords(conn,"Capitol Reef"))),
                     ("Capitol Reef", "Bryce Canyon",
                      self.distance(self.get_coords(conn,"Capitol Reef"),
                                    self.get_coords(conn,"Bryce Canyon"))),
                     ("Zion", "Bryce Canyon",
                      self.distance(self.get_coords(conn,"Zion"),
                                    self.get_coords(conn,"Bryce Canyon"))),
                     ("Zion", "Grand Canyon",
                      self.distance(self.get_coords(conn,"Zion"),
                                    self.get_coords(conn,"Grand Canyon"))),
                     ("Mesa Verde", "Flagstaff, AZ",
                      self.distance(self.get_coords(conn,"Mesa Verde"),
                                    self.get_coords(conn,"Flagstaff, AZ"))),
                     ("Mesa Verde", "Albuquerque, NM",
                      self.distance(self.get_coords(conn,"Mesa Verde"),
                                    self.get_coords(conn,"Albuquerque, NM"))),
                     ("Mesa Verde", "Canyonlands",
                      self.distance(self.get_coords(conn,"Mesa Verde"),
                                    self.get_coords(conn,"Canyonlands"))),
                     ("Great Sand Dunes", "Pueblo, CO",
                      self.distance(self.get_coords(conn,"Great Sand Dunes"),
                                    self.get_coords(conn,"Pueblo, CO"))),
                     ("Great Sand Dunes", "Mesa Verde",
                      self.distance(self.get_coords(conn,"Great Sand Dunes"),
                                    self.get_coords(conn,"Mesa Verde"))),
                     ("Black Canyon of the Gunnison", "Arches",
                      self.distance(self.get_coords(conn,"Black Canyon of the Gunnison"),
                                    self.get_coords(conn,"Arches"))),
                     ("Black Canyon of the Gunnison", "Mesa Verde",
                      self.distance(self.get_coords(conn,"Black Canyon of the Gunnison"),
                                    self.get_coords(conn,"Mesa Verde"))),
                     ("Black Canyon of the Gunnison", "Denver, CO",
                      self.distance(self.get_coords(conn,"Black Canyon of the Gunnison"),
                                    self.get_coords(conn,"Denver, CO"))),
                     ("Rocky Mountain", "Denver, CO",
                      self.distance(self.get_coords(conn,"Rocky Mountain"),
                                    self.get_coords(conn,"Denver, CO"))),
                     ("Rocky Mountain", "Provo, UT",
                      self.distance(self.get_coords(conn,"Rocky Mountain"),
                                    self.get_coords(conn,"Provo, UT"))),
                     # Add so shows in list of parks - redundant
                     ("Bryce Canyon", "Capitol Reef",
                      self.distance(self.get_coords(conn,"Bryce Canyon"),
                                    self.get_coords(conn,"Capitol Reef")))
                     
                    ]
        # Class list of parks
        self._park_list = park_list
                           
        # Enter all of the edges                        
        self.graph.add_weighted_edges_from(mobile_list)
        self.graph.add_weighted_edges_from(lr_list)
        self.graph.add_weighted_edges_from(px_list)
        self.graph.add_weighted_edges_from(sf_list)
        self.graph.add_weighted_edges_from(la_list)
        self.graph.add_weighted_edges_from(den_list)
        self.graph.add_weighted_edges_from(n_hav_list)
        self.graph.add_weighted_edges_from(wilm_list)
        self.graph.add_weighted_edges_from(orl_list)
        self.graph.add_weighted_edges_from(atl_list)
        self.graph.add_weighted_edges_from(d_moi_list)
        self.graph.add_weighted_edges_from(bois_list)
        self.graph.add_weighted_edges_from(chi_list)
        self.graph.add_weighted_edges_from(ind_list)
        self.graph.add_weighted_edges_from(wich_list)
        self.graph.add_weighted_edges_from(lex_list)
        self.graph.add_weighted_edges_from(nola_list)
        self.graph.add_weighted_edges_from(bos_list)
        self.graph.add_weighted_edges_from(balt_list)
        self.graph.add_weighted_edges_from(port_list)
        self.graph.add_weighted_edges_from(grap_list)
        self.graph.add_weighted_edges_from(min_list)
        self.graph.add_weighted_edges_from(stl_list)
        self.graph.add_weighted_edges_from(jax_list)
        self.graph.add_weighted_edges_from(boze_list)
        self.graph.add_weighted_edges_from(faye_list)
        self.graph.add_weighted_edges_from(farg_list)
        self.graph.add_weighted_edges_from(omah_list)
        self.graph.add_weighted_edges_from(shua_list)
        self.graph.add_weighted_edges_from(atlc_list)
        self.graph.add_weighted_edges_from(albu_list)
        self.graph.add_weighted_edges_from(lv_list)
        self.graph.add_weighted_edges_from(nyc_list)
        self.graph.add_weighted_edges_from(clev_list)
        self.graph.add_weighted_edges_from(okc_list)
        self.graph.add_weighted_edges_from(eug_list)
        self.graph.add_weighted_edges_from(penn_list)
        self.graph.add_weighted_edges_from(grvl_list)
        self.graph.add_weighted_edges_from(pier_list)
        self.graph.add_weighted_edges_from(tenn_list)
        self.graph.add_weighted_edges_from(tx_list)
        #self.graph.add_weighted_edges_from(prov_list)
        #self.graph.add_weighted_edges_from(rmnd_list)
        self.graph.add_weighted_edges_from(wash_list)
        self.graph.add_weighted_edges_from(wisc_list)
        self.graph.add_weighted_edges_from(park_list)


    # Returns the list of national parks
    def get_parks(self):
        temp_list = []
        for item in self._park_list:
            temp_list.append(item[0])
        return temp_list

    # Find the closest nodes to start and end points
    # Returns closest starting city and closest ending city
    # as well as the distances
    def closest_nodes(self, loc1, loc2):
        start_node = ["", 3000]
        end_node = ["", 3000]

        # Connect to DB and make sure cities don't already exist
        # Connection string replaced with "" for security
        conn_str = ""

        # Connect to db
        conn = psycopg2.connect(conn_str)

        # Get the input locations' coords (true because user input)
        lat1, lng1 = self.get_coords(conn, loc1, True)
        lat2, lng2 = self.get_coords(conn, loc2, True)
        
        # Create a cursor
        cursor = conn.cursor()
        query_str = "INSERT INTO dijkstramap.latlng(city,lat,lng) "+\
                    "SELECT '" + loc1 + "'," + str(lat1) + ","+str(lng1)+\
                    " WHERE NOT EXISTS (SELECT * FROM " +\
                    "dijkstramap.latlng WHERE city='" + loc1 + "');"
        
        
        cursor.execute(query_str)
        conn.commit()
        
        query_str = "INSERT INTO dijkstramap.latlng(city,lat,lng) "+\
                    "SELECT '" + loc2 + "'," + str(lat2) + ","+str(lng2)+\
                    " WHERE NOT EXISTS (SELECT * FROM " +\
                    "dijkstramap.latlng WHERE city='" + loc2 + "');"
        cursor.execute(query_str)
        conn.commit()

        for city in self.graph.nodes():
            s_dist = self.distance(self.get_coords(conn,loc1),
                                   self.get_coords(conn,city))
            e_dist = self.distance(self.get_coords(conn,loc2),
                                   self.get_coords(conn,city))
            # Change the nearest city and distance if closer
            if s_dist < start_node[1]:
                start_node[0], start_node[1] = city, s_dist
            if e_dist < end_node[1]:
                end_node[0], end_node[1] = city, e_dist

        return start_node[0], start_node[1], end_node[0], end_node[1]

    # Update the instance's graph
    def update_graph(self, loc1, loc2, w):
        self.graph.add_edge(loc1, loc2, weight=w)

    # Returns the lat and long of a location
    def get_coords(self, conn, location, user_coords=False):
        if user_coords:
            # Get location information
            latlng = self.gmaps.geocode(location)
            # Get the location information in a string
            json1 = json.dumps(latlng[0])
            # Get the string in dict form so it's easier to work with
            json2 = json.loads(json1)
            # Get the lat and long
            lat = float(json2['geometry']['location']['lat'])
            lng = float(json2['geometry']['location']['lng'])
            
        else:
            # Create a cursor to interact with db
            cursor = conn.cursor()
            query_str = "SELECT lat, lng FROM dijkstramap.latlng " +\
                        "WHERE city='" + location + "';"
            
            cursor.execute(query_str)
            coords = cursor.fetchall()
            coords = coords[0]
            lat, lng = coords
            
        return lat, lng
        

            
    # Processes the user input into distinct city and state
    def process_inpt(self, user_inpt):
            city = user_inpt[0:user_inpt.find(',')]
            state = user_inpt[user_inpt.find(',')+1:].strip()
            
            return city, state

    # Uses the Haversine formula to determine distance between two locations
    """
            a = sin^2((lat2-lat1)/2) + cos(lat1)*cos(lat2)*sin^2((lng2-lng1)/2)
            c = 2*atan2(sqrt(a), sqrt(1-a))
            distance = earth's radius * c
            
            Angles are in radians.
    """
    def distance(self, loc1, loc2):
            # Radius of earth in miles
            e_rad = 3963.1676
            # Unpack the lat/lng tuples
            lat1, lng1 = loc1
            lat2, lng2 = loc2
            # Convert degrees to radians so formula works
            lat1, lat2, lng1, lng2 = math.radians(lat1), math.radians(lat2), + \
                                                             math.radians(lng1), math.radians(lng2)
            a = math.pow(math.sin((lat2-lat1)/2), 2) + \
                math.cos(lat1)*math.cos(lat2)*math.pow(math.sin((lng2-lng1)/2), 2)
            c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
            distance = e_rad * c
            
            return distance

    # Returns the distances using Dijkstra's, not as-the-crow-flies
    def d_distance(self, loc1, loc2):
        return networkx.dijkstra_path_length(self.graph, loc1, loc2)

    # Adds labels to the url
    def label_url(self, loc1, loc2):
        # Connection string replaced with "" for security
        conn_str = ""

        # Connect to db
        conn = psycopg2.connect(conn_str)
        
        # Determine the path using Dijkstra's algorithm
        self.d_path = networkx.dijkstra_path(self.graph, loc1, loc2)
        # Add markers to the url
        count = 0
        alpha_list = list(string.ascii_uppercase)
        for city in self.d_path:
            lat, lng = self.get_coords(conn,city)
            self.url = self.url + "&markers=color:yellow%7Clabel:" +\
                       alpha_list[count] + "%7C" +\
                       str(lat) + "," + str(lng)
            count = count + 1

        # Add a path to the url
        path = "&path=color:blue"

        for city in self.d_path:
            lat, lng = self.get_coords(conn,city)
            path = path + "|" +\
                   str(lat) + "," + str(lng)
            

        self.url = self.url + path

            
    # Put in a separate module later
    def print_map(self, root, loc1, loc2):
            # Set the title of the window
            title = "CityHop"
            root.wm_title(title)
            # Open the image url
            byte_data = urlopen(self.url)
            byte_data = byte_data.read()
            # Get an in-memory stream of bytes (image file)
            byte_stream = io.BytesIO(byte_data)
            # Open the image file using PIL
            img = Image.open(byte_stream)
            # Load the prepared image into Tkinter
            imgTK = ImageTk.PhotoImage(img)
            # Create a label with widget options
            label = tk.Label(root, image = imgTK, bg = 'linen')
            label.pack()
            # Prepare the items in the path list for display
            alpha_list = list(string.ascii_uppercase)
            zip_list = zip(alpha_list, self.d_path)
            print_path = str(round(self.d_distance(loc1, loc2))) + " Miles\n\n"

            frame = tk.Frame(root, bg = 'linen')
            newline_count = 0
            park_count = 0
            for pair in zip_list:
                if pair[1] not in self.get_parks():
                    print_path += ": ".join(pair) + "\t"*4
                elif pair[1] == "Black Canyon of the Gunnison":
                    print_path += ": ".join(pair) + " National Park\n\n"
                    park_count += 1
                else:
                    print_path += ": ".join(pair) + " National Park" +\
                                  "\t"*4
                    park_count += 1
                    
                newline_count += 1
                if newline_count == 2:
                    print_path += "\n\n"
                    newline_count = 0
            if park_count > 0:
                button1 = tk.Button(root, text="NPS site",
                                    highlightbackground="linen",
                                    cursor="ul_angle",
                                    command= lambda: open_url("http://www.nps.gov/findapark/index.htm"))
                button1.pack(side=tk.BOTTOM)            
            frame.pack(padx=0, pady=0, fill="y", expand=False, side="right")
            scroll = st(frame, wrap = tk.WORD, width=70, height = 20,
                        bg = 'linen', 
                        font = tkFont.Font(family="Helvetica", size=16))
            scroll.config(highlightthickness = 0)
            scroll.pack(fill="y", expand=False, side="right")
            scroll.insert(tk.INSERT, print_path)
            root.mainloop()

def get_url(base_url, search_term):
    google_search = "site: " + base_url + ' ' + search_term
    print "searching for ", google_search
    for item in search(google_search, stop=1):
        print "found ", item
        return item.encode("utf-8")

def open_url(url):
    webbrowser.open(url, new=2)

