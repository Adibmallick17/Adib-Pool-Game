# import phylib;
# import Physics;
# import sqlite3;
# import os;
# import time
# import math

# FRAME_RATE = 0.01 

# # SVG constants
# HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
# <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
# "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
# <svg width="700" height="1375" viewBox="-25 -25 1400 2750"
# xmlns="http://www.w3.org/2000/svg"
# xmlns:xlink="http://www.w3.org/1999/xlink">
# <rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />\n"""

# FOOTER = """</svg>\n"""

# ################################################################################
# # import constants from phylib to global varaibles
# BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
# BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;
# HOLE_RADIUS =  phylib.PHYLIB_HOLE_RADIUS;
# TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH;
# TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH;
# SIM_RATE = phylib.PHYLIB_SIM_RATE;
# VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON;
# DRAG = phylib.PHYLIB_DRAG;
# MAX_TIME = phylib.PHYLIB_MAX_TIME;
# MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS;

# ################################################################################
# # the standard colours of pool balls
# # if you are curious check this out:  
# # https://billiards.colostate.edu/faq/ball/colors/

# BALL_COLOURS = [ 
#     "WHITE",
#     "YELLOW",
#     "BLUE",
#     "RED",
#     "PURPLE",
#     "ORANGE",
#     "GREEN",
#     "BROWN",
#     "BLACK",
#     "LIGHTYELLOW",
#     "LIGHTBLUE",
#     "PINK",             # no LIGHTRED
#     "MEDIUMPURPLE",     # no LIGHTPURPLE
#     "LIGHTSALMON",      # no LIGHTORANGE
#     "LIGHTGREEN",
#     "SANDYBROWN",       # no LIGHTBROWN 
#     ];

# ################################################################################
# class Coordinate(phylib.phylib_coord):
#     """
#     This creates a Coordinate subclass, that adds nothing new, but looks
#     more like a nice Python class.
#     """
#     pass;


# ################################################################################
# class StillBall(phylib.phylib_object):
#     """
#     Python StillBall class.
#     """

#     def __init__( self, number, pos ):
#         """
#         Constructor function. Requires ball number and position (x,y) as
#         arguments.
#         """
        
#         # this creates a generic phylib_object
#         phylib.phylib_object.__init__( self, 
#                                        phylib.PHYLIB_STILL_BALL, 
#                                        number, 
#                                        pos, None, None, 
#                                        0.0, 0.0 );
      
#         # this converts the phylib_object into a StillBall class
#         self.__class__ = StillBall;
        


#     def svg(self):
#         """
#         SVG representation of StillBall.
#         """
#         return f"""<circle cx="{self.obj.still_ball.pos.x}" cy="{self.obj.still_ball.pos.y}" r="{BALL_RADIUS}" fill="{BALL_COLOURS[self.obj.still_ball.number]}" />\n""" 


# class RollingBall(phylib.phylib_object):
#     """
#     Python RollingBall class.
#     """

#     def __init__(self, number, pos, vel, acc):
#         """
#         Constructor function. Requires ball number, position (x,y), and velocity (vx, vy) as arguments.
#         """

#         # Create a generic phylib_object
#         phylib.phylib_object.__init__(self,
#                                        phylib.PHYLIB_ROLLING_BALL,
#                                        number,
#                                        pos,
#                                        vel,
#                                        acc,
#                                        0.0,
#                                        0.0 )

#         # Convert the phylib_object into a RollingBall class
#         self.__class__ = RollingBall 

#     def svg(self):
#         """
#         SVG representation of RollingBall.
#         """
#         return f"""<circle cx="{self.obj.rolling_ball.pos.x}" cy="{self.obj.rolling_ball.pos.y}" r="{BALL_RADIUS}" fill="{BALL_COLOURS[self.obj.rolling_ball.number]}" />\n"""


# class Hole(phylib.phylib_object):
#     """
#     Python Hole class.
#     """

#     def __init__(self, pos):
#         """
#         Constructor function. Requires hole number and position (x, y) as arguments.
#         """

#         # Create a generic phylib_object
#         phylib.phylib_object.__init__(self,
#                                        phylib.PHYLIB_HOLE,
#                                        0,
#                                        pos,
#                                        None,
#                                        None,
#                                        0.0,
#                                        0.0)

#         # Convert the phylib_object into a Hole class
#         self.__class__ = Hole 

#     def svg(self):
#         """
#         SVG representation of Hole.
#         """
#         return f"""<circle cx="{self.obj.hole.pos.x}" cy="{self.obj.hole.pos.y}" r="{HOLE_RADIUS}" fill="black" />\n"""


# class HCushion(phylib.phylib_object):
#     """
#     Python HCushion class.
#     """

#     def __init__(self, y):
#         """
#         Constructor function. Requires cushion number and position (x, y) as arguments.
#         """
#         pos = phylib.phylib_coord(0, y)
#         # Create a generic phylib_object
#         phylib.phylib_object.__init__(self,
#                                        phylib.PHYLIB_HCUSHION,
#                                        0,
#                                        pos,
#                                        None,
#                                        None,
#                                        0.0,
#                                        y)

#         # Convert the phylib_object into a HCushion class
#         self.__class__ = HCushion

#     def svg(self):
#         """
#         SVG representation of HCushion.
#         """
#         y = -25 if self.obj.hcushion.y == 0 else 2700  # Determine if top or bottom cushion
#         return f"""<rect width="1400" height="25" x="-25" y="{y}" fill="darkgreen" />\n"""


# class VCushion(phylib.phylib_object):
#     """
#     Python VCushion class.
#     """

#     def __init__(self, x):
#         """
#         Constructor function. Requires cushion number and position (x, y) as arguments.
#         """
#         pos = phylib.phylib_coord(x, 0)
#         # Create a generic phylib_object
#         phylib.phylib_object.__init__(self,
#                                        phylib.PHYLIB_VCUSHION,
#                                        0,
#                                        pos,
#                                        None,
#                                        None,
#                                        x,
#                                        0.0)

#         # Convert the phylib_object into a VCushion class
#         self.__class__ = VCushion

