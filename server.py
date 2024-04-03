# import sys; # used to get argv
# import cgi; # used to parse Mutlipart FormData       
# import os;
# import glob;
# import Physics;

# import math;

# # web server parts
# from http.server import HTTPServer, BaseHTTPRequestHandler;

# # used to parse the URL and extract form data for GET requests
# from urllib.parse import urlparse, parse_qsl;


# # handler for our web-server - handles both GET and POST requests
# class MyHandler( BaseHTTPRequestHandler ):
#     def do_GET(self):
#         # parse the URL to get the path and form data
#         parsed  = urlparse( self.path );

#         # check if the web-pages matches the list
#         if parsed.path in [ '/shoot.html' ]:

#             # retreive the HTML file
#             fp = open( '.'+self.path );
#             content = fp.read();

#             # generate the headers
#             self.send_response( 200 ); # OK
#             self.send_header( "Content-type", "text/html" );
#             self.send_header( "Content-length", len( content ) );
#             self.end_headers();

#             # send it to the broswer
#             self.wfile.write( bytes( content, "utf-8" ) );
#             fp.close();

#         elif parsed.path.endswith('.svg') and parsed.path.startswith('/table-'):
#             # Dynamically handle SVG files without hardcoding the file name
#             try:
#                 with open('.' + parsed.path, 'rb') as fp:  # Open the file in binary mode
#                     content = fp.read()
#                 self.send_response(200)
#                 self.send_header("Content-type", "image/svg+xml")  # Set the correct content type for SVG files
#                 self.send_header("Content-length", len(content))
#                 self.end_headers()
#                 self.wfile.write(content)
#             except IOError:
#                 # File not found, return 404
#                 self.send_response(404)
#                 self.end_headers()
#                 self.wfile.write(bytes("404: File not found %s" % parsed.path, "utf-8"))


#         # check if the web-pages matches the list

#         else:
#             # generate 404 for GET requests that aren't the 2 files above
#             self.send_response( 404 );
#             self.end_headers();
#             self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );


#     def do_POST(self):
#         # hanle post request
#         # parse the URL to get the path and form data
#         parsed  = urlparse( self.path );

#         if parsed.path in [ '/display.html' ]:

#             # get data send as Multipart FormData (MIME format)
#             form = cgi.FieldStorage( fp=self.rfile,
#                                      headers=self.headers,
#                                      environ = { 'REQUEST_METHOD': 'POST',
#                                                  'CONTENT_TYPE': 
#                                                    self.headers['Content-Type'],
#                                                } 
#                                    );
#              # Step 2: Delete all table-?.svg files
#             for svg_file in glob.glob('table-*.svg'):
#                 os.remove(svg_file)

#             v_relx = float(form['rb_dx'].value)
#             v_rely = float(form['rb_dy'].value) 

#             v_rel = Physics.Coordinate(v_relx,v_rely)

#             speed_a = math.sqrt((float(form['rb_dx'].value) * float(form['rb_dx'].value)) + (float(form['rb_dy'].value) * float(form['rb_dy'].value)))

#             #Check if the speed is greater than PHYLIB_VEL_EPSILON for a
#             if(speed_a > Physics.VEL_EPSILON):
#                 accelax = -(v_rel.x / speed_a) * Physics.DRAG
#                 accelay = -(v_rel.y / speed_a) * Physics.DRAG
#                 accela = Physics.Coordinate(accelax,accelay)
                
#             #Step 4 - Construct the table
                 
#             file_index = 0
            
#             table = Physics.Table()    

#             #3 -- Calculate the position for the StillBall
#             numStillBall = int(form['sb_number'].value); 
#             pos_x = float(form['sb_x'].value)
#             pos_y = float(form['sb_y'].value)
#             pos = Physics.Coordinate(pos_x, pos_y)

#             # 4. Create and store the StillBall
#             sb = Physics.StillBall(numStillBall, pos)

#             # 5. Calculate position, velocity, and acceleration for RollingBall
#             pos_rbx = float(form['rb_x'].value)
#             pos_rby = float(form['rb_y'].value)
#             pos_rb = Physics.Coordinate(pos_rbx,pos_rby)
#             velx = float(form['rb_dx'].value)
#             vely = float(form['rb_dy'].value)
#             vel = Physics.Coordinate(velx,vely)
            
#             # 6. Create and store the RollingBall
#             numRollingBall = int(form['rb_number'].value); 
#             rb = Physics.RollingBall(numRollingBall, pos_rb, vel, accela)

#             # 7. Add the StillBall to the table
#             table += sb

#             # 8. Add the RollingBall to the table
#             table += rb

#             # Write the initial state of the table to an SVG file
#             write_svg(table, file_index)
#             file_index += 1

#             while table is not None:
#                 table = table.segment()
#                 #print(rb, sb, "\n\n\n\n")
#                 if table:
#                     write_svg(table, file_index)
#                     file_index += 1
#                 else:
#                     break
            
#                 # Inside do_POST, after generating SVG files
#             svg_files = glob.glob('table-*.svg')
#             # HTML content start
#             html_content = f"""
#             <html>
#             <head>
#                 <title>Ball Trajectories</title>
#             </head>
#             <body>
#                 <h1>Physics Simulation</h1>
#                 <p>StillBall Position: ({pos_x}, {pos_y})</p>
#                 <p>RollingBall Initial Position: ({pos_rbx}, {pos_rby}), Velocity: ({velx}, {vely}), Acceleration: ({accelax}, {accelay})</p>
#                 <h2>Simulation Results</h2>
#             """
#             # Dynamically adding img tags for each SVG file
#             for svg_file in svg_files:
#                 html_content += f'<img src="{svg_file}" alt="Simulation Step"/><br/>\n'
            
