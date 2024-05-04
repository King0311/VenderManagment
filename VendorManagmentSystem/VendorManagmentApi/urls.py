from django.urls import path , include
from . import views

urlpatterns = [
    path("",views.home,name="home"),

    #Creates a Vendor
    #Example Payload
    # {
    #     "vendor_code": 1,
    #     "name": "Pratik Agnihotri",
    #     "contact_detail": "9136325422",
    #     "address": "Kandivali,West",
    # }
    path("POST/api/vendor/",views.Vendor_POST),

    #Retrives all the Vendors
    path("GET/api/vendor/",views.Vendor_GET),

    #Retrive the specific Vendor
    path("GET/api/vendor/<int:pk>/",views.Vendor_GET),

    #Updates the Vendor data
    path("PUT/api/vendor/<int:pk>/",views.Vendor_PUT),

    # Deletes the Vendor
    path("DELETE/api/vendor/<int:pk>/",views.Vendor_DELETE),

    #########################################################

    # Creates the PO
    #Example Payload
    # {
    #     "po_number": 1,
    #     "del_date": "2024-05-01",
    #     "issue_date": "2024-04-24",
    #     "items": null,
    #     "quantity": 2,
    #     "status": "Pending",
    #     "vendor": 1
    # }
    path("POST/api/purchase_order/",views.Purchase_Order_POST),

    # Retrives all the PO
    path("GET/api/purchase_order/",views.Purchase_Order_GET),

    #Retrives the specific PO
    path("GET/api/purchase_order/<int:pk>/",views.Purchase_Order_GET),

    # Updates the PO data,but to change the status you need to 
    # first aknowledge the PO
    path("PUT/api/purchase_order/<int:pk>/",views.Purchase_Order_PUT),

    # Deletes the PO
    path("DELETE/api/purchase_order/<int:pk>/",views.Purchase_Order_DELETE),

    # Acknowledges the PO
    path("GET/api/purchase_order/<int:pk>/acknowledge/",views.Purchase_Order_ACK),
    ################################################################

    # Retrives the history performance
    path("api/vendor/<int:pk>/performance/", views.Performance),
]