#     def svg(self):
#         """
#         SVG representation of VCushion.
#         """
#         x = -25 if self.obj.vcushion.x == 0 else 1350  # Determine if left or right cushion
#         return f"""<rect width="25" height="2750" x="{x}" y="-25" fill="darkgreen" />\n"""

#     # add an svg method here


# ################################################################################

# class Table( phylib.phylib_table ):
#     """
#     Pool table class.
#     """

#     def __init__( self ):
#         """
#         Table constructor method.
#         This method call the phylib_table constructor and sets the current
#         object index to -1.
#         """
#         phylib.phylib_table.__init__( self )
#         self.current = -1

#     def __iadd__( self, other ):
#         """
#         += operator overloading method.
#         This method allows you to write "table+=object" to add another object
#         to the table.
#         """
#         self.add_object( other )
#         return self

#     def __iter__( self ):
#         """
#         This method adds iterator support for the table.
#         This allows you to write "for object in table:" to loop over all
#         the objects in the table.
#         """
#         return self

#     def __next__( self ):
#         """
#         This provides the next object from the table in a loop.
#         """
#         self.current += 1;  # increment the index to the next object
#         if self.current < MAX_OBJECTS:   # check if there are no more objects
#             return self[ self.current ]; # return the latest object

#         # if we get there then we have gone through all the objects
#         self.current = -1;    # reset the index counter
#         raise StopIteration;  # raise StopIteration to tell for loop to stop

#     def __getitem__( self, index ):
#         """
#         This method adds item retreivel support using square brackets [ ] .
#         It calls get_object (see phylib.i) to retreive a generic phylib_object
#         and then sets the __class__ attribute to make the class match
#         the object type.
#         """
#         result = self.get_object( index ); 
#         if result==None:
#             return None
#         if result.type == phylib.PHYLIB_STILL_BALL:
#             result.__class__ = StillBall
#         if result.type == phylib.PHYLIB_ROLLING_BALL:
#             result.__class__ = RollingBall
#         if result.type == phylib.PHYLIB_HOLE:
#             result.__class__ = Hole
#         if result.type == phylib.PHYLIB_HCUSHION:
#             result.__class__ = HCushion
#         if result.type == phylib.PHYLIB_VCUSHION:
#             result.__class__ = VCushion
#         return result

#     def __str__( self ):
#         """
#         Returns a string representation of the table that matches
#         the phylib_print_table function from A1Test1.c.
#         """
#         result = "";    # create empty string
#         result += "time = %6.1f;\n" % self.time;    # append time
#         for i,obj in enumerate(self): # loop over all objects and number them
#             result += "  [%02d] = %s\n" % (i,obj);  # append object description
#         return result;  # return the string

#     def segment( self ):
#         """
#         Calls the segment method from phylib.i (which calls the phylib_segment
#         functions in phylib.c.
#         Sets the __class__ of the returned phylib_table object to Table
#         to make it a Table object.
#         """

#         result = phylib.phylib_table.segment( self )
#         if result:
#             result.__class__ = Table
#             result.current = -1
#         return result

#     def svg(self):
#         """
#         Method to generate SVG representation of the table.
#         """
#         svg_str = HEADER
#         for obj in self:
#            if obj is not None:
#             svg_str += obj.svg()
#         svg_str += FOOTER
#         return svg_str

#     def roll( self, t ):
#             new = Table();
#             for ball in self:
#                 if isinstance( ball, RollingBall ):
#                     # create4 a new ball with the same number as the old ball
#                     new_ball = RollingBall( ball.obj.rolling_ball.number,
#                                             Coordinate(0,0),
#                                             Coordinate(0,0),
#                                             Coordinate(0,0) );
#                     # compute where it rolls to
#                     phylib.phylib_roll( new_ball, ball, t );

#                     # add ball to table
#                     new += new_ball;

#                 if isinstance( ball, StillBall ):
#                     # create a new ball with the same number and pos as the old ball
#                     new_ball = StillBall(   ball.obj.still_ball.number,
#                                             Coordinate( ball.obj.still_ball.pos.x,
#                                                         ball.obj.still_ball.pos.y ) );
#                     # add ball to table
#                     new += new_ball;
#             # return table
#             return new;

#     def cueBall(self, table, xvel, yvel):

#         for ball in table:
#             if isinstance(ball, StillBall) and ball.obj.still_ball.number == 0:
#                 xpos = ball.obj.still_ball.pos.x
#                 ypos = ball.obj.still_ball.pos.y
#                 ball.type = phylib.PHYLIB_ROLLING_BALL
#                 cue_ball = ball.obj.rolling_ball
#                 cue_ball.number = 0

#         cue_ball.pos.y = ypos
#         cue_ball.pos.x = xpos
#         cue_ball.vel.y = yvel
#         cue_ball.vel.x = xvel
        

#         speed_ball = math.sqrt((xvel * xvel) + (yvel * yvel))
#         acc_x = 0
#         acc_y = 0

#         if speed_ball >= VEL_EPSILON:
#             acc_x = -(xvel / speed_ball) * DRAG
#             acc_y = -(yvel / speed_ball) * DRAG

#             if acc_x == -0.0:
#                 acc_x *= -1.0
#             if acc_y == -0.0:
#                 acc_y *= -1.0

#         acc = Coordinate(acc_x, acc_y)
#         cue_ball.acc.x = acc.x
#         cue_ball.acc.y = acc.y


# class Database():
#     def __init__(self, reset=False):
#         if reset:
#             self._reset_database()
#         self.conn = sqlite3.connect("phylib.db")
#         cursor = self.conn.cursor()
    
#     def _reset_database(self):
#         db_file = "phylib.db"
#         try:
#             if os.path.exists(db_file):
#                 os.remove(db_file)
#         except Exception as e:
#             print("Error resetting database:", e)
    
#     def createDB(self):
#         try:
#             conn = self.conn
#             cursor = self.conn.cursor()
#              # Create Ball table
#             cursor.execute('''CREATE TABLE IF NOT EXISTS Ball (
#                             BALLID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#                             BALLNO INTEGER NOT NULL,
#                             XPOS FLOAT NOT NULL,
#                             YPOS FLOAT NOT NULL,
#                             XVEL FLOAT,
#                             YVEL FLOAT
#                             )''')

