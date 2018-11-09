'''A module for menu controller'''
from app.controllers.base_controller import BaseController
from app.repositories.menu_repo import MenuRepo
from app.repositories.meal_item_repo import MealItemRepo
from app.utils.enums import MealPeriods
from datetime import datetime
import pdb



class MenuController(BaseController):
	'''Menu controller class'''
	def __init__(self, request):
		BaseController.__init__(self, request)
		self.menu_repo = MenuRepo()
		self.meal_repo = MealItemRepo()


	def create_menu(self):
		'''
		params are gotten from request object
		:return: json object with status of menu created with menu
		'''
		date, meal_period, main_meal_id, allowed_side,\
			allowed_protein, side_items, protein_items,\
			vendor_engagement_id = self.request_params(
				'date', 'mealPeriod', 'mainMealId', 'allowedSide',
				'allowedProtein', 'sideItems', 'proteinItems', 'vendorEngagementId'
			)
		print('YYYYYYYYYYYYYYYYYYYY', protein_items)

		menu = self.menu_repo.new_menu(
			date, meal_period, main_meal_id, allowed_side,
			allowed_protein, side_items, protein_items, vendor_engagement_id
		).serialize()

		menu['mainMeal'] = self.meal_repo.get(main_meal_id).serialize()
		menu['proteinItems'] = self.menu_repo.get_meal_items(protein_items)
		menu['sideItems'] = self.menu_repo.get_meal_items(side_items)
		return self.handle_response('OK', payload={'menu': menu}, status_code=201)

	def delete_menu(self, menu_id):
		'''

		:param menu_id: id of the menu
		:return: json object
		'''
		menu = self.menu_repo.get(menu_id)
		updates = {}
		if menu:
			if menu.is_deleted:
				return self.handle_response('Menu has already been deleted', status_code=400)

			updates['is_deleted'] = True

			self.meal_repo.update(menu, **updates)
			return self.handle_response('Menu deleted', payload={"status": "success"})
		return self.handle_response('Invalid or incorrect menu_id provided', status_code=400)

	def list_menus(self, menu_period, menu_date):
		'''retrieves a list of menus for a specific date for a specific meal period.
			date fornat: "YYYY-MM-DD"
			meal period: breakfast or lunch
			menu_date:  date of request
		'''
		if MealPeriods.has_value(menu_period):
			menus = self.menu_repo.get_unpaginated(date=menu_date, meal_period=menu_period, is_deleted=False)
			menu_list = []
			for menu in menus:
				serialised_menu = menu.serialize()
				arr_protein = menu.protein_items.split(",")
				arr_side = menu.side_items.split(",")
				serialised_menu['mainMeal'] = self.meal_repo.get(menu.main_meal_id).serialize()
				serialised_menu['proteinItems'] = self.menu_repo.get_meal_items(arr_protein)
				serialised_menu['sideItems'] = self.menu_repo.get_meal_items(arr_side)
				menu_list.append(serialised_menu)

			return self.handle_response(
				'OK', payload={'dateOfMeal': menu_date, 'mealPeriod': menu_period, 'menuList': menu_list}
			)

		return self.handle_response('Provide valid meal period and date', status_code=404)

	def list_menus_range(self, menu_period, menu_start_date, menu_end_date):
		'''retrieves a list of menus for a specific date range for a specific meal period.
			date fornat: "YYYY-MM-DD"
			meal period: breakfast or lunch
			menu_start_date: start date of search
			menu_end_date: end date of search
		'''
		if MealPeriods.has_value(menu_period):

			menus = self.menu_repo.get_range_unpaginated(
				start_date=menu_start_date, end_date=menu_end_date, meal_period=menu_period
			)
			menu_list = []
			for menu in menus:
				serialised_menu = menu.serialize()
				arr_protein = menu.protein_items.split(",")
				arr_side = menu.side_items.split(",")
				serialised_menu['mainMeal'] = self.meal_repo.get(menu.main_meal_id).serialize()
				serialised_menu['proteinItems'] = self.menu_repo.get_meal_items(arr_protein)
				serialised_menu['sideItems'] = self.menu_repo.get_meal_items(arr_side)
				menu_list.append(serialised_menu)

			return self.handle_response(
				'OK',
				payload={
					'startDateOfSearch': menu_start_date, 'endDateOfSearch': menu_end_date,
					'mealPeriod': menu_period, 'menuList': menu_list
				}
			)

		return self.handle_response('Provide valid meal period and date', status_code=404)

	def list_menus_range_page(self, menu_period, menu_start_date, menu_end_date, page_id, page_num):
		'''retrieves a list of menus for a specific date range for a specific meal period with pagination.
			date fornat: "YYYY-MM-DD"
			'''
		if MealPeriods.has_value(menu_period):

			menus = self.menu_repo.get_range_paginated(
				start_date=menu_start_date, end_date=menu_end_date, meal_period=menu_period,
				page_id=page_id, page_num=page_num
			)
			menu_list = []
			for menu in menus:
				serialised_menu = menu.serialize()
				arr_protein = menu.protein_items.split(",")
				arr_side = menu.side_items.split(",")
				serialised_menu['mainMeal'] = self.meal_repo.get(menu.main_meal_id).serialize()
				serialised_menu['proteinItems'] = self.menu_repo.get_meal_items(arr_protein)
				serialised_menu['sideItems'] = self.menu_repo.get_meal_items(arr_side)
				menu_list.append(serialised_menu)

			return self.handle_response(
				'OK',
				payload={
					'startDateOfSearch': menu_start_date, 'endDateOfSearch': menu_end_date,
					'mealPeriod': menu_period, 'menuList': menu_list
				}
			)

		return self.handle_response('Provide valid meal period and date', status_code=404)


	def update_menu(self, menu_id):
		'''

		:param menu_id: id of menu record
		:params other params sent via request_param
		:return:
		'''
		date, meal_period, main_meal_id, allowed_side,\
			allowed_protein, side_items, protein_items,\
			vendor_engagement_id = self.request_params(
				'date', 'mealPeriod', 'mainMealId', 'allowedSide',
				'allowedProtein', 'sideItems', 'proteinItems', 'vendorEngagementId'
				)
		pdb.set_trace()
		menu = self.menu_repo.get(menu_id)

		if menu:
			updates = {}
			if date:
				updates['date'] = datetime.strptime(date, '%Y-%m-%d')
			if meal_period:
				updates['meal_period'] = meal_period
			if main_meal_id:
				updates['main_meal_id'] = main_meal_id
			if allowed_side:
				updates['allowed_side'] = allowed_side
			if allowed_protein:
				updates['allowed_protein'] = allowed_protein
			if side_items:
				updates['side_items'] = ','.join(str(item) for item in side_items)
			if protein_items:
				updates['protein_items'] = ','.join(str(item) for item in protein_items)
			if vendor_engagement_id:
				updates['vendor_engagement_id'] = vendor_engagement_id

			updated_menu = self.menu_repo.update(menu, **updates)
			prot_items = [int(prot_id) for prot_id in updated_menu.protein_items if prot_id != ',']
			sid_items = [int(side_id) for side_id in updated_menu.protein_items if side_id != ',']

			menu = updated_menu.serialize()
			menu['mainMeal'] = self.meal_repo.get(updated_menu.main_meal_id).serialize()
			menu['proteinItems'] = self.menu_repo.get_meal_items(prot_items)
			menu['sideItems'] = self.menu_repo.get_meal_items(sid_items)
			return self.handle_response('OK', payload={'menu': menu}, status_code=200)

		return self.handle_response('This menu_id does not exist', status_code=404)
