"""
program that creates online map with location of user's friends
"""
import tweepy
from flask import Flask, render_template, redirect, request, url_for
import folium
from geopy.geocoders import Nominatim


def authentification():
    """
    authentificates user's API
    :return: nothing
    """
    auth = tweepy.OAuthHandler('your key can be here :)',
                               'your key can be here :)')
    auth.set_access_token('your key can be here :)',
                          'your key can be here :)')
    api = tweepy.API(auth)
    return api


def create_map(locations):
    """
    creates folium map
    :param locations: coordinates of folium tags
    :return: nothing
    """
    geolocator = Nominatim(user_agent="geopy/1.11.0")
    new_locations = []
    for location in locations:
        try:
            loc = geolocator.geocode(location[0])
            if str(loc) != 'None':
                new_locations.append((loc.latitude, loc.longitude, location[1]))
        except:
            pass
    cur_map = folium.Map(zoom_start=2, )
    for i in range(len(new_locations)):
        cur_map.add_child(folium.Marker(location=(new_locations[i][0], new_locations[i][1]),
                                        popup=new_locations[i][2],
                                        icon=folium.Icon(color='darkpurple', icon='off')))
    folium.TileLayer('Stamen Terrain').add_to(cur_map)  # adds some map styles
    folium.TileLayer('Stamen Toner').add_to(cur_map)
    folium.TileLayer('Stamen Water Color').add_to(cur_map)
    folium.TileLayer('cartodbpositron').add_to(cur_map)
    folium.TileLayer('cartodbdark_matter').add_to(cur_map)
    cur_map.add_child(folium.LayerControl())  # adds the ability to control layers
    cur_map.save('templates/map.html')


def getlocations(user_name):
    """
    gets locations using geopy
    :param user_name: user_name
    :return: nothing
    """
    api = authentification()
    # name = input()
    #user_name = '@wlade_k'
    # user = api.get_user(screen_name=name)
    friends = api.get_friends(screen_name=user_name)
    locations = []
    for friend in friends:
        locations.append((friend.location, friend.screen_name))
    create_map(locations)


app = Flask(__name__)


@app.route("/")
def home():
    error = request.args.get('message')
    return render_template("index.html", error=error)


@app.route('/name', methods=['GET', 'POST'])
def first_page():
    username = request.form["button_name"]
    try:
        getlocations(username)
        return render_template('map.html')
    except:
        return redirect(url_for("home", message="User not found!"))


if __name__ == '__main__':
    app.run(debug=True)