#             # Create TTable table
#             cursor.execute('''CREATE TABLE IF NOT EXISTS TTable (
#                             TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#                             TIME FLOAT NOT NULL
#                             )''')

#             # Create BallTable table
#             cursor.execute('''CREATE TABLE IF NOT EXISTS BallTable (
#                             BALLID INTEGER NOT NULL,
#                             TABLEID INTEGER NOT NULL,
#                             PRIMARY KEY (BALLID, TABLEID),
#                             FOREIGN KEY (BALLID) REFERENCES Ball (BALLID),
#                             FOREIGN KEY (TABLEID) REFERENCES TTable (TABLEID)
#                             )''')

#             # Create Shot table
#             cursor.execute('''CREATE TABLE IF NOT EXISTS Shot (
#                             SHOTID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#                             PLAYERID INTEGER NOT NULL,
#                             GAMEID INTEGER NOT NULL,
#                             FOREIGN KEY (PLAYERID) REFERENCES Player (PLAYERID),
#                             FOREIGN KEY (GAMEID) REFERENCES Game (GAMEID)
#                             )''')

#             # Create TableShot table
#             cursor.execute('''CREATE TABLE IF NOT EXISTS TableShot (
#                             TABLEID INTEGER NOT NULL,
#                             SHOTID INTEGER NOT NULL,
#                             PRIMARY KEY (TABLEID, SHOTID),
#                             FOREIGN KEY (TABLEID) REFERENCES TTable (TABLEID),
#                             FOREIGN KEY (SHOTID) REFERENCES Shot (SHOTID)
#                             )''')

#             # Create Game table
#             cursor.execute('''CREATE TABLE IF NOT EXISTS Game (
#                             GAMEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#                             GAMENAME VARCHAR(64) NOT NULL
#                             )''')

#             # Create Player table
#             cursor.execute('''CREATE TABLE IF NOT EXISTS Player (
#                             PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#                             GAMEID INTEGER NOT NULL,
#                             PLAYERNAME VARCHAR(64) NOT NULL,
#                             FOREIGN KEY (GAMEID) REFERENCES Game (GAMEID)
#                             )''')

#         except Exception as e:
#             print("Error creating database:", e)
#         finally:
#             # Commit changes and close cursor
#             self.conn.commit()
#             cursor.close()    

#     def readTable(self, tableID):
#         try:
#             cursor = self.conn.cursor()
#             cursor.execute('''SELECT Ball.*
#                              FROM Ball 
#                              JOIN BallTable ON Ball.BALLID = BallTable.BALLID
#                              WHERE BallTable.TABLEID = ?''', (tableID + 1,))

#             rows = cursor.fetchall()

#             if not rows:
#                 return None
#             table = Table()

#             for row in rows:
#                 ballID, ballNo, x, y, xVel, yVel = row
#                 position = Coordinate(x,y)
#                 if xVel == 0 and yVel == 0:
#                     ball = StillBall(ballNo,position)
#                 else:
#                     ball_velocity = Coordinate(xVel,yVel)
#                     ball_speed = phylib.phylib_length(ball_velocity)
#                     ball_acceleration = Coordinate(ball_velocity.x * -1.0/ball_speed * phylib.PHYLIB_DRAG, ball_velocity.y * -1.0/ball_speed* phylib.PHYLIB_DRAG)
#                     ball = RollingBall(ballNo, position, ball_velocity, ball_acceleration)
#                 table+=ball

#             return table
#         except Exception as e:
#             print("Error reading table from database:", e)
#             return None
#         finally:
#             # Commit changes and close cursor
#             self.conn.commit()
#             cursor.close()    
    
#     def writeTable(self, table):
#         try:
#             cursor = self.conn.cursor()
#             # Insert balls into Ball table
#             for ball in table:
#                 if isinstance(ball, StillBall):
#                     cursor.execute('''INSERT INTO Ball (BALLNO, XPOS, YPOS,XVEL,YVEL)
#                                       VALUES (?, ?, ?,0,0)''', (ball.obj.still_ball.number, ball.obj.still_ball.pos.x, ball.obj.still_ball.pos.y))
#                 elif isinstance(ball, RollingBall):
#                     cursor.execute('''INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL)
#                                       VALUES (?, ?, ?, ?, ?)''', (ball.obj.rolling_ball.number, ball.obj.rolling_ball.pos.x, ball.obj.rolling_ball.pos.y, ball.obj.rolling_ball.vel.x, ball.obj.rolling_ball.vel.y))
#             ballID = cursor.lastrowid

#             # Retrieve auto-incremented TABLEID value
#             cursor.execute('''INSERT INTO TTable (TIME) VALUES (?)''', (table.time,))
#             tableID = cursor.lastrowid - 1


#             cursor.execute("SELECT * FROM BallTable WHERE BALLID = ?;", (ballID,))
#             flash = cursor.fetchone()

#             # Insert entries into BallTable table
#             if flash is None:
#                 cursor.execute('''INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)''', (ballID, tableID + 1 ))

#             return tableID

#         except Exception as e:
#             print("Error writing table to database:", e)
#             return None

#         finally:
#             self.conn.commit()    
#             cursor.close()    

#     def close(self):
#         try:
#             self.conn.commit()  
#         except Exception as e:
#             print("Error committing changes to the database:", e)
#         finally:
#             try:
#                 self.conn.close() 
#             except Exception as e:
#                 print("Error closing the database connection:", e)

#     def gameID(self, gameName):
#         # Retrieve gameID from the database using the provided gameName
#         with self.conn.cursor() as cursor:
#             cursor.execute("SELECT GAMEID FROM Game WHERE GAMENAME = ?", (gameName,))
#             row = cursor.fetchone()
#             gameID = row[0] if row else None
#         return gameID

