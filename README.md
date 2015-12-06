# Restaurant Menu App

This app was created as [Full Stack Foundations](https://www.udacity.com/course/full-stack-foundations--ud088) and [Authentication & Authorization: OAuth](https://www.udacity.com/course/authentication-authorization-oauth--ud330) courses final project development.

## Requirements

Project was developed and reviewed according to this [rubric](http://imgur.com/bBuOnzA.png).

## How to use

App is deployed on heroku.com servers: http://desolate-bayou-9779.herokuapp.com/

## Features

App shows:
- restaurants from DB
- menu for each restaurant

App allows:
- register via Google or Facebook account
- add, edit or delete restaurants
- add, edit or delete menu items

## Technologies used

1. Flask framework
2. SQLite DB
3. SQLAlchemy python library
4. oauth2client python library
5. httplib2, json, requests, random, string, os python modules

## TODO

1. Add tests
2. Store images in FS (not by links from external resources)
3. Refactor template for Menu to make it more usefull
4. Integrate with some review and restaurant menu API