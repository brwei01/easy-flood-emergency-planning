from shapely.geometry import Point, Polygon, MultiPolygon
import geopandas as gpd
import matplotlib


class UserInput(object):
    def __init__(self):
        pass

    def input(self):
        # initialize a boolean, assuming that the user wish to proceed.
        proceed = True
        while proceed:
            # if the user wish to proceed
            try:
                easting, northing = list(map(float, (input('input easting: '), input('input northing:'))))
            except ValueError:
                print('Wrong input type, please input a numeric number')
                proceed = self.proceed_judgement()
            else:
                sa = StudyArea(easting, northing)
                island_boundary = sa.get_island_boundary()
                circle = sa.circle()
                boundary_rectangle = sa.get_rectangle()
                point = Point(easting, northing)

                try:
                    if any([easting < 425000, northing < 75000, easting > 470000, northing > 100000]):
                        raise OutMapRangeError
                    if not point.within(boundary_rectangle) and not point.touches(boundary_rectangle):
                        raise OutBoundaryRectangleError
                    if not point.within(island_boundary) and not point.touches(island_boundary):
                        raise OutIslandAreaError

                # if input location is out of island area
                except OutIslandAreaError:
                    print('Might be a mistake! Input location not on Island')
                    proceed = self.proceed_judgement()

                # if on island but out of study area
                except OutMapRangeError:
                    print('input location out of map range')
                    proceed = self.proceed_judgement()

                # this following clause is reserved for task 6
                # if on island but out of 5 km inwards rectangle
                except OutBoundaryRectangleError:
                    print('5km radius from user location out of map range, but no worries system can handle')
                    study_area = circle.intersection(boundary_rectangle)
                    return (easting, northing), study_area

                else:
                    # study area as the intersection between the buffer and boundary_rectangle
                    study_area = circle.intersection(boundary_rectangle)
                    return (easting, northing), study_area

    # function to return a flag true or false
    # used for judging does the user wish to proceed or quit.
    def proceed_judgement(self):
        print('Do you wish to re-enter the values?')
        flag = True
        user_in = input('input y to re-enter, n to quit the programme[y/n]')
        if user_in == 'y':
            pass
        elif user_in == 'n':
            flag = False
        else:
            print('please type [y/n]')
        return flag


# Error Classes
class Error(Exception):
    pass


class OutBoundaryRectangleError(Error):
    pass


class OutMapRangeError(Error):
    pass


class OutIslandAreaError(Error):
    pass


# Study area delineation
class StudyArea(object):
    def __init__(self, easting, northing):
        self.easting = easting
        self.northing = northing

    def circle(self):
        # used to make 5000m buffer from user input point
        client_pt = Point(self.easting, self.northing)
        circle = client_pt.buffer(5000)
        return circle

    def get_rectangle(self):
        # built up a boundary rectangle as defined by task1
        x1, x2 = 425000, 470000
        y1, y2 = 75000, 100000
        boundary_polygon = Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])
        return boundary_polygon

    def get_island_boundary(self):
        # read the isle of wight outlines shape file
        gdf = gpd.read_file('Material/shape/isle_of_wight.shp')
        gdf.set_geometry(gdf['geometry'])
        gdf.set_crs('EPSG:27700')
        # return the outlines as geometry array
        return gdf['geometry'].values[0]


