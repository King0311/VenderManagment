from django.shortcuts import render
from .models import Vendor,Purchase_Order
from .serializer import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import *
from datetime import datetime



# Create your views here.
@api_view()
def home(request):
    return Response("hello world")

# here is the history data functions

def On_Time_Delivery_Rate(exp,act):
    try:
        exp_d,act_d = str(exp) , str(act["del_date"])
        exp_d = datetime.strptime(exp_d,'%Y-%m-%d').date()
        act_d = datetime.strptime(act_d,'%Y-%m-%d').date()
        diff = (act_d - exp_d).days
        old_rate = Vendor.objects.get(vendor_code = act["vendor"])
        total_completed = Purchase_Order.objects.filter(vendor = act["vendor"],status = "Completed").count()
        if old_rate.on_time_del_rate == None:
            if diff <= 0:
                old_rate.on_time_del_rate = 1
            else:
                old_rate.on_time_del_rate = 0
        else:
            temp = (old_rate.on_time_del_rate) * (total_completed-1)
            if diff <= 0:
                new_rate = (temp + 1)/total_completed
            else:
                new_rate = temp/total_completed
            old_rate.on_time_del_rate = new_rate
        old_rate.save()
        if Vendor_Performance.objects.filter(vendor = act["vendor"]).exists():
            per = Vendor_Performance.objects.get(vendor = act["vendor"])
            per.on_time_del_rate = old_rate.on_time_del_rate
            per.save()
        else:
            Vendor_Performance.objects.create(vendor = old_rate, on_time_del_rate=old_rate.on_time_del_rate).save()
    except Exception as e:
        print(f"An error occurred: {e}")

def Quality_Rating_Average(pk):
    try:
        po = Purchase_Order.objects.filter(vendor = pk)
        count = 0
        total_rating = 0 
        for rating in po:
            if rating.rating != None:
                count = count + 1
                total_rating = total_rating + int(rating.rating)
        
        if total_rating > 0 and count > 0:
            avg = total_rating/count
            vendor = Vendor.objects.get(vendor_code = pk)
            vendor.avg_quality_rating = (avg)
            vendor.save()
            if Vendor_Performance.objects.filter(vendor = pk).exists():
                per = Vendor_Performance.objects.get(vendor = pk)
                per.avg_quality_rating = vendor.avg_quality_rating
                per.save()
            else:
                Vendor_Performance.objects.create(vendor = vendor, avg_quality_rating=vendor.avg_quality_rating).save()
    except Exception as e:
        print(f"An error occurred: {e}")
          
def Fulfilment_Rate(pk):
    try:
        po = Purchase_Order.objects.filter(vendor = pk)
        total_issued = po.count()
        total_completed = po.filter(status = "Completed").count()
        if total_completed != 0:
            vendor = Vendor.objects.get(vendor_code = pk)
            vendor.fulfillment_rate = (total_completed/total_issued)
            vendor.save()
            if Vendor_Performance.objects.filter(vendor = pk).exists():
                per = Vendor_Performance.objects.get(vendor = pk)
                per.fulfillment_rate = vendor.fulfillment_rate
                per.save()
            else:
                Vendor_Performance.objects.create(vendor = vendor, fulfillment_rate=vendor.fulfillment_rate).save()
    except Exception as e:
        print(f"An error occurred: {e}")

def Average_Response_Time(pk):
    try:
        po = Purchase_Order.objects.filter(vendor = pk)
        total_diff = 0
        count = 0
        for pos in po:
            if pos.issue_date != None and pos.ack_date != None:
                count = count + 1
                issue_d = str(pos.issue_date)
                ack_d = str(pos.ack_date)
                issue_d = datetime.strptime(issue_d,'%Y-%m-%d').date()
                ack_d = datetime.strptime(ack_d,'%Y-%m-%d').date()
                diff = round((ack_d - issue_d).days)
                total_diff = total_diff + diff
        print(total_diff,count)
        if total_diff != 0 and count != 0:
            vendor = Vendor.objects.get(vendor_code = pk.vendor_code)
            vendor.avg_response_time = round(total_diff/count)
            vendor.save()
            if Vendor_Performance.objects.filter(vendor = pk.vendor_code).exists():
                per = Vendor_Performance.objects.get(vendor = pk.vendor_code)
                per.avg_response_time = vendor.avg_response_time
                print(per.avg_quality_rating)
                per.save()
            else:
                Vendor_Performance.objects.create(vendor = pk, avg_response_time=vendor.avg_response_time).save()


    except Exception as e:
        print(f"An error occurred: {e}")


#This is the api for Curd operation on vendor model
#I can you and perbuilt api views like generic or 
# viewset to do this but to prove the logic building i did the most raw possible