#             # Adding back link
#             html_content += '<a href="/shoot.html">Back</a>\n'
            
#             # HTML content end
#             html_content += """
#             </body>
#             </html>
#             """
            
#             # Sending the response
#             self.send_response(200)
#             self.send_header("Content-type", "text/html")
#             self.send_header("Content-length", len(html_content))
#             self.end_headers()
#             self.wfile.write(bytes(html_content, "utf-8"))


# def write_svg(table, index):
#     """
#     Writes the SVG representation of the table to a file named "table-<index>.svg"
#     """
#     filename = f"table-{index}.svg"
#     with open(filename, 'w') as file:
#         file.write(table.svg())
#     print(f"SVG written to {filename}")

# if __name__ == "__main__":
#     httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );
#     print( "Server listing in port:  ", int(sys.argv[1]) );
#     httpd.serve_forever();



import glob
import json
import re
import shutil
import sys
from Physics import Database, Game
from game_manager import initialize_table_with_balls, save_svg
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import cgi
import os

class MyHandler(BaseHTTPRequestHandler): 
    last_index = None
    var_lock = 0

    table = None

    if(var_lock == 0):
        table = initialize_table_with_balls()
        var_lock = 1
        
    
    def clear_svgs_directory(directory="svgs"):
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.makedirs(directory)

    def serve_static_file(self, path, content_type):
        try:
            with open(path, 'rb') as file:
                content = file.read()
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                self.wfile.write(content)
        except Exception as e:
            print(f"Error serving file {path}: {e}")
            self.send_error(500, "Internal Server Error")

    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path in ['/shoot.html', '/']:
            self.serve_static_file('shoot.html', 'text/html')
        elif parsed_path.path.endswith('.js'):
            self.serve_static_file(parsed_path.path.lstrip('/'), 'application/javascript')
        elif parsed_path.path.startswith('/getSVG/'):
            table_id = parsed_path.path.split('/')[-1]
            self.serve_svg(table_id)
        else:
            self.send_error(404, 'File Not Found')

    def do_POST(self):
        parsed_path = urlparse(self.path)

        gameName = "ExampleGame"
        player1Name = "Player1"
        player2Name = "Player2"
        # Initialize the Game instance
        game = Game(gameName=gameName, player1Name=player1Name, player2Name=player2Name)

            # Initialize the table with balls for shooting

        clear_svgs_directory()
        if parsed_path.path == '/initializeGame':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            form_data = json.loads(post_data.decode('utf-8'))
            
            player1_name = form_data['player1Name']
            player2_name = form_data['player2Name']

            # Initialize game and table, then save the SVG
            MyHandler.table = initialize_table_with_balls()
            table_id = Database().writeTable(MyHandler.table)
            svg_filename = f"table_{table_id}.svg"
            save_svg(MyHandler.table, os.path.join("svgs", svg_filename))  # Ensure correct path

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'tableId': table_id}
            self.wfile.write(json.dumps(response).encode('utf-8'))

        elif parsed_path.path == '/shoot':

            fcounter = -1
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            form_data = json.loads(post_data.decode('utf-8'))

            xvel = form_data['xvel']
            yvel = form_data['yvel']

            # Static values for game initialization
            gameName = "ExampleGame"
            player1Name = "Player1"
            player2Name = "Player2"

            

            # Perform the shooting action
            game.shoot(gameName=gameName, playerName=player1Name, table=MyHandler.table, xvel=xvel, yvel=yvel)
            
            svgsfpath = 'svgs'
            
            
            for path in os.listdir(svgsfpath):
            # check if current path is a file
                if os.path.isfile(os.path.join(svgsfpath, path)):
                    fcounter += 1
                    print(fcounter)


            

            # List all SVG filenames in the 'svgs' directory, sorted numerically
            svg_filenames = sorted(
                [os.path.basename(f) for f in glob.glob('svgs/table_*.svg')],
                key=lambda f: int(re.search(r'(\d+)', f).group())
            )
            last_svg_filename = svg_filenames[-1]
            
            # Respond with the list of SVG filenames
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'status': 'success',
                'message': 'Shot data received and processed',
                'svgFilenames': svg_filenames,  # Send the list of SVG filenames
                'lastSvgFilename': last_svg_filename,
                'lastIndex': fcounter  # Include the last SVG filename
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))

                        
    def serve_svg(self, table_id):
        svg_filename = f'svgs/table_{table_id}.svg'
        print("1:SVG file with path  is")
        print(svg_filename);
        try:
            with open(svg_filename, 'rb') as file:
                print("2:File to read is");
                print (file);
                svg_content = file.read()
                #print (svg_content);
                self.send_response(200)
                self.send_header('Content-type', 'image/svg+xml')
                self.end_headers()
                self.wfile.write(svg_content)
        except FileNotFoundError:
            self.send_error(404, 'SVG Not Found')
        except Exception as e:
            print(f"Failed to serve SVG for table ID {table_id}: {e}")
            self.send_error(500, 'Internal Server Error')



def clear_svgs_directory(directory="svgs"):
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server_address = ('', port)

    # Reset the database and initialize the table structure before starting the server
    db = Database(reset=True)  # Reset the database if needed
    db.createDB()  # Create the necessary tables

    httpd = HTTPServer(server_address, MyHandler)
    print(f"Server listening on port {port}")
    httpd.serve_forever()

