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
<option value="13" selected="">Yellow</option>
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