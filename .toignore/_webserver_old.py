from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
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
                    output += "<div><a href=\"restaurants/" + str(restaurant.id) + "/edit\">Edit</a></div>"
                    output += "<div><a href=\"restaurants/" + str(restaurant.id) + "/delete\">Delete</a></div>"
                    output += "<br>"
                output += "<div><a href=\"/restaurants/new\">Create new restaurant</a></div>"
                output += "</body></html>"
                self.wfile.write(output)
                return
            if self.path.endswith("/edit"):
                restaurant_id = self.path.split('/')[2]
                restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
                if restaurant != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Edit restaurant</h1>"
                    output += "<h2>Enter new name of restaurant</h2>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurant_id
                    output += "<input name='newName' type='text' placeholder='%s'>" % restaurant.name
                    output += "<input type='submit' value='Rename'></form>"
                    output += "<a href=\"/restaurants\">Back to restaurants</h1>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    return
            if self.path.endswith("/delete"):
                restaurant_id = self.path.split('/')[2]
                restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
                if restaurant != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Delete restaurant</h1>"
                    output += "<h2>Are you sure you want to delete restaurant %s?</h2>" % restaurant.name
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % restaurant_id
                    output += "<input type='submit' value='Delete'></form>"
                    output += "<a href=\"/restaurants\">Back to restaurants</h1>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    return
            if self.path.endswith("/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>New restaurant</h1>"
                output += "<h2>Enter name of new restaurant</h2>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                output += "<input name='newName' type='text' placeholder='New Restaurant Name'>"
                output += "<input type='submit' value='Save'></form>"
                output += "<a href=\"/restaurants\">Back to restaurants</h1>"
                output += "</body></html>"
                self.wfile.write(output)
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                namecontent = fields.get('newName')

                restaurant_id = self.path.split('/')[2]
                restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
                if restaurant != []:
                    restaurant.name = namecontent[0]
                    session.add(restaurant)
                    session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))

                restaurant_id = self.path.split('/')[2]
                restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
                if restaurant != []:
                    session.delete(restaurant)
                    session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
            if self.path.endswith("/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                namecontent = fields.get('newName')

                res = Restaurant(name = namecontent[0])
                session.add(res)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
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

