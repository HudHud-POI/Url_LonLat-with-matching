# Url_LonLat-with-matching

## Project Overview

This project reads a file containing Google Maps links for photos but lacks latitude and longitude. It uses Selenium to extract the latitude and longitude from these links and saves them in specific columns in the photos file. Then, it matches this photos file with another database file using the latitude and longitude. If a match is found, it updates the relevant columns with the photos. If no match is found, it creates a new row with the place name, latitude, longitude, Google Maps link, and photos.

## Requirements
