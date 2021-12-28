# Current module provides an ability to get the data from the spotify api.
# For each operation exists corresponding function. Functions basically
# write responds to the specified .csv files. Some of them may use the output
# of other functions as input. It is assumend to implement this by writing an 
# output to and reading an input from yaml configure files. Some wrapper functions
# for such operations are presented in utils module.


import pandas as pd
#import datetime
from os.path import expanduser
from itertools import zip_longest


def get_categories(
        spotify, 
        country = 'US', 
        path = expanduser('~')
        ):
    """
    A function used to get the .csv file containing stopify categories info
    for certain country.
    
    Parameters
    ----------
    spotify : spotify.client.Spotify() instance
        Spotify API client with valid credentials
    country : str
        ISO 3166-1 alpha-2 country code (default 'US')
    path : str
        path to the directory in which will be saved 
        <country>.csv file (default os.path.expanduser('~') - user HOME dir)
        
    Returns
    ----------
    pandas.DataFrame
        a dataframe with country categories information
    """
    # get the results by request
    results = spotify.categories(country, limit = 50)['categories']
    categories = results['items'] # list for creating pandas df
    
    # iterate through all possible categories and extend the list
    while results['next']:
         results = spotify.next(results)['categories']
         categories.extend(results['items'])
         
    # Create a dict for df construction
    cat_dict = {key : [] for key in ['category_name', 'category_id']}
    
    # Fill the dict with curtain values from a list
    for cat in categories:
         cat_dict['category_name'].append(cat['name'])
         cat_dict['category_id'].append(cat['id'])
    
    #Create a pandas df
    df = pd.DataFrame(cat_dict)
    
    # Export dataframe to a csv file
    df.to_csv(path + country + '.csv', index = False)
    
    return df

def get_global_top(
        spotify, 
        path = expanduser('~')
        ):
    """
    A function used to get the .csv file containing stopify top tracks from 
    global charts.
    
    Parameters
    ----------
    spotify : spotify.client.Spotify() instance
        Spotify API client with valid credentials
    path : str
        path to the directory in which will be saved 
        Global.csv file (default os.path.expanduser('~') - user HOME dir)
        
    Returns
    ----------
    pandas.DataFrame
        a dataframe with global charts information
    """
    # list with the ID's of top playlists
    top_playlists_ids = [plst['id'] for plst in spotify.category_playlists('toplists', country = None)['playlists']['items']]
    # list for all items from all top playlists
    itms_list = []
    # fill items list
    for id_ in top_playlists_ids:
        results = spotify.playlist_items(id_, additional_types = ['track'])
        itms_list.extend(results['items'])
        while results['next']:
            results = spotify.next(results)
            itms_list.extend(results['items'])
    
    # Create a dict for df construction
    track_dict = {key : [] for key in ['id', 'name', 
                                       'artist_id', 'artist_name', 
                                       'track_popularity']}
    
    # Fill the tracks list with top songs
    for res in itms_list:
        if res['track'] is not None:
            if res['track']['id'] not in track_dict['id']:
                track_dict['id'].append(res['track']['id'])
                track_dict['name'].append(res['track']['name'])
                track_dict['artist_id'].append(res['track']['artists'][0]['id'])
                track_dict['artist_name'].append(res['track']['artists'][0]['name'])
                track_dict['track_popularity'].append(res['track']['popularity'])
    
    #Create a pandas df
    df = pd.DataFrame(track_dict)
    df = df.sort_values(by = ['track_popularity', 'name'], ascending = [False, True])
    
    # Export dataframe to a csv file
    df.to_csv(path + 'Global.csv', index = False)    
    
    return df

