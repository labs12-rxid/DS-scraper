import re
import numpy as np

# x = f"""

# removed by drugs.com
# <option value="7">Diamond</option>
# <option value="28">Square</option>

# """



drugs_shapes = f"""<option value="0">Select shape</option>
<option value="1">Barrel</option>
<option value="5">Capsule-shape</option>
<option value="6">Character-shape</option>
<option value="9">Egg-shape</option>
<option value="10">Eight-sided</option>
<option value="11">Elliptical / Oval</option>
<option value="12">Figure eight-shape</option>
<option value="13">Five-sided</option>
<option value="14">Four-sided</option>
<option value="15">Gear-shape</option>
<option value="16">Heart-shape</option>
<option value="18">Kidney-shape</option>
<option value="23">Rectangle</option>
<option value="24">Round</option>
<option value="25">Seven-sided</option>
<option value="27">Six-sided</option>
<option value="32">Three-sided</option>
<option value="33">U-shape</option>"""

drugs_colors = f"""<option value="12">White</option>
<option value="14">Beige</option>
<option value="73">Black</option>
<option value="1">Blue</option>
<option value="2">Brown</option>
<option value="3">Clear</option>
<option value="4">Gold</option>
<option value="5">Gray</option>
<option value="6">Green</option>
<option value="44">Maroon</option>
<option value="7">Orange</option>
<option value="74">Peach</option>
<option value="8">Pink</option>
<option value="9">Purple</option>
<option value="10">Red</option>
<option value="11">Tan</option>
<option value="12">White</option>
<option value="13">Yellow</option>
<option value="69">Beige & Red</option>
<option value="55">Black & Green</option>
<option value="70">Black & Teal</option>
<option value="48">Black & Yellow</option>
<option value="52">Blue & Brown</option>
<option value="45">Blue & Gray</option>
<option value="75">Blue & Green</option>
<option value="71">Blue & Orange</option>
<option value="53">Blue & Peach</option>
<option value="34">Blue & Pink</option>
<option value="19">Blue & White</option>
<option value="26">Blue & White Specks</option>
<option value="21">Blue & Yellow</option>
<option value="47">Brown & Clear</option>
<option value="54">Brown & Orange</option>
<option value="28">Brown & Peach</option>
<option value="16">Brown & Red</option>
<option value="57">Brown & White</option>
<option value="27">Brown & Yellow</option>
<option value="49">Clear & Green</option>
<option value="46">Dark & Light Green</option>
<option value="51">Gold & White</option>
<option value="61">Gray & Peach</option>
<option value="39">Gray & Pink</option>
<option value="58">Gray & Red</option>
<option value="67">Gray & White</option>
<option value="68">Gray & Yellow</option>
<option value="65">Green & Orange</option>
<option value="63">Green & Peach</option>
<option value="56">Green & Pink</option>
<option value="43">Green & Purple</option>
<option value="62">Green & Turquoise</option>
<option value="30">Green & White</option>
<option value="22">Green & Yellow</option>
<option value="42">Lavender & White</option>
<option value="40">Maroon & Pink</option>
<option value="50">Orange & Turquoise</option>
<option value="64">Orange & White</option>
<option value="23">Orange & Yellow</option>
<option value="60">Peach & Purple</option>
<option value="66">Peach & Red</option>
<option value="18">Peach & White</option>
<option value="15">Pink & Purple</option>
<option value="37">Pink & Red Specks</option>
<option value="29">Pink & Turquoise</option>
<option value="25">Pink & White</option>
<option value="72">Pink & Yellow</option>
<option value="17">Red & Turquoise</option>
<option value="35">Red & White</option>
<option value="20">Red & Yellow</option>
<option value="33">Tan & White</option>
<option value="59">Turquoise & White</option>
<option value="24">Turquoise & Yellow</option>
<option value="32">White & Blue Specks</option>
<option value="41">White & Red Specks</option>
<option value="38">White & Yellow</option>
<option value="31">Yellow & Gray</option>
<option value="36">Yellow & White</option>"""

mo = re.findall(r'\<option value\="(\d{1,2})"\>([\w-]+)\<', drugs_shapes)
shape_array = list(np.zeros(34, dtype=str))
for o in mo:
    shape_array[int(o[0])] = o[1]

mo = re.findall(r'\<option value\="(\d{1,2})"\>([\w\s&]+)\<', drugs_colors)
color_array = list(np.zeros(76, dtype=str))
for o in mo:
    if int(o[0]) > 75:
        print('high color', o)
        break
    color_array[int(o[0])] = o[1]  
print('yellow????', color_array[13])