#     # Helper method 
#     def setGame(self, gameName, player1Name, player2Name):
#         cursor = self.conn.cursor()
#         cursor.execute("""INSERT INTO Game (GAMENAME) VALUES (?)""", (gameName,))
#         gameID = cursor.lastrowid
#         cursor.execute("""INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?) """, (gameName, player1Name))
#         player1ID = cursor.lastrowid
#         cursor.execute("""INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?) """, (gameName, player2Name))
#         player2ID = cursor.lastrowid
#         self.conn.commit()
#         cursor.close()
#         return gameID

#     #Helper method 
#     def playerID(self, playerName):
#         # Retrieve playerID from the database using the provided playerName
#         with self.conn.cursor() as cursor:
#             cursor.execute(""" SELECT PLAYERID FROM Player WHERE PLAYERNAME = ? """, (playerName,))
#             row = cursor.fetchone()
#             if row:
#                 playerID = row[0]
#             else:
#                 playerID = None
#         self.conn.commit()
#         cursor.close()    
#         return playerID


#     #Helper method
#     def newShot(self, gameName, playerName):
#         cursor = self.conn.cursor()
#         cursor.execute("""SELECT GAMEID FROM Game WHERE GAMENAME = ? """, (gameName,))
#         gameID = cursor.fetchone()[0]
#         cursor.execute("""SELECT PLAYERID FROM Player WHERE PLAYERNAME = ? """, (playerName,))
#         playerID = cursor.fetchone()[0]
#         cursor.execute("""INSERT INTO Shot (PLAYERID, GAMEID) VALUES (?, ?) """, (playerID, gameID,))
#         shotID = cursor.lastrowid
#         self.conn.commit()
#         cursor.close()
#         return shotID 

#     def tableShot(self, tableID, playerID):    
#         cursor = self.conn.cursor()
#         cursor.execute("""INSERT INTO TableShot (TABLEID, SHOTID) VALUES (?, ?) """, (tableID, playerID))
#         self.conn.commit()
#         cursor.close()


#     def getGame(self, gameID):
#         cursor = self.conn.cursor()
#         cursor.execute(""" SELECT Game.GAMENAME, Player1.PLAYERNAME, Player2.PLAYERNAME FROM Game 
#                            JOIN Player AS Player1 ON Game.PLAYERID = Player1.PLAYERID 
#                            JOIN Player AS Player2 ON Game.PLAYERID = Player2.PLAYERID 
#                            WHERE Game.GAMEID = ? 
#                            """, (gameID,))
#         gameData = cursor.fetchone()
#         self.conn.commit()
#         cursor.close()

#         return gameData        

# class Game():

#     def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):

#         """
#         Initiates a Game object with the given attributes.
#         """
#         self.db = Database(reset=True)
#         self.db.createDB()

#         # Check constructor arguments if game ID is not None
#         if gameID is not None and all(arg is None for arg in [gameName, player1Name, player2Name]):
#             new_gameID = gameID + 1 #Adding 1 for SQL indexing 
#             game_data = self.db.getGame(new_gameID)
#             if game_data:
#                 self.gameID, self.gameName, self.player1Name, self.player2Name = game_data
#             else:
#                 raise ValueError(f"Game with ID {gameID} does not exist")    

#         # gameID is None and names are given
#         elif gameID is None and all(arg is not None for arg in [gameName, player1Name, player2Name]):
#             self.gameID = self.db.setGame(gameName, player1Name, player2Name)
#             self.gameName = gameName
#             self.player1Name = player1Name
#             self.player2Name = player2Name
#         else:
#             raise TypeError("Invalid combination of arguments provided to constructor") 


#     def shoot(self, gameName, playerName, table, xvel, yvel):

#         cursor = self.db.conn.cursor()
#         db = Database()
#         shotID = self.db.newShot(gameName, playerName)
#         table = table
#         table.cueBall(table, xvel, yvel)
    
#         while table:
#             copy_table = table.segment()
#             if copy_table is None:
#                 break
        
#             time_start = table.time
#             time_end = copy_table.time
#             segment_length = time_end - time_start
#             framesNum = math.floor(segment_length / FRAME_RATE)
        
#             for i in range(framesNum):
#                 newTable = table.roll(i * FRAME_RATE)
#                 newTable.time = (table.time + i * FRAME_RATE)
#                 tableID = self.db.writeTable(newTable)
#                 self.db.tableShot(tableID, shotID)
        
#             table = copy_table
  
#         cursor.close()
#         db.close()

#         return shotID 


import math
import phylib;
import sqlite3;
import os;

import Physics

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH;
SIM_RATE = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON;
DRAG = phylib.PHYLIB_DRAG
MAX_TIME = phylib.PHYLIB_MAX_TIME;
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS;
STILL_BALL = phylib.PHYLIB_STILL_BALL;
ROLLING_BALL = phylib.PHYLIB_ROLLING_BALL;
HOLE = phylib.PHYLIB_HOLE;
HCUSHION = phylib.PHYLIB_HCUSHION;
VCUSHION = phylib.PHYLIB_VCUSHION;
FRAME_RATE = phylib.PHYLIB_SIM_RATE;

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />"""
FOOTER = """</svg>\n"""

# add more here DONE

################################################################################
# the standard colours of pool balls
# if you are curious check this out:
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN
    ];




################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object):
    """
    Python StillBall class.
    """
    def __init__(self, number, pos):
        super().__init__(phylib.PHYLIB_STILL_BALL, number, pos, None, None, 0.0, 0.0)
        self.number = number  # Explicitly set the number attribute
        self.pos = pos
        self.__class__ = StillBall


    # add an svg method here
    def svg(self):
        # Ensure ball number is within the range of BALL_COLOURS
        #color_index = self.obj.still_ball.number % len(BALL_COLOURS)
        svgString = """<circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (
            self.obj.still_ball.pos.x,
            self.obj.still_ball.pos.y,
            BALL_RADIUS,
            BALL_COLOURS[self.obj.still_ball.number]
        )
        return svgString



################################################################################

class RollingBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos, vel, acc ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self,
                                       phylib.PHYLIB_ROLLING_BALL,
                                       number,
                                       pos, vel, acc,
                                       0.0, 0.0 );

        # this converts the phylib_object into a StillBall class
        self.__class__ = RollingBall;


    # add an svg method here
    def svg(self):
        # Ensure ball number is within the range of BALL_COLOURS
        #color_index = self.obj.rolling_ball.number % len(BALL_COLOURS)
        svgString = """<circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (
            self.obj.rolling_ball.pos.x,
            self.obj.rolling_ball.pos.y,
            BALL_RADIUS,
            BALL_COLOURS[self.obj.rolling_ball.number]
        )
        return svgString

################################################################################

class Hole( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self,
                                       phylib.PHYLIB_HOLE,
                                       0,
                                       pos, None, None,
                                       0.0, 0.0);

        # this converts the phylib_object into a StillBall class
        self.__class__ = Hole;


    # add an svg method here
    def svg(self):
        svgString=""" <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS)
        return svgString

################################################################################

class HCushion( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, y ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self,
                                       phylib.PHYLIB_HCUSHION,
                                       0,
                                       None, None, None,
                                       None, y );

        # this converts the phylib_object into a StillBall class
        self.__class__ = HCushion;


    # add an svg method here
    def svg(self):
        if self.obj.hcushion.y == 0:
            y = -25
        else:
            y=2700
        return '<rect width = "1400" height = "25" x ="-25" y ="%d" fill="darkgreen" />\n'%(y)


################################################################################

class VCushion( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, x ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self,
                                       phylib.PHYLIB_VCUSHION,
                                       0,
                                       None, None, None,
                                       x, None);

        # this converts the phylib_object into a StillBall class
        self.__class__ = VCushion;


    # add an svg method here
    def svg(self):
        if self.obj.vcushion.x == 0.0:
            x = -25
        else:
            x = 1350
        return '<rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n'%(x)


