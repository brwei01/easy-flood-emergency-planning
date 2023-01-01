from Input import User_Input
from Elevation import HighestElevationLocator
from Nearest_ITN import IntegratedTransportNetwork


def main():
    # user input and study area generation
    user_input, study_area = User_Input().input()
    print("user's location is:", user_input)
    # Plotter().show_rim(study_area)

    # generating cell values in study area
    dem_path = 'Material/elevation/SZ.asc'
    evacu_points = HighestElevationLocator(dem_path, study_area).highest_locator()
    print("evacuation point is:", evacu_points)

    # finding the nearest ITNs for user location and evacuation point
    itn_file_path = 'Material/itn/solent_itn.json'
    nearest_node_user_input = IntegratedTransportNetwork(itn_file_path, user_input).get_nearest_node_coords()
    print('nearest itn to user location:', nearest_node_user_input)
    nearest_node_highest_points = []
    for evacu_point in evacu_points:  # multiple solutions may exist
        nearest_node_highest_points = IntegratedTransportNetwork(itn_file_path, evacu_point).get_nearest_node_coords()
    print('nearest itn to evacuation points', nearest_node_highest_points)


if __name__ == '__main__':
    main()
