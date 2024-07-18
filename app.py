

from flask import Flask, request, render_template, redirect, url_for, session
import os
from werkzeug.utils import secure_filename
from transcribe import transcribe
import re
import spacy
import json
from collections import Counter

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
# app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
# app.secret_key = 'supersecretkey'
#
#
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
#
#
# # Function to download SpaCy model if not already downloaded
# def download_spacy_model():
#     try:
#         spacy.cli.download("en_core_web_sm")
#         print("Model downloaded successfully.")
#     except Exception as e:
#         print(f"An error occurred: {e}")
#
#
# # Ensure the SpaCy model is downloaded
# download_spacy_model()
#
# # Load SpaCy model for Named Entity Recognition (NER)
# nlp = spacy.load("en_core_web_sm")
#
# # Define the list of common grocery items
# food_dictionary = [
#     # Add your list of common grocery items here...
#     "apple", "banana", "carrot", "milk", "bread", "egg",
#     "tomato", "potato", "cheese", "lettuce", "beef", "pork", "fish", "butter",
#     "yogurt", "spinach", "broccoli", "orange", "grape", "strawberry", "blueberry",
#     "onion", "garlic", "cucumber", "pepper", "corn", "peas", "beans", "sugar",
#     "salt", "pepper", "flour", "oil", "vinegar", "mustard", "ketchup", "pasta",
#     "noodles", "soup", "cereal", "chocolate", "coffee", "tea", "juice", "soda",
#     "water", "wine", "beer", "whiskey", "vodka", "avocado", "apple", "banana", "carrot",
#     "milk", "bread", "egg", "chicken", "rice",
#     "tomato", "potato", "cheese", "lettuce", "beef", "pork", "fish", "butter",
#     "yogurt", "spinach", "broccoli", "orange", "grape", "strawberry", "blueberry",
#     "onion", "garlic", "cucumber", "pepper", "corn", "peas", "beans", "sugar",
#     "salt", "pepper", "flour", "oil", "vinegar", "mustard", "ketchup", "pasta",
#     "noodles", "soup", "cereal", "chocolate", "coffee", "tea", "juice", "soda",
#     "water", "wine", "beer", "whiskey", "avocado", "bacon", "ham", "sausage", "salmon",
#     "shrimp", "tuna", "oats", "granola", "pancake mix", "waffle mix", "muffin mix",
#     "cake mix", "brownie mix", "cornmeal", "baking powder", "baking soda", "yeast",
#     "cinnamon", "nutmeg", "vanilla extract", "almond extract", "soy sauce", "hot sauce",
#     "barbecue sauce", "olive oil", "canola oil", "sesame oil", "coconut oil", "avocado oil",
#     "rice vinegar", "balsamic vinegar", "red wine vinegar", "white vinegar", "apple cider vinegar",
#     "dill", "basil", "oregano", "parsley", "rosemary", "thyme", "cilantro", "chives", "ginger",
#     "turmeric", "coriander", "cumin", "paprika", "saffron", "cardamom", "cloves", "anise", "bay leaves",
#     "tarragon", "fenugreek", "allspice", "peppermint", "spearmint", "lavender", "lemongrass", "galangal",
#     "kaffir lime", "horseradish", "wasabi", "nutmeg", "mace", "caraway", "fennel", "poppy seeds",
#     "sesame seeds", "pumpkin seeds", "sunflower seeds", "chia seeds", "flax seeds", "hemp seeds",
#     "cocoa powder", "carob powder", "tahini", "hummus", "guacamole", "salsa", "pico de gallo",
#     "refried beans", "black beans", "kidney beans", "pinto beans", "chickpeas", "lentils", "split peas",
#     "mung beans", "adzuki beans", "cannellini beans", "navy beans", "butter beans", "fava beans",
#     "lima beans", "soybeans", "edamame", "tofu", "tempeh", "seitan", "falafel", "quinoa", "bulgur",
#     "farro", "barley", "millet", "spelt", "amaranth", "buckwheat", "teff", "kamut", "freekeh",
#     "sorghum", "wheat berries", "couscous", "polenta", "grits", "hominy", "masa harina", "corn tortillas",
#     "flour tortillas", "pita bread", "naan", "baguette", "ciabatta", "sourdough", "rye bread",
#     "pumpernickel", "whole wheat bread", "multigrain bread", "white bread", "brioche", "croissant",
#     "english muffin", "bagel", "focaccia", "chapati", "roti", "matzo", "lavash", "injera",
#     "pancakes", "waffles", "french toast", "crepes", "blintzes", "latkes", "hash browns",
#     "home fries", "tater tots", "fries", "curly fries", "sweet potato fries", "potato chips",
#     "tortilla chips", "pretzels", "popcorn", "crackers", "breadsticks", "rice cakes", "pita chips",
#     "graham crackers", "animal crackers", "goldfish crackers", "wheat thins", "triscuit", "cheez-it",
#     "club crackers", "saltines", "oyster crackers", "melba toast", "bagel chips", "rye crisps",
#     "naan chips", "veggie chips", "kale chips", "parsnip chips", "beet chips", "banana chips",
#     "plantain chips", "apple chips", "dried mango", "dried apricots", "dried figs", "dried dates",
#     "dried prunes", "dried cranberries", "dried cherries", "dried blueberries", "dried strawberries",
#     "dried raspberries", "raisins", "sultanas", "currants", "fig bars", "date bars", "granola bars",
#     "energy bars", "protein bars", "fruit leather", "fruit snacks", "trail mix", "mixed nuts",
#     "almonds", "cashews", "walnuts", "pecans", "hazelnuts", "brazil nuts", "macadamia nuts",
#     "pistachios", "peanuts", "peanut butter", "almond butter", "cashew butter", "sunflower seed butter",
#     "tahini", "nutella", "chocolate spread", "marshmallow fluff", "jelly", "jam", "marmalade",
#     "apple butter", "fruit preserves", "lemon curd", "orange curd", "lime curd", "cranberry sauce",
#     "applesauce", "pear sauce", "fruit compote", "fruit chutney", "fruit relish", "mint jelly",
#     "mint sauce", "honey mustard", "dijon mustard", "yellow mustard", "spicy brown mustard",
#     "whole grain mustard", "mayonnaise", "aioli", "remoulade", "tartar sauce", "horseradish sauce",
#     "cocktail sauce", "hot mustard", "honey", "maple syrup", "agave syrup", "corn syrup",
#     "molasses", "blackstrap molasses", "brown sugar", "coconut sugar", "turbinado sugar",
#     "demerara sugar", "powdered sugar", "confectioners' sugar", "icing sugar", "sanding sugar",
#     "decorating sugar", "colored sugar", "sprinkles", "nonpareils", "jimmies", "edible glitter",
#     "candy eyes", "chocolate chips", "white chocolate chips", "butterscotch chips", "peanut butter chips",
#     "caramel chips", "mint chips", "cinnamon chips", "fruit chips", "yogurt chips", "cookie dough",
#     "cookie mix", "brownie mix", "cake mix", "pancake mix", "waffle mix", "muffin mix",
#     "bread mix", "pizza dough", "pie crust", "phyllo dough", "puff pastry", "croissant dough",
#     "cookie dough", "gingerbread dough", "scone mix", "shortbread mix", "biscuit mix", "doughnut mix",
#     "fritter mix", "crepe mix", "pita bread", "naan", "bagels", "english muffins", "croissants",
#     "danish pastries", "cinnamon rolls", "coffee cake", "strudel", "turnovers", "empanadas",
#     "quesadillas", "burritos", "tacos", "enchiladas", "tamales", "flautas", "tostadas",
#     "nachos", "churros", "sopapillas", "gelato", "sorbet", "ice cream", "frozen yogurt",
#     "popsicles", "fudgesicles", "ice cream sandwiches", "ice cream cones", "waffle cones",
#     "sugar cones", "cake cones", "pretzel cones", "chocolate syrup", "caramel syrup",
#     "strawberry syrup", "marshmallow topping", "sprinkles", "nonpareils", "jimmies",
#     "chopped nuts", "whipped cream", "maraschino cherries", "candy canes", "peppermint bark",
#     "chocolate truffles", "chocolate bars", "candy bars", "licorice", "gummy bears",
#     "gummy worms", "gummy sharks", "gummy rings", "jelly beans", "jelly babies",
#     "marshmallows", "fruit slices", "hard candy", "lollipops", "jawbreakers", "candy corn",
#     "caramel corn", "toffee", "fudge", "divinity", "pralines", "brittle", "caramels",
#     "taffy", "nougat", "rock candy", "chocolates", "bonbons", "creme brulee", "flan",
#     "pudding", "custard", "jello", "fruit cocktail", "fruit salad", "berry mix",
#     "chocolate mousse", "vanilla pudding", "rice pudding", "tapioca pudding", "banana pudding",
#     "chocolate pudding", "vanilla ice cream", "kiwi", "mango", "papaya", "pineapple", "watermelon",
#     "cantaloupe", "honeydew", "dragon fruit",
#     "starfruit", "passion fruit", "pomegranate", "persimmon", "nectarine", "peach", "plum", "apricot",
#     "fig", "date", "guava", "lychee", "rambutan", "longan", "mulberry", "blackberry", "raspberry",
#     "boysenberry", "gooseberry", "currant", "elderberry", "cranberry", "kiwifruit", "pomelo", "quince",
#     "tangerine", "clementine", "satsuma", "mandarin", "ugli fruit", "kumquat", "coconut", "jackfruit",
#     "durian", "breadfruit", "sapodilla", "tamarind", "cherimoya", "soursop", "mangosteen", "jabuticaba",
#     "acerola", "salak", "langsat", "pequi", "pitaya", "lucuma", "bael", "marula", "miracle fruit",
#     "medlar", "bilberry", "cloudberry", "loganberry", "jostaberry", "serviceberry", "rowanberry", "seaberry",
#     "hackberry", "kiwano", "horned melon", "bitter melon", "fuzzy melon", "chayote", "jicama", "kohlrabi",
#     "radish", "daikon", "turnip", "rutabaga", "parsnip", "celeriac", "salsify", "jerusalem artichoke",
#     "artichoke", "cardoon", "asparagus", "bamboo shoot", "bean sprout", "bok choy", "broccolini", "broccoflower",
#     "brussels sprout", "cabbage", "cauliflower", "celery", "chard", "collard green", "endive", "escarole",
#     "fennel", "kale", "leek", "mustard green", "rapini", "spinach", "swiss chard", "watercress", "arugula",
#     "beet green", "dandelion green", "tatsoi", "mizuna", "amaranth", "quandong", "bunya nut", "macadamia",
#     "pecan", "pine nut", "water chestnut", "taro", "yam", "cassava", "plantain", "banana blossom", "bitterleaf",
#     "broad bean", "butter bean", "chickpea", "fava bean", "green bean", "lima bean", "mung bean", "snap pea",
#     "snow pea", "soybean", "yardlong bean", "adzuki bean", "black bean", "black-eyed pea", "chili pepper",
#     "bell pepper", "banana pepper", "cherry pepper", "jalapeno", "poblano", "serrano", "habanero", "scotch bonnet",
#     "ghost pepper", "carolina reaper", "pepperoncini", "cayenne pepper", "chipotle", "ancho chili", "guajillo chili",
#     "pasilla chili", "new mexico chili", "cubanelle pepper", "fresno pepper", "shishito pepper", "padron pepper",
#     "aji amarillo", "aji dulce", "rocoto", "chilaca", "mulato chili", "mirasol chili", "peppadew", "pimento",
#     "banana squash", "butternut squash", "acorn squash", "delicata squash", "hubbard squash", "kabocha squash",
#     "spaghetti squash", "zucchini", "yellow squash", "crookneck squash", "pattypan squash", "tatume", "chayote",
#     "calabaza", "cucamelon", "gourds", "bottle gourd", "sponge gourd", "ridge gourd", "snake gourd", "winter melon",
#     "cucumber", "gherkin", "burpless cucumber", "armenian cucumber", "lemon cucumber", "apple cucumber", "kiwano",
#     "mouse melon", "indian cucumber", "pumpkin", "sugar pumpkin", "cinderella pumpkin", "fairytale pumpkin",
#     "jack-o-lantern pumpkin", "mini pumpkin", "pie pumpkin", "white pumpkin", "blue pumpkin", "pink pumpkin",
#     "red kuri squash", "turban squash", "tromboncino", "zephyr squash", "zucchini blossoms", "courgette",
#     "cherry tomato", "grape tomato", "heirloom tomato", "roma tomato", "beefsteak tomato", "plum tomato",
#     "green tomato", "yellow tomato", "orange tomato", "black tomato", "striped tomato", "sungold tomato",
#     "brandywine tomato", "big boy tomato", "early girl tomato", "sweet 100 tomato", "black krim tomato",
#     "purple cherokee tomato", "green zebra tomato", "pineapple tomato", "jubilee tomato", "blush tomato",
#     "red pear tomato", "yellow pear tomato", "tomatillo", "cape gooseberry", "ground cherry", "husk tomato",
#     "mexican sour gherkin", "mouse melon", "garden huckleberry", "naranjilla", "lulo", "tamarillo", "pepino",
#     "melothria", "mouse melon", "potatoes", "zucchini", "brussel sprouts"
# ]
#
#
# def extract_food_items(text):
#     # Use SpaCy to find named entities related to food
#     doc = nlp(text)
#     food_items = set()
#
#     # Add items recognized by SpaCy's NER
#     for ent in doc.ents:
#         if ent.label_ in ["FOOD", "PRODUCT"]:
#             food_items.add(ent.text.lower())  # Convert to lowercase
#
#     # Add items found using the expanded dictionary
#     food_pattern = re.compile(r'\b(?:' + '|'.join(food_dictionary) + r')\b', re.IGNORECASE)
#     food_items.update([item.lower() for item in food_pattern.findall(text)])  # Convert to lowercase
#
#     return list(food_items)
#
#
# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return redirect(request.url)
#         file = request.files['file']
#         if file.filename == '':
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(filepath)
#             transcriber = transcribe(d=app.config['UPLOAD_FOLDER'])
#             text = transcriber.image_to_text(filename)
#             food_items = extract_food_items(text)
#             # Save food items to session or database
#             if 'inventory' not in session:
#                 session['inventory'] = []
#             session['inventory'].extend(food_items)
#             session['inventory'] = list(set(session['inventory']))  # Remove duplicates
#             session.modified = True
#             return render_template('result.html', text=text, food_items=food_items)
#     return render_template('upload.html')
#
#
# @app.route('/add_item', methods=['POST'])
# def add_item():
#     food_items = request.form.getlist('food_items')
#     new_item = request.form.get('new_item')
#     if new_item:
#         food_items.append(new_item)
#     session['inventory'] = list(set(food_items))  # Remove duplicates
#     session.modified = True
#     return render_template('result.html', text=request.form.get('text'), food_items=food_items)
#
# @app.route('/remove_item', methods=['POST'])
# def remove_item():
#     item_to_remove = request.form.get('item_to_remove')
#     if 'inventory' in session:
#         print(f"Attempting to remove item: {item_to_remove}")
#         print(f"Current inventory: {session['inventory']}")
#         session['inventory'] = [item for item in session['inventory'] if item != item_to_remove]
#         print(f"Updated inventory: {session['inventory']}")
#         session.modified = True
#     return redirect(url_for('inventory'))
#
# @app.route('/inventory')
# def inventory():
#     inventory = session.get('inventory', [])
#     return render_template('inventory.html', inventory=inventory)
#
#
# @app.route('/recipes')
# def recipes():
#     with open('/Users/mihikapall/PycharmProjects/pythonProject/grocery-app-test/data/recipes.json') as f:
#         recipes = json.load(f)
#     inventory_items = session.get('inventory', [])
#     recommended_recipes = recommend_recipes(inventory_items, recipes)
#     return render_template('recipes.html', recipes=recommended_recipes)
#
#
# def recommend_recipes(inventory_items, recipes):
#     inventory_counter = Counter([item.lower() for item in inventory_items])  # Convert to lowercase
#     recipe_scores = []
#     for recipe in recipes:
#         recipe_counter = Counter([ingredient.lower() for ingredient in recipe['ingredients']])
#         common_ingredients = inventory_counter & recipe_counter
#         score = sum(common_ingredients.values())
#         recipe_scores.append((score, recipe))
#     recipe_scores.sort(reverse=True, key=lambda x: x[0])
#     return [recipe for score, recipe in recipe_scores if score > 0]
#
#
# if __name__ == '__main__':
#     if not os.path.exists(app.config['UPLOAD_FOLDER']):
#         os.makedirs(app.config['UPLOAD_FOLDER'])
#     app.run(debug=True)