################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def to_json(self):
        objects = []
        for obj in self:
            if isinstance(obj, (StillBall, RollingBall, Hole, HCushion, VCushion)):
                objects.append(obj.to_json())
        return objects

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index );
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment(self):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c. Sets the __class__ of the returned phylib_table object
        to Table to make it a Table object.
        """
        #print("[Segment] Calling phylib_segment...")

        result = phylib.phylib_table.segment(self)

        if result:
            #print("[Segment] New table state generated.")
            result.__class__ = Table
            result.current = -1
        else:
            print("[Segment] No new table state generated.")

        #print("[Segment] Segmentation complete.")
        return result

    def svg(self):
        """
        Returns SVG rep of table
        """
        svgString = HEADER
    # add svg method here
        for obj in self:
            if obj is not None:
                svgString += obj.svg()
        svgString += FOOTER
        return svgString

    def roll(self, t):
        new = Table()  # Create a new Table instance
        for ball in self:  # Iterate over all balls in the current table
            if isinstance(ball, RollingBall):
                # Create a new RollingBall with the same number as the old ball
                new_ball = RollingBall(ball.obj.rolling_ball.number,
                                    Coordinate(0, 0),
                                    Coordinate(0, 0),
                                    Coordinate(0, 0))
                # Compute where it rolls to
                phylib.phylib_roll(new_ball, ball, t)
                # Add the new RollingBall to the new table
                new += new_ball
            elif isinstance(ball, StillBall):  # This line should be part of the loop
                # Create a new StillBall with the same number and position as the old ball
                new_ball = StillBall(ball.obj.still_ball.number,
                                    Coordinate(ball.obj.still_ball.pos.x,
                                                ball.obj.still_ball.pos.y))
                # Add the new StillBall to the new table
                new += new_ball

        return new  # Return the new table with updated balls

    def findCueBall(self):
        """Find and return the cue ball from the table."""
        for obj in self:
            if isinstance(obj, StillBall) and obj.obj.still_ball.number == 0:
                return obj
            elif isinstance(obj, RollingBall) and obj.obj.rolling_ball.number == 0:
                return obj
        return None

    def findCueBall(self):
        """Find and return the cue ball from the table."""
        for obj in self:
            print(f"[findCueBall] Checking object: {obj}")
            if (isinstance(obj, StillBall) and obj.obj.still_ball.number == 0) or (isinstance(obj, RollingBall) and obj.obj.rolling_ball.number == 0):
                return obj
        return None

    def to_json(self):
        """Convert the table and its objects to a JSON-friendly format."""
        # Initialize the JSON structure
        table_data = {
            "cueBall": None,
            "balls": [],
            "holes": [],
            "hcushions": [],
            "vcushions": []
        }

        # Iterate over objects in the table
        for obj in self:
            if isinstance(obj, StillBall) or isinstance(obj, RollingBall):
                # Special handling for the cue ball (ball number 0)
                if obj.obj.still_ball.number or obj.obj.rolling_ball.number == 0:
                    table_data["cueBall"] = {
                        "number": obj.obj.still_ball.number or obj.obj.rolling_ball.number,
                        "position": {"x": obj.obj.still_ball.pos.x or obj.obj.rolling_ball.pos.x, "y": obj.obj.rolling_ball.pos.y or obj.obj.still_ball.pos.y},
                        "color": BALL_COLOURS[obj.obj.still_ball.number or obj.obj.rolling_ball.number]
                    }
                else:
                    table_data["balls"].append({
                        "number": obj.obj.still_ball.number or obj.obj.rolling_ball.number,
                        "position": {"x": obj.obj.rolling_ball.pos.x or obj.obj.still_ball.pos.x, "y": obj.obj.still_ball.pos.y or obj.obj.rolling_ball.pos.y},
                        "color": BALL_COLOURS[obj.obj.still_ball.number or obj.obj.rolling_ball.number]
                    })
            elif isinstance(obj, Hole):
                table_data["holes"].append({
                    "position": {"x": obj.obj.hole.pos.x, "y": obj.obj.hole.pos.y}
                })
            elif isinstance(obj, HCushion):
                table_data["hcushions"].append({
                    "y": obj.obj.hcushion.y
                })
            elif isinstance(obj, VCushion):
                table_data["vcushions"].append({
                    "x": obj.obj.vcushion.x
                })

        return table_data

#//////////////////////////// SQL PART ///////////////////////////////////////////////////#

class Database:
    def __init__(self, db_path='poolgame.db', reset=False):
        self.db_path = db_path
        if reset:
            if os.path.exists(self.db_path):
                os.remove(self.db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.cur = self.conn.cursor()

    def read_latest_table_id(self):
        self.cur.execute("SELECT MAX(TABLEID) FROM TTable")
        latest_table_id = self.cur.fetchone()[0]
        return latest_table_id

    def createDB(self):
        # Your createDB code remains the same
        self.cur.execute("""CREATE TABLE Ball (BALLID INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
                    BALLNO INTEGER NOT NULL,
                    XPOS FLOAT NOT NULL,
                    YPOS FLOAT NOT NULL,
                    XVEL FLOAT,
                    YVEL FLOAT)""")

        self.cur.execute("""CREATE TABLE TTable (TABLEID INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
                    TIME FLOAT NOT NULL)""")

        self.cur.execute("""CREATE TABLE BallTable (BALLID INTEGER NOT NULL,
                    TABLEID INTEGER NOT NULL,
                    FOREIGN KEY (BALLID) REFERENCES Ball (BALLID),
                    FOREIGN KEY (TABLEID) REFERENCES TTable (TABLEID))""")

        self.cur.execute("""CREATE TABLE Shot (SHOTID INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
                    PLAYERID INTEGER NOT NULL,
                    GAMEID INTEGER NOT NULL,
                    FOREIGN KEY (PLAYERID) REFERENCES Player (PLAYERID),
                    FOREIGN KEY (GAMEID) REFERENCES Game (GAMEID))""")

        self.cur.execute("""CREATE TABLE TableShot (TABLEID INTEGER NOT NULL,
                    SHOTID INTEGER NOT NULL,
                    FOREIGN KEY (TABLEID) REFERENCES TTable (TABLEID),
                    FOREIGN KEY (SHOTID) REFERENCES Shot (SHOTID))""")

        self.cur.execute("""CREATE TABLE Game (GAMEID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    GAMENAME VARCHAR(64) NOT NULL)""")

        self.cur.execute("""CREATE TABLE Player (PLAYERID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    GAMEID INTEGER NOT NULL,
                    PLAYERNAME VARCHAR(64) NOT NULL,
                    FOREIGN KEY (GAMEID) REFERENCES Game (GAMEID))""")


        # Commit changes and check the data
        self.conn.commit()

    def get_latest_table_id(self):
        try:
            self.cur.execute("SELECT MAX(TABLEID) FROM TTable")
            result = self.cur.fetchone()
            latest_table_id = result[0] if result else None
            return latest_table_id
        except sqlite3.Error as e:
            print(f"Error fetching latest table ID: {e}")
            return None

    def readTable(self, tableID):
        print(f"Reading table with ID: {tableID} ")
        query = f"""
        SELECT Ball.BALLID, Ball.BALLNO, Ball.XPOS, Ball.YPOS, Ball.XVEL, Ball.YVEL, TTable.TIME
        FROM Ball
        INNER JOIN BallTable ON Ball.BALLID = BallTable.BALLID
        INNER JOIN TTable ON BallTable.TABLEID = TTable.TABLEID
        WHERE BallTable.TABLEID = {tableID + 1}
        """
        #ORDER BY Ball.BALLID ASC

        self.cur.execute(query)
        balls_data = self.cur.fetchall()

        if not balls_data:
            return None

        table = Table()
        table.time = balls_data[0][-1]  # Assuming the last item is the time

        for ball_data in balls_data:
            _, ball_no, xpos, ypos, x_vel, y_vel, _ = ball_data  # Adjusted to include BALLNO
            if x_vel == 0 and y_vel == 0:
                ball = StillBall(ball_no, Coordinate(xpos, ypos))  # Use ball_no for color
            else:
                ball = RollingBall(ball_no, Coordinate(xpos, ypos), Coordinate(x_vel, y_vel), Coordinate(0, 0))  # Use ball_no for color
            table += ball
        print(f"[Database] Fetched data for table ID {tableID}: {balls_data}")
        return table

    def writeTable(self, table):
        #print(f"Writing table with time: {table.time}")
        self.cur.execute("INSERT INTO TTable (TIME) VALUES (?)", (table.time,))
        table_id = self.cur.lastrowid

        for obj in table:
            if isinstance(obj, StillBall):
                ball_no = obj.obj.still_ball.number
                xpos, ypos = obj.obj.still_ball.pos.x, obj.obj.still_ball.pos.y
                xvel, yvel = 0, 0

                self.cur.execute("INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ?, ?, ?, ?)",
                                (ball_no, xpos, ypos, xvel, yvel))
                ball_id = self.cur.lastrowid
                self.cur.execute("INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)", (ball_id, table_id))

            elif isinstance(obj, RollingBall):
                ball_no = obj.obj.rolling_ball.number
                xpos, ypos = obj.obj.rolling_ball.pos.x, obj.obj.rolling_ball.pos.y
                xvel, yvel = obj.obj.rolling_ball.vel.x, obj.obj.rolling_ball.vel.y

                self.cur.execute("INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ?, ?, ?, ?)",
                                (ball_no, xpos, ypos, xvel, yvel))
                ball_id = self.cur.lastrowid
                self.cur.execute("INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)", (ball_id, table_id))

        #print(f"Written table ID: {table_id}")  # Adjust based on your DB API
        self.conn.commit()
        #print("[Database] Transaction committed.")
        return table_id

    def close(self):
        self.conn.close()

    def getGame(self, gameID):
        # Retrieve game details
        query = f"""
        SELECT Game.GAMENAME, P1.PLAYERNAME as Player1, P2.PLAYERNAME as Player2
        FROM Game
        JOIN Player P1 ON Game.GAMEID = P1.GAMEID AND P1.PLAYERID = (
            SELECT MIN(PLAYERID) FROM Player WHERE GAMEID = {gameID + 1}
        )
        JOIN Player P2 ON Game.GAMEID = P2.GAMEID AND P2.PLAYERID = (
            SELECT MAX(PLAYERID) FROM Player WHERE GAMEID = {gameID + 1}
        )
        WHERE Game.GAMEID = {gameID + 1}
        """
        self.cur.execute(query)
        result = self.cur.fetchone()
        return result if result else (None, None, None)

    def setGame(self, gameName, player1Name, player2Name):
        # Insert game and player details
        self.cur.execute("INSERT INTO Game (GAMENAME) VALUES (?)", (gameName,))
        gameID = self.cur.lastrowid
        self.cur.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)", (gameID, player1Name))
        self.cur.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)", (gameID, player2Name))
        self.conn.commit()
        return gameID - 1  # Adjusting for 0-based indexing

    def getPlayerID(self, gameID, playerName):
        """Retrieve a player's ID based on their name and the game ID."""
        query = """
        SELECT PLAYERID FROM Player WHERE GAMEID = ? AND PLAYERNAME = ?
        """
        try:
            self.cur.execute(query, (gameID, playerName))
            result = self.cur.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error retrieving player ID: {e}")
            return None

    def newShot(self, gameID, playerID):
        """Add a new shot entry for a player in a game and return the shot ID."""
        query = """
        INSERT INTO Shot (PLAYERID, GAMEID) VALUES (?, ?)
        """
        try:
            self.cur.execute(query, (playerID, gameID))
            self.conn.commit()
            return self.cur.lastrowid
        except Exception as e:
            print(f"Error adding new shot: {e}")
            return None


    def getGameDetailsByGameID(self, gameID):
        # Retrieve game details using a JOIN across Game and Player tables
        query = """
        SELECT g.GAMENAME, p1.PLAYERNAME as Player1, p2.PLAYERNAME as Player2
        FROM Game g
        JOIN Player p1 ON g.GAMEID = p1.GAMEID
        JOIN Player p2 ON g.GAMEID = p2.GAMEID
        WHERE g.GAMEID = ? AND p1.PLAYERID < p2.PLAYERID
        ORDER BY p1.PLAYERID ASC, p2.PLAYERID ASC
        """
        self.cur.execute(query, (gameID,))
        result = self.cur.fetchone()

        if result:
            return result  # Returns a tuple (gameName, player1Name, player2Name)
        else:
            return None, None, None  # Return None values if the game ID was not found

    def createGameAndPlayers(self, gameName, player1Name, player2Name):
        # Insert new game into Game table
        self.cur.execute("INSERT INTO Game (GAMENAME) VALUES (?)", (gameName,))
        gameID = self.cur.lastrowid  # Retrieve the newly created game ID

        # Insert first player (to ensure they get the lower PLAYERID)
        self.cur.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)", (gameID, player1Name))

        # Insert second player
        self.cur.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)", (gameID, player2Name))

        self.conn.commit()  # Commit the changes to the database

        return gameID  # Return the game ID for further use

    def recordTableShot(self, tableID, shotID):
        """Record the association between a table state and a shot."""
        try:
            self.cur.execute("INSERT INTO TableShot (TABLEID, SHOTID) VALUES (?, ?)", (tableID, shotID))
            self.conn.commit()
            return shotID
        except Exception as e:
            print(f"Error recording table shot: {e}")