def get_country_top(
        spotify, 
        plsts = [], 
        country = None, 
        path = expanduser('~')
        ):
    """
    A function used to get the top chart for a certain country. Chart is based
    on the plsts parameter. Playlysts can be provided by the get_playlists 
    function, but it may be needed some manual filtering of its result for avoiding
    tracks from global charts.
    
    Parameters
    ----------
    spotify : spotify.client.Spotify() instance
        Spotify API client with valid credentials
    plsts : list of strings
        list of the ID's for all playlists will be used for chart creating.
    country : str
        ISO 3166-1 alpha-2 country code (default 'US')
    path : str
        path to the directory in which will be saved 
        <country>.csv file (default os.path.expanduser('~') - user HOME dir)

    Returns
    -------
    pandas.DataFrame
        a dataframe with country charts information.

    """
    # list for all items from all top playlists
    itms_list = []
    # fill items list
    for id_ in plsts:
        results = spotify.playlist_items(id_, additional_types = ['track'])
        itms_list.extend(results['items'])
        while results['next']:
            results = spotify.next(results)
            itms_list.extend(results['items'])
    
    # Create a dict for df construction
    track_dict = {key : [] for key in ['id', 'name', 
                                       'artist_id', 'artist_name', 
                                       'track_popularity']}
    
    # Fill the tracks list with top songs
    for res in itms_list:
        if res['track'] is not None:
            if res['track']['id'] not in track_dict['id']:
                track_dict['id'].append(res['track']['id'])
                track_dict['name'].append(res['track']['name'])
                track_dict['artist_id'].append(res['track']['artists'][0]['id'])
                track_dict['artist_name'].append(res['track']['artists'][0]['name'])
                track_dict['track_popularity'].append(res['track']['popularity'])
    
    #Create a pandas df
    df = pd.DataFrame(track_dict)
    df = df.sort_values(by = ['track_popularity', 'name'], ascending = [False, True])
    
    # Export dataframe to a csv file
    df.to_csv(path + country + '.csv', index = False)    
    
    return df

def get_playlists(
        spotify, 
        category_ids = ['toplists'],
        country = None,
        path = expanduser('~')
        ):
    """
    A function used to get the .csv file containing stopify playlist for
    given categories and country.
    
    Parameters
    ----------
    spotify : spotify.client.Spotify() instance
        Spotify API client with valid credentials
    categori_ids : list of str
        list, containing id's of desired categories for playlists compilation
    country : str
        ISO 3166-1 alpha-2 country code (default 'US')
    path : str
        path to the directory in which will be saved 
        <country>.csv file (default os.path.expanduser('~') - user HOME dir)
        
    Returns
    ----------
    pandas.DataFrame
        a dataframe with global playlists compilation
    """
     # Create a playlists dict for df construction
    plst_dict = {key : [] for key in [ 'name', 'id']}
    
    # Fill the plst dict
    for id_ in category_ids:
        toplists = spotify.category_playlists(id_, country = country)['playlists']['items']
        for top in toplists:
            if top['id'] not in plst_dict['id']:
                plst_dict['id'].append(top['id'])
                plst_dict['name'].append(top['name'])
            
    #Create a pandas df
    df = pd.DataFrame(plst_dict)
    
    # Construct the name of a file
    if country is None:
        name = 'GLobal'
    else:
        name = country
    
    # Export dataframe to a csv file
    df.to_csv(path + name + '.csv', index = False)    
    
    return df

def get_releases(
        spotify, 
        country = None, 
        path = expanduser('~')
        ):
    """
    A function used to get the .csv file containing stopify new releases albums
    for given country.
    
    Parameters
    ----------
    spotify : spotify.client.Spotify() instance
        Spotify API client with valid credentials
    country : str
        ISO 3166-1 alpha-2 country code (default 'US')
    path : str
        path to the directory in which will be saved 
        <country>.csv file (default os.path.expanduser('~') - user HOME dir)
        
    Returns
    ----------
    pandas.DataFrame
        a dataframe with new releases info
    """
    # Create a playlists dict for df construction
    albums_dict = {key : [] for key in [ 'name', 'id', 'release_date']}
   
    itms_list = [] # list for all albums from new releases
    
    # get all new releases from api
    results = spotify.new_releases(country = country, limit = 50)['albums']
    itms_list.extend(results['items'])
    while results['next']:
        results = spotify.next(results)['albums']
        itms_list.extend(results['items'])
            
    # fill albums_dict with new releases
    for res in itms_list:
        if res['id'] not in albums_dict['id']:
            albums_dict['id'].append(res['id'])
            albums_dict['name'].append(res['name'])
            albums_dict['release_date'].append(res['release_date'])
    
    #Create a pandas df
    df = pd.DataFrame(albums_dict)
    
    # Construct the name of a file
    if country is None:
        name = 'GLobal'
    else:
        name = country
    
    # Export dataframe to a csv file
    df.to_csv(path + name + '.csv', index = False)    
    
    return df