from flask import Flask, request, render_template, redirect, url_for, session
import os
from werkzeug.utils import secure_filename
from transcribe import transcribe
import re
import spacy
import json
from collections import Counter


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.secret_key = 'supersecretkey'




def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']




# Function to download SpaCy model if not already downloaded
def download_spacy_model():
   try:
       spacy.cli.download("en_core_web_sm")
       print("Model downloaded successfully.")
   except Exception as e:
       print(f"An error occurred: {e}")




# Ensure the SpaCy model is downloaded
download_spacy_model()


# Load SpaCy model for Named Entity Recognition (NER)
nlp = spacy.load("en_core_web_sm")


# Define the list of common grocery items
food_dictionary = [
   # Add your list of common grocery items here...
   "apple", "banana", "carrot", "milk", "bread", "egg",
   "tomato", "potato", "cheese", "lettuce", "beef", "pork", "fish", "butter",
   "yogurt", "spinach", "broccoli", "orange", "grape", "strawberry", "blueberry",
   "onion", "garlic", "cucumber", "pepper", "corn", "peas", "beans", "sugar",
   "salt", "pepper", "flour", "oil", "vinegar", "mustard", "ketchup", "pasta",
   "noodles", "soup", "cereal", "chocolate", "coffee", "tea", "juice", "soda",
   "water", "wine", "beer", "whiskey", "vodka", "avocado", "apple", "banana", "carrot",
   "milk", "bread", "egg", "chicken", "rice",
   "tomato", "potato", "cheese", "lettuce", "beef", "pork", "fish", "butter",
   "yogurt", "spinach", "broccoli", "orange", "grape", "strawberry", "blueberry",
   "onion", "garlic", "cucumber", "pepper", "corn", "peas", "beans", "sugar",
   "salt", "pepper", "flour", "oil", "vinegar", "mustard", "ketchup", "pasta",
   "noodles", "soup", "cereal", "chocolate", "coffee", "tea", "juice", "soda",
   "water", "wine", "beer", "whiskey", "avocado", "bacon", "ham", "sausage", "salmon",
   "shrimp", "tuna", "oats", "granola", "pancake mix", "waffle mix", "muffin mix",
   "cake mix", "brownie mix", "cornmeal", "baking powder", "baking soda", "yeast",
   "cinnamon", "nutmeg", "vanilla extract", "almond extract", "soy sauce", "hot sauce",
   "barbecue sauce", "olive oil", "canola oil", "sesame oil", "coconut oil", "avocado oil",
   "rice vinegar", "balsamic vinegar", "red wine vinegar", "white vinegar", "apple cider vinegar",
   "dill", "basil", "oregano", "parsley", "rosemary", "thyme", "cilantro", "chives", "ginger",
   "turmeric", "coriander", "cumin", "paprika", "saffron", "cardamom", "cloves", "anise", "bay leaves",
   "tarragon", "fenugreek", "allspice", "peppermint", "spearmint", "lavender", "lemongrass", "galangal",
   "kaffir lime", "horseradish", "wasabi", "nutmeg", "mace", "caraway", "fennel", "poppy seeds",
   "sesame seeds", "pumpkin seeds", "sunflower seeds", "chia seeds", "flax seeds", "hemp seeds",
   "cocoa powder", "carob powder", "tahini", "hummus", "guacamole", "salsa", "pico de gallo",
   "refried beans", "black beans", "kidney beans", "pinto beans", "chickpeas", "lentils", "split peas",
   "mung beans", "adzuki beans", "cannellini beans", "navy beans", "butter beans", "fava beans",
   "lima beans", "soybeans", "edamame", "tofu", "tempeh", "seitan", "falafel", "quinoa", "bulgur",
   "farro", "barley", "millet", "spelt", "amaranth", "buckwheat", "teff", "kamut", "freekeh",
   "sorghum", "wheat berries", "couscous", "polenta", "grits", "hominy", "masa harina", "corn tortillas",
   "flour tortillas", "pita bread", "naan", "baguette", "ciabatta", "sourdough", "rye bread",
   "pumpernickel", "whole wheat bread", "multigrain bread", "white bread", "brioche", "croissant",
   "english muffin", "bagel", "focaccia", "chapati", "roti", "matzo", "lavash", "injera",
   "pancakes", "waffles", "french toast", "crepes", "blintzes", "latkes", "hash browns",
   "home fries", "tater tots", "fries", "curly fries", "sweet potato fries", "potato chips",
   "tortilla chips", "pretzels", "popcorn", "crackers", "breadsticks", "rice cakes", "pita chips",
   "graham crackers", "animal crackers", "goldfish crackers", "wheat thins", "triscuit", "cheez-it",
   "club crackers", "saltines", "oyster crackers", "melba toast", "bagel chips", "rye crisps",
   "naan chips", "veggie chips", "kale chips", "parsnip chips", "beet chips", "banana chips",
   "plantain chips", "apple chips", "dried mango", "dried apricots", "dried figs", "dried dates",
   "dried prunes", "dried cranberries", "dried cherries", "dried blueberries", "dried strawberries",
   "dried raspberries", "raisins", "sultanas", "currants", "fig bars", "date bars", "granola bars",
   "energy bars", "protein bars", "fruit leather", "fruit snacks", "trail mix", "mixed nuts",
   "almonds", "cashews", "walnuts", "pecans", "hazelnuts", "brazil nuts", "macadamia nuts",
   "pistachios", "peanuts", "peanut butter", "almond butter", "cashew butter", "sunflower seed butter",
   "tahini", "nutella", "chocolate spread", "marshmallow fluff", "jelly", "jam", "marmalade",
   "apple butter", "fruit preserves", "lemon curd", "orange curd", "lime curd", "cranberry sauce",
   "applesauce", "pear sauce", "fruit compote", "fruit chutney", "fruit relish", "mint jelly",
   "mint sauce", "honey mustard", "dijon mustard", "yellow mustard", "spicy brown mustard",
   "whole grain mustard", "mayonnaise", "aioli", "remoulade", "tartar sauce", "horseradish sauce",
   "cocktail sauce", "hot mustard", "honey", "maple syrup", "agave syrup", "corn syrup",
   "molasses", "blackstrap molasses", "brown sugar", "coconut sugar", "turbinado sugar",
   "demerara sugar", "powdered sugar", "confectioners' sugar", "icing sugar", "sanding sugar",
   "decorating sugar", "colored sugar", "sprinkles", "nonpareils", "jimmies", "edible glitter",
   "candy eyes", "chocolate chips", "white chocolate chips", "butterscotch chips", "peanut butter chips",
   "caramel chips", "mint chips", "cinnamon chips", "fruit chips", "yogurt chips", "cookie dough",
   "cookie mix", "brownie mix", "cake mix", "pancake mix", "waffle mix", "muffin mix",
   "bread mix", "pizza dough", "pie crust", "phyllo dough", "puff pastry", "croissant dough",
   "cookie dough", "gingerbread dough", "scone mix", "shortbread mix", "biscuit mix", "doughnut mix",
   "fritter mix", "crepe mix", "pita bread", "naan", "bagels", "english muffins", "croissants",
   "danish pastries", "cinnamon rolls", "coffee cake", "strudel", "turnovers", "empanadas",
   "quesadillas", "burritos", "tacos", "enchiladas", "tamales", "flautas", "tostadas",
   "nachos", "churros", "sopapillas", "gelato", "sorbet", "ice cream", "frozen yogurt",
   "popsicles", "fudgesicles", "ice cream sandwiches", "ice cream cones", "waffle cones",
   "sugar cones", "cake cones", "pretzel cones", "chocolate syrup", "caramel syrup",
   "strawberry syrup", "marshmallow topping", "sprinkles", "nonpareils", "jimmies",
   "chopped nuts", "whipped cream", "maraschino cherries", "candy canes", "peppermint bark",
   "chocolate truffles", "chocolate bars", "candy bars", "licorice", "gummy bears",
   "gummy worms", "gummy sharks", "gummy rings", "jelly beans", "jelly babies",
   "marshmallows", "fruit slices", "hard candy", "lollipops", "jawbreakers", "candy corn",
   "caramel corn", "toffee", "fudge", "divinity", "pralines", "brittle", "caramels",
   "taffy", "nougat", "rock candy", "chocolates", "bonbons", "creme brulee", "flan",
   "pudding", "custard", "jello", "fruit cocktail", "fruit salad", "berry mix",
   "chocolate mousse", "vanilla pudding", "rice pudding", "tapioca pudding", "banana pudding",
   "chocolate pudding", "vanilla ice cream", "kiwi", "mango", "papaya", "pineapple", "watermelon",
   "cantaloupe", "honeydew", "dragon fruit",
   "starfruit", "passion fruit", "pomegranate", "persimmon", "nectarine", "peach", "plum", "apricot",
   "fig", "date", "guava", "lychee", "rambutan", "longan", "mulberry", "blackberry", "raspberry",
   "boysenberry", "gooseberry", "currant", "elderberry", "cranberry", "kiwifruit", "pomelo", "quince",
   "tangerine", "clementine", "satsuma", "mandarin", "ugli fruit", "kumquat", "coconut", "jackfruit",
   "durian", "breadfruit", "sapodilla", "tamarind", "cherimoya", "soursop", "mangosteen", "jabuticaba",
   "acerola", "salak", "langsat", "pequi", "pitaya", "lucuma", "bael", "marula", "miracle fruit",
   "medlar", "bilberry", "cloudberry", "loganberry", "jostaberry", "serviceberry", "rowanberry", "seaberry",
   "hackberry", "kiwano", "horned melon", "bitter melon", "fuzzy melon", "chayote", "jicama", "kohlrabi",
   "radish", "daikon", "turnip", "rutabaga", "parsnip", "celeriac", "salsify", "jerusalem artichoke",
   "artichoke", "cardoon", "asparagus", "bamboo shoot", "bean sprout", "bok choy", "broccolini", "broccoflower",
   "brussels sprout", "cabbage", "cauliflower", "celery", "chard", "collard green", "endive", "escarole",
   "fennel", "kale", "leek", "mustard green", "rapini", "spinach", "swiss chard", "watercress", "arugula",
   "beet green", "dandelion green", "tatsoi", "mizuna", "amaranth", "quandong", "bunya nut", "macadamia",
   "pecan", "pine nut", "water chestnut", "taro", "yam", "cassava", "plantain", "banana blossom", "bitterleaf",
   "broad bean", "butter bean", "chickpea", "fava bean", "green bean", "lima bean", "mung bean", "snap pea",
   "snow pea", "soybean", "yardlong bean", "adzuki bean", "black bean", "black-eyed pea", "chili pepper",
   "bell pepper", "banana pepper", "cherry pepper", "jalapeno", "poblano", "serrano", "habanero", "scotch bonnet",
   "ghost pepper", "carolina reaper", "pepperoncini", "cayenne pepper", "chipotle", "ancho chili", "guajillo chili",
   "pasilla chili", "new mexico chili", "cubanelle pepper", "fresno pepper", "shishito pepper", "padron pepper",
   "aji amarillo", "aji dulce", "rocoto", "chilaca", "mulato chili", "mirasol chili", "peppadew", "pimento",
   "banana squash", "butternut squash", "acorn squash", "delicata squash", "hubbard squash", "kabocha squash",
   "spaghetti squash", "zucchini", "yellow squash", "crookneck squash", "pattypan squash", "tatume", "chayote",
   "calabaza", "cucamelon", "gourds", "bottle gourd", "sponge gourd", "ridge gourd", "snake gourd", "winter melon",
   "cucumber", "gherkin", "burpless cucumber", "armenian cucumber", "lemon cucumber", "apple cucumber", "kiwano",
   "mouse melon", "indian cucumber", "pumpkin", "sugar pumpkin", "cinderella pumpkin", "fairytale pumpkin",
   "jack-o-lantern pumpkin", "mini pumpkin", "pie pumpkin", "white pumpkin", "blue pumpkin", "pink pumpkin",
   "red kuri squash", "turban squash", "tromboncino", "zephyr squash", "zucchini blossoms", "courgette",
   "cherry tomato", "grape tomato", "heirloom tomato", "roma tomato", "beefsteak tomato", "plum tomato",
   "green tomato", "yellow tomato", "orange tomato", "black tomato", "striped tomato", "sungold tomato",
   "brandywine tomato", "big boy tomato", "early girl tomato", "sweet 100 tomato", "black krim tomato",
   "purple cherokee tomato", "green zebra tomato", "pineapple tomato", "jubilee tomato", "blush tomato",
   "red pear tomato", "yellow pear tomato", "tomatillo", "cape gooseberry", "ground cherry", "husk tomato",
   "mexican sour gherkin", "mouse melon", "garden huckleberry", "naranjilla", "lulo", "tamarillo", "pepino",
   "melothria", "mouse melon", "potatoes", "zucchini", "brussel sprouts"
]




