room_name_prompt = "Enter the Room/Area name: "

floor_prompt = """Enter the corresponding number for the Floor.
0. Basement
1. Ground
2. Floor 1
3. Floor 2
4. Floor 3
etc
"""

room_type_prompt = """Enter the corresponding number for the Room/Area type.
0. Office, 1. Classroom, 2. Kitchen, 3. Workshop, 4. Lab, 
5. Store Room, 6. Washroom, 7. Conference Room, 
8. Meeting Room, 9. Changing/Locker Room, 10. Electrical Room
"""

building_prompt = """Enter the corresponding number for the Building that the room is in.
0. Geomatics Engineering and Land Management, 
1. George Moonsammy Building (Block 9), 
2. Systems Lab (Block 11), 
3. Block 13 (Max Richards Building), 
4. Kenneth S. Julien Building (Block 1), 
5. Block 2 Civil Building, 
6. Civil/Chemical/Mechanical Labs
"""

observer_name_prompt = """What was the obeserver's name?
"""

interlude_listener_options = """q:quit, space:next,
"""



buildings = {
    0:"Geomatics Engineering and Land Management",
    1:"George Moonsammy Building",
    2:"Systems Laboratory",
    3:"Max Richards Building",
    4:"Kenneth S. Julien Building",
    5:"IDC Imbert Building",
    6:"Civil, Chemical and Mechanical Engineering Laboratories",
}


floors = {
    0:"Basement",
    'b':"Basement",
    1:"Ground",
    'g':"Ground",
    2:1,
    3:2,
    4:3,
    5:4,
    6:5,
}

room_types = {
    0:"Office",
    1:"Classroom",
    2:"Kitchen",
    3:"Workshop",
    4:"Lab",
    5:"Store Room",
    6:"Washroom",
    7:"Conference room",
}

effect_zones = {
    0:"Ceiling",
    1:"Walls",
    2:"Floor",
    3:"Windows",
    4:"Furnishings",
    5:"HVAC systems",
    6:"Supplies & Materials",
    7:"Pipes",
    8:"All components are more than 3 feet away from Exterior Wall",
    9:"No Exterior Walls",
    10:"No Effect/Zone",
}

ceiling_material = {
    0:"Ceiling Tile",
    1:"Plaster",
    2:"Concrete",
    3:"Sheet rock",
    4:"Metal",
    5:"Wood",
    6:"N/A",
}

wall_materials = {
    0:"Sheet rock",
    1:"Plaster",
    2:"Concrete",
    3:"Block",
    4:"Tile",
    5:"Wood",
    6:"N/A",
}

floor_material = {
    0:"Wood",
    1:"Carpet",
    2:"Vinyl",
    3:"Ceramic",
    4:"Concrete",
    5:"N/A",
}

windows_material = {
    0:"Exterior",
    1:"Interior",
    2:"skylight",
    3:"N/A",
}

furnishing = {
    0:"Furniture",
    1:"Mechanical",
    2:"Sink",
    3:"Toilet",
    4:"Copier",
    5:"N/A",
}

hvac_material = {
    0:"Forced Air",
    1:"Fan",
    2:"Unit Ventilator",
    3:"Window Unit",
    4:"N/A",
}

supplies_and_materials = {
    0:"Books",
    1:"Boxes",
    2:"Equipment",
    3:"N/A",
}

supplies_and_materials_desc = {
    0:"Wrinkled pages",
    1:"Crumpled boxes",
    2:"Other",
}