def get_albums_tracks(
        spotify, 
        country = None,
        albums_ids = [],
        path = expanduser('~')
        ): 
    """
    A function used to get the .csv file containing stopify new releases albums
    for given country.
    
    Parameters
    ----------
    spotify : spotify.client.Spotify() instance
        Spotify API client with valid credentials
    country : str
        ISO 3166-1 alpha-2 country code (default 'US')
    album_ids : list of str
        array with album ID's
    path : str
        path to the directory in which will be saved 
        <country>.csv file (default os.path.expanduser('~') - user HOME dir)
        
    Returns
    ----------
    pandas.DataFrame
        a dataframe with new track info for all albums from albums_ids
    """
    
    itms_list = [] # list for all items from all top playlists
    # fill items list
    for id_ in albums_ids:
        results = spotify.album_tracks(id_, limit = 50)
        itms_list.extend(results['items'])
        while results['next']:
            results = spotify.next(results)
            itms_list.extend(results['items'])
            
    # Create a dict for df construction
    track_dict = {key : [] for key in ['id', 'name', 
                                       'artist_id', 'artist_name',
                                        'danceability', 'energy',
                                        'key', 'loudness',
                                        'mode', 'speechiness',
                                        'acousticness', 'instrumentalness',
                                        'liveness', 'valence', 
                                        'tempo', 'duration_ms',
                                        'time_signature']}
    
    # Fill the tracks list with top songs
    for res in itms_list:
        if res is not None:
            if res['id'] not in track_dict['id']:
                track_dict['id'].append(res['id'])
                track_dict['name'].append(res['name'])
                track_dict['artist_id'].append(res['artists'][0]['id'])
                track_dict['artist_name'].append(res['artists'][0]['name'])
                      
    features = [] # list for all track's features
    # the procedure of proper track_dict splitting (spotify.audio_features() 
    # can use lists with length <= 100)
    bounds = [x for x in range(0, len(track_dict['id']), 100)]
    for b in bounds[:-1]:
        features.extend(spotify.audio_features(track_dict['id'][b:b+99]))
    features.extend(spotify.audio_features(track_dict['id'][bounds[-1]:-1])) 
    
    # process of filling the proper rows with features information
    for id_, f in zip_longest(track_dict['id'], features):
        if f is not None:
            if f['id'] in track_dict['id']:
                track_dict['danceability'].append(f['danceability'])
                track_dict['energy'].append(f['energy'])
                track_dict['key'].append(f['key'])
                track_dict['loudness'].append(f['loudness'])
                track_dict['mode'].append(f['mode'])
                track_dict['speechiness'].append(f['speechiness'])
                track_dict['acousticness'].append(f['acousticness'])
                track_dict['instrumentalness'].append(f['instrumentalness'])
                track_dict['liveness'].append(f['liveness'])
                track_dict['valence'].append(f['valence'])
                track_dict['tempo'].append(f['tempo'])
                track_dict['duration_ms'].append(f['duration_ms'])
                track_dict['time_signature'].append(f['time_signature'])
            else:
                track_dict['danceability'].append(None)
                track_dict['energy'].append(None)
                track_dict['key'].append(None)
                track_dict['loudness'].append(None)
                track_dict['mode'].append(None)
                track_dict['speechiness'].append(None)
                track_dict['acousticness'].append(None)
                track_dict['instrumentalness'].append(None)
                track_dict['liveness'].append(None)
                track_dict['valence'].append(None)
                track_dict['tempo'].append(None)
                track_dict['duration_ms'].append(None)
                track_dict['time_signature'].append(None)
        else:
            track_dict['danceability'].append(None)
            track_dict['energy'].append(None)
            track_dict['key'].append(None)
            track_dict['loudness'].append(None)
            track_dict['mode'].append(None)
            track_dict['speechiness'].append(None)
            track_dict['acousticness'].append(None)
            track_dict['instrumentalness'].append(None)
            track_dict['liveness'].append(None)
            track_dict['valence'].append(None)
            track_dict['tempo'].append(None)
            track_dict['duration_ms'].append(None)
            track_dict['time_signature'].append(None)
    
    #Create a pandas df
    df = pd.DataFrame(track_dict)
    
    # Construct the name of a file
    if country is None:
        name = 'GLobal'
    else:
        name = country
    
    # Export dataframe to a csv file
    df.to_csv(path + name + '.csv', index = False)    
    
    return df 