@api_view(["POST"])
def Vendor_POST(request):
    if request.method == "POST":
        vendor_serializer = Vendor_Serializer(data=request.data)
        if vendor_serializer.is_valid():
            try:
                vendor_serializer.save()
                return Response({'message': "Vendor created successfully."}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'message': f'Error while saving vendor: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'message': vendor_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': "Wrong Request"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
def Vendor_PUT(request,pk):
    if request.method == "PUT":
        if not request.data:
            return Response({'message': "No data sent to update."}, status=status.HTTP_400_BAD_REQUEST)
        if pk is None:
            return Response({'message': "Which data to update not specified."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            vendor = Vendor.objects.get(vendor_code=pk)
            vendor_serializer = Vendor_Serializer(vendor, data=request.data, partial=True)
            if vendor_serializer.is_valid():
                vendor_serializer.save()
                return Response({'message': "Vendor data updated successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({'message': vendor_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'message': "Vendor not found."}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'message': "Wrong Request"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
def Vendor_DELETE(request,pk):
    if request.method == "DELETE":
        if pk is None:
            return Response({'message': "No vendor ID specified for deletion."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            vendor = Vendor.objects.get(vendor_code=pk)
            vendor.delete()
            return Response({'message': "Vendor successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({'message': "Vendor not found."}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'message': "Wrong Request"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def Vendor_GET(request,pk=None):
    if request.method == "GET":
        if pk is not None:
            try:
                vendor = Vendor.objects.get(vendor_code=pk)
                serializer = Vendor_Serializer(vendor)
                return Response(serializer.data)
            except ObjectDoesNotExist:
                return Response({'message': 'No data available'}, status=status.HTTP_404_NOT_FOUND)
        else:
            vendors = Vendor.objects.all()
            serializer = Vendor_Serializer(vendors, many=True)
            if vendors.exists():
                return Response(serializer.data)
            else:
                return Response({'message': 'No data available'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'message': "Wrong Request"}, status=status.HTTP_400_BAD_REQUEST) 
            
@api_view(["POST"])
def Purchase_Order_POST(request):
    if request.method == "POST":
        po_serializer = Purchase_Order_Serializer(data=request.data)
        if po_serializer.is_valid():
            try:
                po_serializer.save()
                return Response({'message': "Vendor created successfully."}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'message': f'Error while saving vendor: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'message': po_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': "Wrong Request"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
def Purchase_Order_PUT(request,pk):
    if request.method == "PUT":
        if not request.data:
            return Response({'message': "No data sent to update."}, status=status.HTTP_400_BAD_REQUEST)
        if pk is None:
            return Response({'message': "Which data to update not specified."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            po = Purchase_Order.objects.get(po_number=pk)
            old = po.del_date
            if "status" in request.data:
                if po.status == "Completed":
                    return Response({"message" : "Already Completed"},status=status.HTTP_400_BAD_REQUEST)
                elif po.ack_date != None:
                    if  request.data["status"] == "Completed" :
                        today = datetime.now()
                        formatted_datetime = today.strftime('%Y-%m-%d')
                        request.data["del_date"] = formatted_datetime
                else:
                    return Response({"message" : "You need to first Acknowledge the PO(Hit the Ack api)"},status=status.HTTP_400_BAD_REQUEST)
            po_serializer = Purchase_Order_Serializer(po, data=request.data, partial=True)
            if po_serializer.is_valid():
                po_serializer.save()
                if "status" in request.data:
                    if  request.data["status"] == "Completed":
                        Fulfilment_Rate(po_serializer.data["vendor"])
                        On_Time_Delivery_Rate(old,po_serializer.data)
                if "rating" in request.data:
                    Quality_Rating_Average(po_serializer.data["vendor"])
                print("here")
                return Response({'message': "PO data updated successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({'message': po_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'message': "PO not found."}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'message': "Wrong Request"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def Purchase_Order_ACK(request,pk):
    today = datetime.now()
    formatted_datetime = today.strftime('%Y-%m-%d')
    po = Purchase_Order.objects.get(po_number = pk)
    po.ack_date = formatted_datetime
    po.save()
    Average_Response_Time(po.vendor)
    return Response({'message': "Acknowledged"}, status=status.HTTP_200_OK)

@api_view(["DELETE"])
def Purchase_Order_DELETE(request,pk):
    if request.method == "DELETE":
        if pk is None:
            return Response({'message': "No PO ID specified for deletion."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            po = Purchase_Order.objects.get(po_number=pk)
            po.delete()
            return Response({'message': "PO successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({'message': "PO not found."}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'message': "Wrong Request"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def Purchase_Order_GET(request,pk=None):
    if request.method == "GET":
        if pk is not None:
            try:
                po = Purchase_Order.objects.get(po_number=pk)
                serializer = Purchase_Order_Serializer(po)
                return Response(serializer.data)
            except ObjectDoesNotExist:
                return Response({'message': 'No data available'}, status=status.HTTP_404_NOT_FOUND)
        else:
            po = Purchase_Order.objects.all()
            serializer = Purchase_Order_Serializer(po, many=True)
            if po.exists():
                return Response(serializer.data)
            else:
                return Response({'message': 'No data available'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'message': "Wrong Request"}, status=status.HTTP_400_BAD_REQUEST) 

            
    ######################################################################################################################################
    
    ######################################################################################################################################

    
            
    ######################################################################################################################################

@api_view(["GET"])
def Performance(request,pk):
    if request.method == 'GET':
        try:
            hist_data = Vendor_Performance.objects.filter(vendor = pk)
            serializer = Vendor_Performance_Serializer(hist_data,many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({'message': 'No data available'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'message': "Wrong Method."}, status=status.HTTP_400_BAD_REQUEST)