def extract_food_items(text):
   # Use SpaCy to find named entities related to food
   doc = nlp(text)
   food_items = set()


   # Add items recognized by SpaCy's NER
   for ent in doc.ents:
       if ent.label_ in ["FOOD", "PRODUCT"]:
           food_items.add(ent.text.lower())  # Convert to lowercase


   # Add items found using the expanded dictionary
   food_pattern = re.compile(r'\b(?:' + '|'.join(food_dictionary) + r')\b', re.IGNORECASE)
   food_items.update([item.lower() for item in food_pattern.findall(text)])  # Convert to lowercase


   return list(food_items)




@app.route('/', methods=['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
       if 'file' not in request.files:
           return redirect(request.url)
       file = request.files['file']
       if file.filename == '':
           return redirect(request.url)
       if file and allowed_file(file.filename):
           filename = secure_filename(file.filename)
           filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
           file.save(filepath)
           transcriber = transcribe(d=app.config['UPLOAD_FOLDER'])
           text = transcriber.image_to_text(filename)
           food_items = extract_food_items(text)
           # Save food items to session or database
           if 'inventory' not in session:
               session['inventory'] = []
           session['inventory'].extend(food_items)
           session['inventory'] = list(set(session['inventory']))  # Remove duplicates
           session.modified = True
           return render_template('result.html', text=text, food_items=food_items)
   return render_template('upload.html')




@app.route('/add_item', methods=['POST'])
def add_item():
   food_items = request.form.getlist('food_items')
   new_item = request.form.get('new_item')
   if new_item:
       food_items.append(new_item)
   session['inventory'] = list(set(food_items))  # Remove duplicates
   session.modified = True
   return render_template('result.html', text=request.form.get('text'), food_items=food_items)


@app.route('/remove_item', methods=['POST'])
def remove_item():
   item_to_remove = request.form.get('item_to_remove')
   if 'inventory' in session:
       session['inventory'] = [item for item in session['inventory'] if item != item_to_remove]
       session.modified = True
   return redirect(url_for('inventory'))


@app.route('/inventory')
def inventory():
   inventory = session.get('inventory', [])
   return render_template('inventory.html', inventory=inventory)




@app.route('/recipes')
def recipes():
   with open('/Users/mihikapall/PycharmProjects/pythonProject/grocery-app-test/data/recipes.json') as f:
       recipes = json.load(f)
   inventory_items = session.get('inventory', [])
   recommended_recipes = recommend_recipes(inventory_items, recipes)
   return render_template('recipes.html', recipes=recommended_recipes)




def recommend_recipes(inventory_items, recipes):
   inventory_counter = Counter([item.lower() for item in inventory_items])  # Convert to lowercase
   recipe_scores = []
   for recipe in recipes:
       recipe_counter = Counter([ingredient.lower() for ingredient in recipe['ingredients']])
       common_ingredients = inventory_counter & recipe_counter
       score = sum(common_ingredients.values())
       recipe_scores.append((score, recipe))
   recipe_scores.sort(reverse=True, key=lambda x: x[0])
   return [recipe for score, recipe in recipe_scores if score > 0]




if __name__ == '__main__':
   if not os.path.exists(app.config['UPLOAD_FOLDER']):
       os.makedirs(app.config['UPLOAD_FOLDER'])
   app.run(debug=True)
