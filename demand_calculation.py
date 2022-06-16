from datetime import datetime, timedelta
import time
import pytz
# import fcntl
import csv
import os
from copy import deepcopy


#https://solar-ops.notion.site/Peak-Demand-Calculation-d64d4eed3c8f441b96205f83d438d6f3


# Open and parse data from demand_example.csv into dictinoary:
energy_data = {'Datetime': [], 'energy_accumulated_kwh': []}


def find_peak_demand(start_datetime, end_datetime, window_type, window_length_minutes):
	"""
	Input:
	:start_datetime: ISOFormat datetime of period start
	:end_datetime: ISOFormat datetime of period end
	:window_type: String, either 'rolling' or 'time-based' to specify calculation method
	:window_length_minutes: Integer, number of minutes in a window

	Returns:
	dictionary with keys 'peak_demand' and 'start_datetime'
	:peak_demand: Integer, kW_demand of highest window
	:start_datetime: ISOFormat datetime of window start
	"""
	pass


"""
find_peak_demand('2021-09-01T08:00', '2021-09-01T09:00', 'rolling', 15)
#should return:
{
	"peak_demand": 4984
	"start_datetime": '2021-09-01T08:14'
}
"""

# ---------------------------------------------*---------------------------------*----------------------------------
# ---------------------------------------------*---------------------------------*----------------------------------


# extract the data from csv and keep it inside the dictionary.
def energy_data_returner():
	""" takes the csv file and returns the data dictionary."""

	filename = "demand_example.csv"
	datetime_list = []
	energy_data_list = []
	with open(filename, "r") as data:
		for line in csv.DictReader(data):
			values = list(line.values())
			datetime_list.append(values[0])
			energy_data_list.append(values[1])
	return {'Datetime': datetime_list, 'energy_accumulated_kwh': energy_data_list}		


# write a function to convert the string into the time format.
def time_returner(string_data):
	datetime_object = datetime.strptime(string_data, "%Y-%m-%dT%H:%M")
	return datetime_object

# write a function to convert the time into string format. If required.



windows = ["rolling", "time-based"]    # these are the types of windows.
window_lengths = [15, 30]    # these are the two types of window lengths.


def rolling_window_demand(start_datetime, end_datetime, window_length_minutes):
	energy_data = energy_data_returner()
	time_points_list = energy_data["Datetime"]
	energy_accumulated_list = energy_data["energy_accumulated_kwh"]


	timepoint_energy_dict = {}
	i = 0
	while i < len(time_points_list):

		timepointA = time_points_list[i]
		if (i + window_length_minutes) < len(time_points_list):
			timepointB = time_points_list[i + window_length_minutes]
			energy_at_A = energy_accumulated_list[i]
			energy_at_B = energy_accumulated_list[i + window_length_minutes]
			demand_power = (int(energy_at_B) - int(energy_at_A)) * (60/window_length_minutes)
			timepoint_energy_dict[timepointA] = demand_power
		i = i + 1
	
	sorted_list = sorted(timepoint_energy_dict.items(), key = lambda x:(x[1], x[0]))
	(time, demand) = sorted_list[-1]
	return {"peak_demand": demand, "start_datetime": time}


def time_based_window_demand(start_datetime, end_datetime, window_length_minutes):
	energy_data = energy_data_returner()
	time_points_list = energy_data["Datetime"]
	energy_accumulated_list = energy_data["energy_accumulated_kwh"]


	timepoint_energy_dict = {}
	i = 0
	while i < len(time_points_list):

		timepointA = time_points_list[i]
		if (i + window_length_minutes) < len(time_points_list):
			timepointB = time_points_list[i + window_length_minutes]
			energy_at_A = energy_accumulated_list[i]
			energy_at_B = energy_accumulated_list[i + window_length_minutes]
			demand_power = (int(energy_at_B) - int(energy_at_A)) * (60/window_length_minutes)
			timepoint_energy_dict[timepointA] = demand_power
		i = i + window_length_minutes
	
	sorted_list = sorted(timepoint_energy_dict.items(), key = lambda x:(x[1], x[0]))
	(time, demand) = sorted_list[-1]
	return {"peak_demand": demand, "start_datetime": time}


def find_peak_demand(start_datetime, end_datetime, window_type, window_length_minutes):
	if window_type == windows[0]:
		if window_length_minutes in window_lengths:
			a = start_datetime
			b = end_datetime
			window = window_length_minutes
			return rolling_window_demand(a, b, window)

	elif window_type == windows[1]:
		if window_length_minutes in window_lengths:
			a = start_datetime
			b = end_datetime
			window = window_length_minutes
			return time_based_window_demand(a, b, window)
	
	else:
		return "invalid window type, plz give proper window type"


if __name__=="__main__":
	print(find_peak_demand('2021-09-01T08:00', '2021-09-01T09:00', 'rolling', 15))