# def get_albums_tracks(spotify, 
#                      country = None,
#                      albums_ids = [],
#                      path = expanduser('~')): 
    
#     # list for all items from all top playlists
#     itms_list = []
#     # fill items list
#     for id_ in albums_ids:
#         results = spotify.album_tracks(id_, limit = 50)
#         itms_list.extend(results['items'])
#         while results['next']:
#             results = spotify.next(results)
#             itms_list.extend(results['items'])
            
#     # Create a dict for df construction
#     track_dict = {key : [] for key in ['id', 'name', 
#                                        'artist_id', 'artist_name',
#                                        'danceability', 'energy',
#                                        'key', 'loudness',
#                                        'mode', 'speechiness',
#                                        'acousticness', 'instrumentalness',
#                                        'liveness', 'valence', 
#                                        'tempo', 'duration_ms',
#                                        'time_signature']}
    
#     # Fill the tracks list with top songs
#     for res in itms_list:
#         if res is not None:
#             if res['id'] not in track_dict['id']:
#                 features = spotify.audio_features([res['id']])[0] 
#                 track_dict['id'].append(res['id'])
#                 track_dict['name'].append(res['name'])
#                 track_dict['artist_id'].append(res['artists'][0]['id'])
#                 track_dict['artist_name'].append(res['artists'][0]['name'])
#                 if features is not None:
#                     track_dict['danceability'].append(features['danceability'])
#                     track_dict['energy'].append(features['energy'])
#                     track_dict['key'].append(features['key'])
#                     track_dict['loudness'].append(features['loudness'])
#                     track_dict['mode'].append(features['mode'])
#                     track_dict['speechiness'].append(features['speechiness'])
#                     track_dict['acousticness'].append(features['acousticness'])
#                     track_dict['instrumentalness'].append(features['instrumentalness'])
#                     track_dict['liveness'].append(features['liveness'])
#                     track_dict['valence'].append(features['valence'])
#                     track_dict['tempo'].append(features['tempo'])
#                     track_dict['duration_ms'].append(features['duration_ms'])
#                     track_dict['time_signature'].append(features['time_signature'])
#                 else:
#                     track_dict['danceability'].append(None)
#                     track_dict['energy'].append(None)
#                     track_dict['key'].append(None)
#                     track_dict['loudness'].append(None)
#                     track_dict['mode'].append(None)
#                     track_dict['speechiness'].append(None)
#                     track_dict['acousticness'].append(None)
#                     track_dict['instrumentalness'].append(None)
#                     track_dict['liveness'].append(None)
#                     track_dict['valence'].append(None)
#                     track_dict['tempo'].append(None)
#                     track_dict['duration_ms'].append(None)
#                     track_dict['time_signature'].append(None)

#     #Create a pandas df
#     df = pd.DataFrame(track_dict)
#     #df = df.sort_values(by = ['track_popularity', 'name'], ascending = [False, True])
    
#     # Construct the name of a file
#     if country is None:
#         name = 'GLobal'
#     else:
#         name = country
    
#     # Export dataframe to a csv file
#     df.to_csv(path + name + '.csv', index = False)    
    
#     return df    