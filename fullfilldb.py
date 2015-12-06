from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from restaurants.models import Restaurant, Base, MenuItem, User

#engine = create_engine('sqlite:///restaurantmenu.db')
engine = create_engine('postgres://oayymjoacnwrzl:6z1aa9scW0slIYh-B_V5VKGKc-@ec2-46-137-72-123.eu-west-1.compute.amazonaws.com:5432/d1ve6bgi7vcigp')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
User1 = User(name="Robo Barista", email="alexey.drozdov@gmail.com",
             img='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()


#Menu for UrbanBurger
restaurant1 = Restaurant(user_id=1, name = "Urban Burger", address="1600 Pennsylvania Ave NW,Washington, DC 20500, USA", phone="+123456789", website="google.com", cousine="French", img="http://www.pulpolocal.com/wp-content/uploads/2013/11/ryba-11-200x300.jpg")
session.add(restaurant1)
session.commit()

menuItem1 = MenuItem(user_id=1, name = "French Fries", description = "with garlic and parmesan", price = "$2.99", course = "Appetizer", restaurant = restaurant1, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(user_id=1, name = "Veggie Burger", description = "Juicy grilled veggie patty with tomato mayo and lettuce", price = "$7.50", course = "Entree", restaurant = restaurant1, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(user_id=1, name = "Chicken Burger", description = "Juicy grilled chicken patty with tomato mayo and lettuce", price = "$5.50", course = "Entree", restaurant = restaurant1, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(user_id=1, name = "Chocolate Cake", description = "fresh baked and served with ice cream", price = "$3.99", course = "Dessert", restaurant = restaurant1, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem4)
session.commit()

menuItem5 = MenuItem(user_id=1, name = "Sirloin Burger", description = "Made with grade A beef", price = "$7.99", course = "Entree", restaurant = restaurant1, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem5)
session.commit()

menuItem6 = MenuItem(user_id=1, name = "Root Beer", description = "16oz of refreshing goodness", price = "$1.99", course = "Beverage", restaurant = restaurant1, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem6)
session.commit()

menuItem7 = MenuItem(user_id=1, name = "Iced Tea", description = "with Lemon", price = "$.99", course = "Beverage", restaurant = restaurant1, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem7)
session.commit()

menuItem8 = MenuItem(user_id=1, name = "Grilled Cheese Sandwich", description = "On texas toast with American Cheese", price = "$3.49", course = "Entree", restaurant = restaurant1, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem8)
session.commit()

menuItem9 = MenuItem(user_id=1, name = "Veggie Burger", description = "Made with freshest of ingredients and home grown spices", price = "$5.99", course = "Entree", restaurant = restaurant1, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem9)
session.commit()


#Menu for Super Stir Fry
restaurant2 = Restaurant(user_id=1, name = "Super Stir Fry", address="1600 Pennsylvania Ave NW,Washington, DC 20500, USA", phone="+123456789", website="google.com", cousine="French", img="http://www.sandiegomagazine.com/San-Diego-Magazine/November-2011/Thanksgiving-Alfresco/thanksgiving-san-diego-magazine-1.jpg")
session.add(restaurant2)
session.commit()

menuItem1 = MenuItem(user_id=1, name = "Chicken Stir Fry", description = "With your choice of noodles vegetables and sauces", price = "$7.99", course = "Entree", restaurant = restaurant2, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(user_id=1, name = "Peking Duck", description = " A famous duck dish from Beijing[1] that has been prepared since the imperial era. The meat is prized for its thin, crisp skin, with authentic versions of the dish serving mostly the skin and little meat, sliced in front of the diners by the cook", price = "$25", course = "Entree", restaurant = restaurant2, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(user_id=1, name = "Spicy Tuna Roll", description = "Seared rare ahi, avocado, edamame, cucumber with wasabi soy sauce ", price = "15", course = "Entree", restaurant = restaurant2, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(user_id=1, name = "Nepali Momo ", description = "Steamed dumplings made with vegetables, spices and meat. ", price = "12", course = "Entree", restaurant = restaurant2, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem4)
session.commit()

menuItem5 = MenuItem(user_id=1, name = "Beef Noodle Soup", description = "A Chinese noodle soup made of stewed or red braised beef, beef broth, vegetables and Chinese noodles.", price = "14", course = "Entree", restaurant = restaurant2, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem5)
session.commit()

menuItem6 = MenuItem(user_id=1, name = "Ramen", description = "a Japanese noodle soup dish. It consists of Chinese-style wheat noodles served in a meat- or (occasionally) fish-based broth, often flavored with soy sauce or miso, and uses toppings such as sliced pork, dried seaweed, kamaboko, and green onions.", price = "12", course = "Entree", restaurant = restaurant2, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem6)
session.commit()


#Menu for Panda Garden
restaurant3 = Restaurant(user_id=1, name = "Panda Garden", address="1600 Pennsylvania Ave NW,Washington, DC 20500, USA", phone="+123456789", website="google.com", cousine="French", img="http://r-ec.bstatic.com/images/hotel/max300/430/43085706.jpg")
session.add(restaurant3)
session.commit()

menuItem1 = MenuItem(user_id=1, name = "Pho", description = "a Vietnamese noodle soup consisting of broth, linguine-shaped rice noodles called banh pho, a few herbs, and meat.", price = "$8.99", course = "Entree", restaurant = restaurant3, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(user_id=1, name = "Chinese Dumplings", description = "a common Chinese dumpling which generally consists of minced meat and finely chopped vegetables wrapped into a piece of dough skin. The skin can be either thin and elastic or thicker.", price = "$6.99", course = "Appetizer", restaurant = restaurant3, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(user_id=1, name = "Gyoza", description = "The most prominent differences between Japanese-style gyoza and Chinese-style jiaozi are the rich garlic flavor, which is less noticeable in the Chinese version, the light seasoning of Japanese gyoza with salt and soy sauce, and the fact that gyoza wrappers are much thinner", price = "$9.95", course = "Entree", restaurant = restaurant3, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(user_id=1, name = "Stinky Tofu", description = "Taiwanese dish, deep fried fermented tofu served with pickled cabbage.", price = "$6.99", course = "Entree", restaurant = restaurant3, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem4)
session.commit()

menuItem4 = MenuItem(user_id=1, name = "Veggie Burger", description = "Juicy grilled veggie patty with tomato mayo and lettuce", price = "$9.50", course = "Entree", restaurant = restaurant3, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem4)
session.commit()


#Menu for Thyme for that
restaurant4 = Restaurant(user_id=1, name = "Thyme for That Vegetarian Cuisine ", address="1600 Pennsylvania Ave NW,Washington, DC 20500, USA", phone="+123456789", website="google.com", cousine="French", img="http://alberghi.ultrahotels.net/images/hotels/zoom/b/36/36cb8610934c2b89da6f6fff639b853c.jpg")
session.add(restaurant4)
session.commit()

menuItem1 = MenuItem(user_id=1, name = "Tres Leches Cake", description = "Rich, luscious sponge cake soaked in sweet milk and topped with vanilla bean whipped cream and strawberries.", price = "$2.99", course = "Dessert", restaurant = restaurant4, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(user_id=1, name = "Mushroom risotto", description = "Portabello mushrooms in a creamy risotto", price = "$5.99", course = "Entree", restaurant = restaurant4, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(user_id=1, name = "Honey Boba Shaved Snow", description = "Milk snow layered with honey boba, jasmine tea jelly, grass jelly, caramel, cream, and freshly made mochi", price = "$4.50", course = "Dessert", restaurant = restaurant4, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(user_id=1, name = "Cauliflower Manchurian", description = "Golden fried cauliflower florets in a midly spiced soya,garlic sauce cooked with fresh cilantro, celery, chilies,ginger & green onions", price = "$6.95", course = "Appetizer", restaurant = restaurant4, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem4)
session.commit()

menuItem5 = MenuItem(user_id=1, name = "Aloo Gobi Burrito", description = "Vegan goodness. Burrito filled with rice, garbanzo beans, curry sauce, potatoes (aloo), fried cauliflower (gobi) and chutney. Nom Nom", price = "$7.95", course = "Entree", restaurant = restaurant4, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem5)
session.commit()

menuItem6 = MenuItem(user_id=1, name = "Veggie Burger", description = "Juicy grilled veggie patty with tomato mayo and lettuce", price = "$6.80", course = "Entree", restaurant = restaurant4, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem6)
session.commit()


#Menu for Tony's Bistro
restaurant5 = Restaurant(user_id=1, name = "Tony\'s Bistro ", address="1600 Pennsylvania Ave NW,Washington, DC 20500, USA", phone="+123456789", website="google.com", cousine="French", img="http://100dorog.ru/upload/contents/680/HI68/HI68146707.jpg")
session.add(restaurant5)
session.commit()

menuItem1 = MenuItem(user_id=1, name = "Shellfish Tower", description = "Lobster, shrimp, sea snails, crawfish, stacked into a delicious tower", price = "$13.95", course = "Entree", restaurant = restaurant5, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(user_id=1, name = "Chicken and Rice", description = "Chicken... and rice", price = "$4.95", course = "Entree", restaurant = restaurant5, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(user_id=1, name = "Mom's Spaghetti", description = "Spaghetti with some incredible tomato sauce made by mom", price = "$6.95", course = "Entree", restaurant = restaurant5, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(user_id=1, name = "Choc Full O\' Mint (Smitten\'s Fresh Mint Chip ice cream)", description = "Milk, cream, salt, ..., Liquid nitrogen magic", price = "$3.95", course = "Dessert", restaurant = restaurant5, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem4)
session.commit()

menuItem5 = MenuItem(user_id=1, name = "Tonkatsu Ramen", description = "Noodles in a delicious pork-based broth with a soft-boiled egg", price = "$7.95", course = "Entree", restaurant = restaurant5, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem5)
session.commit()


#Menu for Andala's
restaurant6 = Restaurant(user_id=1, name = "Andala\'s", address="1600 Pennsylvania Ave NW,Washington, DC 20500, USA", phone="+123456789", website="google.com", cousine="French", img="http://q-dc.bstatic.com/images/hotel/max300/148/14872422.jpg")
session.add(restaurant6)
session.commit()

menuItem1 = MenuItem(user_id=1, name = "Lamb Curry", description = "Slow cook that thang in a pool of tomatoes, onions and alllll those tasty Indian spices. Mmmm.", price = "$9.95", course = "Entree", restaurant = restaurant6, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(user_id=1, name = "Chicken Marsala", description = "Chicken cooked in Marsala wine sauce with mushrooms", price = "$7.95", course = "Entree", restaurant = restaurant6, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(user_id=1, name = "Potstickers", description = "Delicious chicken and veggies encapsulated in fried dough.", price = "$6.50", course = "Appetizer", restaurant = restaurant6, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(user_id=1, name = "Nigiri Sampler", description = "Maguro, Sake, Hamachi, Unagi, Uni, TORO!", price = "$6.75", course = "Appetizer", restaurant = restaurant6, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem4)
session.commit()

menuItem5 = MenuItem(user_id=1, name = "Veggie Burger", description = "Juicy grilled veggie patty with tomato mayo and lettuce", price = "$7.00", course = "Entree", restaurant = restaurant6, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem5)
session.commit()


#Menu for Auntie Ann's
restaurant7 = Restaurant(user_id=1, name = "Auntie Ann\'s Diner' ", address="1600 Pennsylvania Ave NW,Washington, DC 20500, USA", phone="+123456789", website="google.com", cousine="French", img="http://cs627628.vk.me/v627628409/b46c/uuOOnp_ktZ0.jpg")
session.add(restaurant7)
session.commit()

menuItem1 = MenuItem(user_id=1, name = "Boysenberry Sorbet", description = "An unsettlingly huge amount of ripe berries turned into frozen (and seedless) awesomeness", price = "$2.99", course = "Dessert", restaurant = restaurant7, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(user_id=1, name = "Broiled salmon", description = "Salmon fillet marinated with fresh herbs and broiled hot & fast", price = "$10.95", course = "Entree", restaurant = restaurant7, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(user_id=1, name = "Morels on toast (seasonal)", description = "Wild morel mushrooms fried in butter, served on herbed toast slices", price = "$7.50", course = "Appetizer", restaurant = restaurant7, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(user_id=1, name = "Tandoori Chicken", description = "Chicken marinated in yoghurt and seasoned with a spicy mix(chilli, tamarind among others) and slow cooked in a cylindrical clay or metal oven which gets its heat from burning charcoal.", price = "$8.95", course = "Entree", restaurant = restaurant7, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem4)
session.commit()

menuItem5 = MenuItem(user_id=1, name = "Veggie Burger", description = "Juicy grilled veggie patty with tomato mayo and lettuce", price = "$9.50", course = "Entree", restaurant = restaurant7, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem5)
session.commit()

menuItem6 = MenuItem(user_id=1, name = "Chicken Fried Steak", description = "Fresh battered sirloin steak fried and smothered with cream gravy", price = "$8.99", course = "Entree", restaurant = restaurant7, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem6)
session.commit()

menuItem7 = MenuItem(user_id=1, name = "Spinach Ice Cream", description = "vanilla ice cream made with organic spinach leaves", price = "$1.99", course = "Dessert", restaurant = restaurant7, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem7)
session.commit()


#Menu for Cocina Y Amor
restaurant8 = Restaurant(user_id=1, name = "Cocina Y Amor ", address="1600 Pennsylvania Ave NW,Washington, DC 20500, USA", phone="+123456789", website="google.com", cousine="French", img="http://r-ec.bstatic.com/images/hotel/max300/360/36062598.jpg")
session.add(restaurant8)
session.commit()

menuItem1 = MenuItem(user_id=1, name = "Super Burrito Al Pastor", description = "Marinated Pork, Rice, Beans, Avocado, Cilantro, Salsa, Tortilla", price = "$5.95", course = "Entree", restaurant = restaurant8, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(user_id=1, name = "Cachapa", description = "Golden brown, corn-based Venezuelan pancake; usually stuffed with queso telita or queso de mano, and possibly lechon. ", price = "$7.99", course = "Entree", restaurant = restaurant8, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem2)
session.commit()


#Menu for State Bird Provisions
restaurant9 = Restaurant(user_id=1, name = "State Bird Provisions", address="1600 Pennsylvania Ave NW,Washington, DC 20500, USA", phone="+123456789", website="google.com", cousine="French", img="http://cs605826.vk.me/v605826336/2b73/zS_FcMnRWDA.jpg")
session.add(restaurant9)
session.commit()

menuItem1 = MenuItem(user_id=1, name = "Chantrelle Toast", description = "Crispy Toast with Sesame Seeds slathered with buttery chantrelle mushrooms", price = "$5.95", course = "Appetizer", restaurant = restaurant9, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem1)
session.commit

menuItem2 = MenuItem(user_id=1, name = "Guanciale Chawanmushi", description = "Japanese egg custard served hot with spicey Italian Pork Jowl (guanciale)", price = "$6.95", course = "Dessert", restaurant = restaurant9, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(user_id=1, name = "Lemon Curd Ice Cream Sandwich", description = "Lemon Curd Ice Cream Sandwich on a chocolate macaron with cardamom meringue and cashews", price = "$4.25", course = "Dessert", restaurant = restaurant9, img="http://cs410422.vk.me/v410422551/6f70/MPbIcchYB9U.jpg")
session.add(menuItem3)
session.commit()

print "added menu items!"