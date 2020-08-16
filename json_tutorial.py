import json
from json import JSONEncoder, JSONDecoder

import requests


def example_1():
    x = {
        "name": "Ken",
        "age": 45,
        "married": True,
        "children": ("Alice", "Bob"),
        "pets": ['Dog'],
        "cars": [
            {"model": "Audi A1", "mpg": 15.1},
            {"model": "Zeep Compass", "mpg": 18.1}
        ]
    }
    # sorting result in ascending order by keys:
    sorted_string = json.dumps(x, indent=4, sort_keys=True)
    print(sorted_string)


def example_2():
    # json data string
    person_data = '{  "person":  { "name":  "Kenn",  "sex":  "male",  "age":  28}}'
    # Decoding or converting JSON format in dictionary using loads()
    dict_obj = json.loads(person_data)
    print(dict_obj)
    # check type of dict_obj
    print("Type of dict_obj", type(dict_obj))
    # get human object details
    print("Person......", dict_obj.get('person'))

    # here we create new data_file.json file with write mode using file i/o operation
    with open('json_file.json', "w") as file_write:
        # write json data into file
        json.dump(person_data, file_write)


def example_3():
    # File I/O Open function for read data from JSON File
    with open('json_file.json') as file_object:
        # store file data in object
        data = json.load(file_object)
    print(data)


def example_4():
    # Create a List that contains dictionary
    lst = ['a', 'b', 'c', {'4': 5, '6': 7}]
    # separator used for compact representation of JSON.
    # Use of ',' to identify list items
    # Use of ':' to identify key and value in dictionary
    compact_obj = json.dumps(lst, separators=(',', ':'))
    print(compact_obj)


def example_5():
    dic = {'a': 4, 'b': 5}
    ''' To format the code use of indent and 4 shows number of space and use of separator 
    is not necessary but standard way to write code of particular function. '''
    formatted_obj = json.dumps(dic, indent=4, separators=(',', ': '))
    print(formatted_obj)


def example_6():
    x = {
        "name": "Ken",
        "age": 45,
        "married": True,
        "children": ("Alice", "Bob"),
        "pets": ['Dog'],
        "cars": [
            {"model": "Audi A1", "mpg": 15.1},
            {"model": "Zeep Compass", "mpg": 18.1}
        ],
    }
    # sorting result in asscending order by keys:
    sorted_string = json.dumps(x, indent=4, sort_keys=True)
    print(sorted_string)


def complex_encode(object):
    # check using isinstance method
    if isinstance(object, complex):
        return [object.real, object.imag]
    # raised error using exception handling if object is not complex
    raise TypeError(repr(object) + " is not JSON serialized")


def example_7():
    # perform json encoding by passing parameter
    complex_obj = json.dumps(4 + 5j, default=complex_encode)
    print(complex_obj)


def is_complex(objct):
    if '__complex__' in objct:
        return complex(objct['real'], objct['img'])
    return objct

######################################################################
# this is my super duper comment explaining below
######################################################################


def example_8():
    complex_object = json.loads('{"__complex__": true, "real": 4, "img": 5}', object_hook=is_complex)
    # here we not passed complex object so it's convert into dictionary
    simple_object = json.loads('{"real": 6, "img": 7}', object_hook=is_complex)
    print("Complex_object......", complex_object)
    print("Without_complex_object......", simple_object)


def example_9():
    colour_dict = {"colour": ["red", "yellow", "green"]}
    # directly called encode method of JSON
    print(JSONEncoder().encode(colour_dict))


def example_10():
    colour_string = '{ "colour": ["red", "yellow"]}'
    # directly called decode method of JSON
    print(JSONDecoder().decode(colour_string))


def example_11():
    # get JSON string data from CityBike NYC using web requests library
    json_response = requests.get("https://feeds.citibikenyc.com/stations/stations.json")
    # check type of json_response object
    print(json_response.text)
    # load data in loads() function of json library
    bike_dict = json.loads(json_response.text)
    # check type of news_dict
    print(type(bike_dict))
    # now get stationBeanList key data from dict
    print(bike_dict['stationBeanList'][0])


def example_12():
    # File I/O Open function for read data from JSON File
    data = {}  # Define Empty Dictionary Object
    try:
        with open('json_file_name.json') as file_object:
            data = json.load(file_object)
    except ValueError:
        print("Bad JSON file format,  Change JSON File")


def example_13():
    # pass float Infinite value
    infinite_json = json.dumps(float('inf'))
    # check infinite json type
    print(infinite_json)
    print(type(infinite_json))
    json_nan = json.dumps(float('nan'))
    print(json_nan)
    # pass json_string as Infinity
    infinite = json.loads('Infinity')
    print(infinite)
    # check type of Infinity
    print(type(infinite))