class Game:
    sendtable = None
    def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):
        print("[Game Init] Initializing Game...")
        self.db = Database()  # Database instance created internally

        if gameID is not None:
            print(f"[Game Init] Initializing with gameID: {gameID}")
            self.gameID = gameID
            details = self.db.getGameDetailsByGameID(gameID)
            if details:
                self.gameName, self.player1Name, self.player2Name = details
                print(f"[Game Init] Game details loaded: {self.gameName}, Players: {self.player1Name}, {self.player2Name}")
            else:
                print("[Game Init] Game with the specified gameID not found.")
                raise ValueError("Game with the specified gameID not found.")
        elif all([gameName, player1Name, player2Name]):
            print(f"[Game Init] Creating new game: {gameName} with players {player1Name} and {player2Name}")
            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name
            self.gameID = self.db.createGameAndPlayers(gameName, player1Name, player2Name)
            print(f"[Game Init] New game created with gameID: {self.gameID}")
        else:
            print("[Game Init] Invalid constructor arguments provided.")
            raise TypeError("Invalid constructor arguments")

        self.table = None  # Placeholder for table initialization
        print("[Game Init] Game initialization completed.")

    def ballCounter(self,table):
        ballcount = 0
        for obj in table:
            if(isinstance(obj, StillBall) | isinstance(obj,RollingBall)):
                ballcount += 1

        return ballcount


    def stillballCounter(self,table):
        ballcount = 0
        for obj in table:
            if(isinstance(obj, StillBall)):
                ballcount += 1

        return ballcount


    def shoot(self, gameName, playerName, table, xvel, yvel):
        print(f"\n[Shoot] Starting shoot method for game: {gameName}, player: {playerName}")

        # Check if the game name matches
        if gameName != self.gameName:
            print(f"[Shoot] Mismatched game names: {gameName} != {self.gameName}")
            raise ValueError(f"The game name '{gameName}' does not match this game session.")

        # Get player ID and validate it
        playerID = 1
        if playerID is None:
            raise ValueError(f"Player {playerName} not found in this game.")

        # Record a new shot in the database
        shotID = self.db.newShot(self.gameID, playerID)
        print(f"[Shoot] New shot ID: {shotID}")

        print("before calculatins - ")
        print(table)

        # Find the cue ball and validate its presence
        cue_ball = table.findCueBall()
        if cue_ball is None:
            raise ValueError("Cue ball not found on the provided table.")
        print("cue ball - ")
        print(cue_ball)

        # Update cue ball to a rolling state with the given velocities
        #table.updateState(cue_ball, xvel, yvel)
        #print(f"[Shoot] Updated cue ball with velocities: xvel={xvel}, yvel={yvel}")

        cue_ballX = cue_ball.obj.still_ball.pos.x
        cue_ballY = cue_ball.obj.still_ball.pos.y

        cue_ball.type = phylib.PHYLIB_ROLLING_BALL

        cue_ball.obj.rolling_ball.vel.x = math.floor(xvel)
        cue_ball.obj.rolling_ball.vel.y = math.floor(yvel)
        cue_ball.obj.rolling_ball.pos.x = cue_ballX
        cue_ball.obj.rolling_ball.pos.y = cue_ballY

        speed = math.sqrt(xvel**2 + yvel**2)

        accX, accY = 0.0, 0.0

        if speed > 0.01:
            accX = -(xvel/speed)*DRAG
            accY = -(yvel/speed)*DRAG
        else:
            accX = 0
            accY = 0
        cue_ball.obj.rolling_ball.acc.x = accX
        cue_ball.obj.rolling_ball.acc.y = accY

        for obj in table:
            if isinstance(obj, (StillBall, RollingBall)) and obj == cue_ball:
                # Directly update the properties of the cue ball in the table
                obj.type = phylib.PHYLIB_ROLLING_BALL
                obj.vel.x = cue_ball.obj.rolling_ball.vel.x
                obj.vel.y = cue_ball.obj.rolling_ball.vel.y
                obj.pos.x = cue_ball.obj.rolling_ball.pos.x
                obj.pos.y = cue_ball.obj.rolling_ball.pos.y
                obj.acc.x = cue_ball.obj.rolling_ball.acc.x
                obj.acc.y = cue_ball.obj.rolling_ball.acc.y
                break  # Cue ball found and updated, exit the loop


        print("cue ball and table after calculations")
        print(cue_ball)
        print(table)

        #print("printing table index 25 is - ")
        #print(table.table[25])


        # Initial setup and validations omitted for brevity; assuming they're correctly implemented

        # Write the initial table state before segmentation
        initialTableID = self.db.writeTable(table)
        self.db.recordTableShot(initialTableID, shotID)

        print("Processing segments...")

        oldTime = table.time  # Ensure oldTime is initialized correctly as a float
        segment_counter = 0  # Initialize counter for segments

        while table is not None:


            seg = table.segment()  # Get the next segment
            if seg is None:
                break  # Exit loop if there are no more segments

            bcount = self.ballCounter(seg)
            stillbcount = self.stillballCounter(seg)

            if(bcount == stillbcount):
                print("Printing sendtable where balls are still - ")

                sendtable = seg
                print(sendtable)
                return seg


            newTime = seg.time  # Time of the new segment
            loopTime = math.floor((newTime - oldTime) / 0.01)  # Calculate frame count for the segment

            for k in range(loopTime):
                lTime = k * 0.01
                copyTable = table.roll(lTime)  # Roll the table to the current frame's state
                copyTable.time = oldTime + lTime  # Update copyTable's time

                # Optionally, save the state for significant frames only
                if k == loopTime - 1:  # Assuming the last frame in a segment is significant
                    svg_filename = f"table_{segment_counter}.svg"
                    svg_filepath = os.path.join("svgs", svg_filename)
                    with open(svg_filepath, 'w') as svg_file:
                        svg_file.write(copyTable.svg())  # Write SVG content

                    segment_counter += 1

            table = seg  # Move to the next segment for processing
            oldTime = newTime  # Update oldTime with the time of the new segment

            #tId = self.db.writeTable(copyTable)
            #self.db.recordTableShot(tId, shotID)



            '''if((obj.obj.still_ball.number == 1 | obj.obj.rolling_ball.number == 1 & (isinstance(obj,StillBall) | isinstance(obj,NULL))) &
            (obj.obj.still_ball.number == 2 | obj.obj.rolling_ball.number == 2 & (isinstance(obj,StillBall) | isinstance(obj,None))) &
            (obj.obj.still_ball.number == 3 | obj.obj.rolling_ball.number == 3 & (isinstance(obj,StillBall) | isinstance(obj,None))) &
            (obj.obj.still_ball.number == 4 | obj.obj.rolling_ball.number == 4 & (isinstance(obj,StillBall) | isinstance(obj,None))) &
            (obj.obj.still_ball.number == 5 | obj.obj.rolling_ball.number == 5 & (isinstance(obj,StillBall) | isinstance(obj,None))) &
            (obj.obj.still_ball.number == 6 | obj.obj.rolling_ball.number == 6 & (isinstance(obj,StillBall) | isinstance(obj,None))) &
            (obj.obj.still_ball.number == 7 | obj.obj.rolling_ball.number == 7 & (isinstance(obj,StillBall) | isinstance(obj,None))) &
            (obj.obj.still_ball.number == 8 | obj.obj.rolling_ball.number == 8 & (isinstance(obj,StillBall) | isinstance(obj,None))) &
            (obj.obj.still_ball.number == 9 | obj.obj.rolling_ball.number == 9 & (isinstance(obj,StillBall) | isinstance(obj,None))) &
            (obj.obj.still_ball.number == 10 | obj.obj.rolling_ball.number == 10 & (isinstance(obj,StillBall) | isinstance(obj,None))) &
            (obj.obj.still_ball.number == 11 | obj.obj.rolling_ball.number == 11 & (isinstance(obj,StillBall) | isinstance(obj,None))) &
            (obj.obj.still_ball.number == 12 | obj.obj.rolling_ball.number == 12 & (isinstance(obj,StillBall) | isinstance(obj,None))) &
            (obj.obj.still_ball.number == 13 | obj.obj.rolling_ball.number == 13 & (isinstance(obj,StillBall) | isinstance(obj,None))) &
            (obj.obj.still_ball.number == 14 | obj.obj.rolling_ball.number == 14 & (isinstance(obj,StillBall) | isinstance(obj,None))) &
            (obj.obj.still_ball.number == 15 | obj.obj.rolling_ball.number == 15 & (isinstance(obj,StillBall) | isinstance(obj,None))) &
            (obj.obj.still_ball.number == 0 | obj.obj.rolling_ball.number == 0 & (isinstance(obj,StillBall) | isinstance(obj,None)))):
                return table'''


        print("[Shoot] Shoot method completed.")