shape_codes = [
    {"id": -1, "name": 'unspecified', 'code': -1},
    {"id": 0, "name": 'Round', 'code': 24},
    {"id": 1, "name": 'Capsule', 'code': 5},
    {"id": 2, "name": 'Oval', "code": 20},
    {"id": 3, "name": 'Egg', "code":  9},
    {"id": 4, "name": 'Barrel', "code": 1},
    {"id": 5, "name": 'Rectangle', "code": 23},
    {"id": 6, "name": '3 Sided', "code": 32},
    {"id": 7, "name": '4 Sided', "code": 14},
    {"id": 8, "name": '5 Sided', "code": 13},
    {"id": 9, "name": '6 Sided', "code": 27},
    {"id": 10, "name": '7 sided', "code": 25},
    {"id": 11, "name": '8 sided', "code": 10},
    {"id": 12, "name": 'U Shaped', "code": 33},
    {"id": 13, "name": 'Figure 8', "code": 12},
    {"id": 14, "name": 'Heart', "code": 16},
    {"id": 15, "name": 'Kidney', "code": 18},
    {"id": 16, "name": 'Gear', "code": 15},
    {"id": 17, "name": 'Character', "code": 6}
    # {"id": 18, "name": 'Diamand', "code": 7}, # these were removed by drugs.com
    # {"id": 19, "name": 'Square', "code": 28},
]
color_codes = [
    {'id': 0, 'name': 'Beige', 'code': 14},
    {'id': 1, 'name': 'Black', 'code': 73},
    {'id': 2, 'name': 'Blue', 'code': 1},
    {'id': 3, 'name': 'Brown', 'code': 2},
    {'id': 4, 'name': 'Clear', 'code': 3},
    {'id': 5, 'name': 'Gold', 'code': 4},
    {'id': 6, 'name': 'Gray', 'code': 5},
    {'id': 7, 'name': 'Green', 'code': 6},
    {'id': 8, 'name': 'Maroon', 'code': 44},
    {'id': 9, 'name': 'Orange', 'code': 7},
    {'id': 10, 'name': 'Peach', 'code': 74},
    {'id': 11, 'name': 'Pink', 'code': 8},
    {'id': 12, 'name': 'Purple', 'code': 9},
    {'id': 13, 'name': 'Red', 'code': 10},
    {'id': 14, 'name': 'Tan', 'code': 11},
    {'id': 15, 'name': 'White', 'code': 12},
    {'id': 16, 'name': 'Yellow', 'code': 13},            
    {'id': 0, 'name': 'Beige & Beige', 'code': 14},
    {'id': 1, 'name': 'Black & Black', 'code': 73},
    {'id': 2, 'name': 'Blue & Blue', 'code': 1},
    {'id': 3, 'name': 'Brown & Brown', 'code': 2},
    {'id': 4, 'name': 'Clear & Clear', 'code': 3},
    {'id': 5, 'name': 'Gold & Gold', 'code': 4},
    {'id': 6, 'name': 'Gray & Gray', 'code': 5},
    {'id': 7, 'name': 'Green & Green', 'code': 6},
    {'id': 8, 'name': 'Maroon & Maroon', 'code': 44},
    {'id': 9, 'name': 'Orange & Orange', 'code': 7},
    {'id': 10, 'name': 'Peach & Peach', 'code': 74},
    {'id': 11, 'name': 'Pink & Pink', 'code': 8},
    {'id': 12, 'name': 'Purple & Purple', 'code': 9},
    {'id': 13, 'name': 'Red & Red', 'code': 10},
    {'id': 14, 'name': 'Tan & Tan', 'code': 11},
    {'id': 15, 'name': 'White & White', 'code': 12},
    {'id': 16, 'name': 'Yellow & Yellow', 'code': 13},
    {'id': 17, 'name': 'Beige & Red', 'code': 69},
    {'id': 18, 'name': 'Black & Green', 'code': 55},
    {'id': 19, 'name': 'Black & Teal', 'code': 70},
    {'id': 20, 'name': 'Black & Yellow', 'code': 48},
    {'id': 21, 'name': 'Blue & Brown', 'code': 52},
    {'id': 22, 'name': 'Blue & Grey', 'code': 45},
    {'id': 23, 'name': 'Blue & Orange', 'code': 71},
    {'id': 24, 'name': 'Blue & Peach', 'code': 53},
    {'id': 25, 'name': 'Blue & Pink', 'code': 34},
    {'id': 26, 'name': 'Blue & White', 'code': 19},
    {'id': 27, 'name': 'Blue & White Specks', 'code': 26},
    {'id': 28, 'name': 'Blue & Yellow', 'code': 21},
    {'id': 29, 'name': 'Brown & Clear', 'code': 47},
    {'id': 30, 'name': 'Brown & Orange', 'code': 54},
    {'id': 31, 'name': 'Brown & Peach', 'code': 28},
    {'id': 32, 'name': 'Brown & Red', 'code': 16},
    {'id': 33, 'name': 'Brown & White', 'code': 57},
    {'id': 34, 'name': 'Brown & Yellow', 'code': 27}, 
    {'id': 35, 'name': 'Clear & Green', 'code': 49},
    {'id': 36, 'name': 'Dark & Light Green', 'code': 46},
    {'id': 37, 'name': 'Gold & White', 'code': 51},
    {'id': 38, 'name': 'Grey & Peach', 'code': 63},
    {'id': 39, 'name': 'Grey & Pink', 'code': 39},
    {'id': 40, 'name': 'Grey & Red', 'code':58},
    {'id': 41, 'name': 'Grey & White', 'code': 51},
    {'id': 42, 'name': 'Grey & Yellow', 'code': 68},
    {'id': 43, 'name': 'Green & Orange', 'code': 65},
    {'id': 44, 'name': 'Green & Peach', 'code': 63},
    {'id': 45, 'name': 'Green & Pink', 'code': 56},
    {'id': 46, 'name': 'Green & Purple', 'code': 43},
    {'id': 47, 'name': 'Green & Turquoise', 'code': 62},
    {'id': 48, 'name': 'Green & White', 'code': 30},
    {'id': 49, 'name': 'Green & Yellow', 'code': 22},
    {'id': 50, 'name': 'Lavender & White', 'code': 42},
    {'id': 51, 'name': 'Maroon & Pink', 'code': 40},
    {'id': 52, 'name': 'Orange & Turquoise', 'code': 50},
    {'id': 53, 'name': 'Orange & White', 'code': 64},
    {'id': 54, 'name': 'Orange & Yellow', 'code': 23},
    {'id': 55, 'name': 'Peach & Purple', 'code': 60},
    {'id': 56, 'name': 'Peach & Red', 'code': 66},
    {'id': 57, 'name': 'Peach & White', 'code': 18},
    {'id': 58, 'name': 'Pink & Purple', 'code': 15},
    {'id': 59, 'name': 'Pink & Red Specks', 'code': 37},
    {'id': 60, 'name': 'Pink & Turquoise', 'code': 29},
    {'id': 61, 'name': 'Pink & White', 'code': 25},
    {'id': 62, 'name': 'Pink & Yellow', 'code': 72},
    {'id': 63, 'name': 'Red & Turquoise', 'code': 17},
    {'id': 64, 'name': 'Red & White', 'code': 35},
    {'id': 65, 'name': 'Red & Yellow', 'code': 20},
    {'id': 66, 'name': 'Tan & White', 'code': 33},
    {'id': 67, 'name': 'Turquoise & White', 'code': 59},
    {'id': 68, 'name': 'Turquuise & Yellow', 'code': 24},
    {'id': 69, 'name': 'White & Blue Specks', 'code': 32},
    {'id': 70, 'name': 'White & Red Specks', 'code': 41},
    {'id': 71, 'name': 'White & Yellow', 'code': 38},
    {'id': 72, 'name': 'Yellow & Grey', 'code': 31},
    {'id': 73, 'name': 'Yellow & White', 'code': 36}]

