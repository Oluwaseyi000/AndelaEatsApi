"""A controller module for report-related activities
"""
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import and_
from app.controllers.base_controller import BaseController
from app.repositories import OrderRepo, VendorRatingRepo, VendorEngagementRepo, VendorRepo
from app.models import Order, Menu


class ReportsController(BaseController):
    def __init__(self, request):
        BaseController.__init__(self, request)
        self.rating_repo = VendorRatingRepo()
        self.order_repo = OrderRepo()
        self.engagement_repo = VendorEngagementRepo()
        self.vendor_repo = VendorRepo()

    def dashboard_summary(self):
        params = self.get_params_dict()

        if 'all_vendor_comparison' in params:
            orders = self.order_repo.fetch_all()
            vendors = self.vendor_repo.get_unpaginated(is_deleted=False)
            vendor_orders = []
            for vendor in vendors:
                vendor_info = {}
                vendor_info['id'] = vendor.id
                vendor_info['name'] = vendor.name
                vendor_info['collectedOrders'] = len([order for order in orders.items if
                                                    order.order_status == 'collected' and Menu.query.get(
                                                        order.menu_id).vendor_engagement.vendor_id == vendor.id])
                vendor_info['uncollectedOrders'] = len([order for order in orders.items if
                                                     order.order_status == 'booked' and Menu.query.get(
                                                         order.menu_id).vendor_engagement.vendor_id == vendor.id])
                vendor_info['cancelledOrders'] = len([order for order in orders.items if
                                                      order.order_status == 'cancelled' and Menu.query.get(
                                                          order.menu_id).vendor_engagement.vendor_id == vendor.id])
                vendor_orders.append(vendor_info)

            return self.handle_response('ok', payload=vendor_orders)

        str_start_date = params.get('start_date')
        start_date = datetime.now().date() if str_start_date is None else datetime.strptime(str_start_date, '%Y-%m-%d').date()

        str_end_date = params.get('end_date')
        end_date = (datetime.now().date() - timedelta(14)) if str_end_date is None else datetime.strptime(str_end_date, '%Y-%m-%d').date()

        if start_date < end_date:
            return self.handle_response('Start date must not be less than end date', status_code=400)

        orders = Order.query.filter(and_(Order.date_booked_for >= end_date, Order.date_booked_for <= start_date))
        orders_collected = [order for order in orders if order.order_status == 'collected']
        orders_cancelled = [order for order in orders if order.order_status == 'cancelled']
        orders_uncollected = [order for order in orders if order.order_status == 'booked']
        dates = [date.date() for date in pd.bdate_range(end_date, start_date)]
        result = []

        for date in dates:
            date_info = {
                'date': date,
                'collectedOrders': len([order for order in orders_collected if order.date_booked_for == date]),
                'uncollectedOrders': len([order for order in orders_uncollected if order.date_booked_for == date]),
                'cancelledOrders': len([order for order in orders_cancelled if order.date_booked_for == date]),
                'averageRating': self.rating_repo.daily_average_rating(date),
                'vendor': self.engagement_repo.vendor_of_the_day(date)
            }
            result.append(date_info)

        return self.handle_response('OK', payload=result)

