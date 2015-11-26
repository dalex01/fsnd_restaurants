from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

engine = create_engine('sqlite:///restaurantmenu.db')
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



class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Restaurants!</h1>"
                restaurants = session.query(Restaurant).all()
                for restaurant in restaurants:
                    output += "<div>" + str(restaurant.name) + "</div>"
                    output += "<div><a href=\"restaurant/" + str(restaurant.id) + "/edit\">Edit</a></div>"
                    output += "<div><a href=\"restaurant/" + str(restaurant.id) + "/delete\">Delete</a></div>"
                    output += "<br>"
                output += "<div><a href=\"/restaurants/new\">Create new restaurant</a></div>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/edit"):
                output = ""
                output += "<html><body>"
                output += "<h1>Edit!</h1>"
                output += "<a href=\"/restaurants\">Back to restaurants</h1>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/delete"):
                output = ""
                output += "<html><body>"
                output += "<h1>Delete!</h1>"
                output += "<a href=\"/restaurants\">Back to restaurants</h1>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/new"):
                output = ""
                output += "<html><body>"
                output += "<h1>New restaurant</h1>"
                output += "<a href=\"/restaurants\">Back to restaurants</h1>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
        	pass
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()