color_table = \
    """
        Beige	#F5F5DC	(245,245,220)
        Black	#000000	(0,0,0)
        Blue	#0000FF	(0,0,255)
        Brown	#A52A2A	(165,42,42)
        Gold	#FFD700	(255,215,0)
        Gray 	#808080	(128,128,128)
        Green	#008000	(0,128,0)
        Maroon	#800000	(128,0,0)
        Orange	#FFA500	(255,165,0)
        Peach	#FFDAB9	(255,218,185)
        Pink	#FFC0CB	(255,192,203)
        Purple	#800080	(12,0,128)
        Red     #FF0000	(255,0,0)
        Tan     #D2B48C	(210,180,140)
        White	#FFFFFF	(255,255,255)
        Yellow	#FFFF00	(255,255,0)
        """
color_map = {
    'beige': ['white', 'brown', 'gray', 'tan'],
    'brown': ['beige'],
    'gray': ['beige', 'white'],
    'maroon': ['red', 'purple'],
    'peach': ['pink'],
    'pink': ['peach'],
    'purple': ['maroon'],
    'red': ['maroon'],
    'tan': ['beige'],
    'white': ['beige', 'tan', 'yellow', 'gray'],
    'yellow': ['white']
}
shape_map = {
    'oval': ['egg-shape', 'egg', 'elliptical / oval'],
    'egg': ['egg-shape','oval',' elliptical / oval'],
    'capsule': ['capsule-shape'],
    'square': ['four-sided', 'rectangle'],
    'rectangle': ['four-sided'],
    'four-sided': ['rectangle'],
    'diamand': ['four-sided']
    }
  