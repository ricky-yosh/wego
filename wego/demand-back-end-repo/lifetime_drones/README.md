# WeGo Plugin App Template

This is a custom Django app template to quickly create new plugins for WeGo's TaaS solutions web service.

## Usage

To use this template: run the following command, replacing `new_app_name` with the desired name for your new app:

   ```bash
   python manage.py startapp --template=./plugin_template new_plugin_name
   ```

This template imports models, managers, and views from plugin_skeleton.
## Contents
- **models.py**
    - Contains definitions for Item and Order objects and functions related to them.
- **tests.py**
    - Contains tests for all functions in models.
- **urls.py**
    - Contains urls to each API endpoint
- **serializers.py**
    - Contains serializers to convert data into json data
- **views.py**
    - Contains functionality for API endpoints by primarily calling functions in models.py.

## Base API Ednpoints in views.py
- **add-item-to-inventory/**
- **remove-item-from-inventory/**
- **get-inventory/**
- **create-order/**
- **submit-order/**
- **create-and-submit-order/**
- **cancel-order/**
- **get-order-status/**
- **get-order-history/**
- **get-trip-status/**