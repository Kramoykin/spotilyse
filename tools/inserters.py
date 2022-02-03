# Current module provides an ability to insert the data coolected from the spotify api
# to the Postgres database. For each table (artist and track) exists its own inserter 
# function. 

import psycopg2
import pandas

def insert_artist(
        artist_df,
        user="ivan-pc",
        password="passwd",
        host="localhost",
        port="5432",
        database="spotilyse"
        ):
    """
    This function is preordained for data insertion into the artist table.
    It inserts all the rows from artist_df, if row with such id is already
    exist then popularity, followers and update columns will be updated.
    
    Parameters
    ----------
    artist_df : pandas.DataFrame()
        pandas dataframe with artist info. 
    user : str
        database user
    password : str
        database password
    host : str
        database host
    port : str
        database port
    database : str
        database name
    """
    # The insert query for the artist database
    artist_insert_query = """ 
        INSERT INTO artist (id, 
                            name, 
                            popularity,
                            genre,
                            followers,
                            update) 
        VALUES (%s,%s,%s,%s,%s,%s)
        ON CONFLICT (id)
        DO UPDATE SET
            popularity = EXCLUDED.popularity,
            followers = EXCLUDED.followers,
            update = EXCLUDED.update
                           """
                           
    # Try to connect to a database
    try:
        connection = psycopg2.connect(user = user,
                                      password = password,
                                      host = host,
                                      port = port,
                                      database = database)
    except psycopg2.OperationalError as err:
        # pass exception to function
        print(err)
        # set the connection to 'None' in case of error
        connection = None
        
    if connection:
        # create the cursor
        cursor = connection.cursor()
        # iterate through the rows
        for row in artist_df.itertuples():
            # fill the rectord to insert from a row
            record_to_insert = (getattr(row, 'Index'), 
                                getattr(row, 'artist_name'), 
                                getattr(row, 'artist_popularity'),
                                getattr(row, 'artist_genre'), 
                                getattr(row, 'artist_followers'), 
                                getattr(row, 'update'))
            # insert a row
            cursor.execute(artist_insert_query, record_to_insert)
            
        connection.commit() # commit all the insertions
        
        cursor.close() # close the cursor
        
        connection.close() # close the connection
        
        
def insert_track(
        track_df,
        user="ivan-pc",
        password="passwd",
        host="localhost",
        port="5432",
        database="spotilyse"
        ):
    """
    This function is preordained for data insertion into the track table.
    It inserts all the rows from artist_df, if row with such id is already
    exist then popularity, followers and update columns will be updated.
    
    Parameters
    ----------
    track_df : pandas.DataFrame()
        pandas dataframe with track info. 
    user : str
        database user
    password : str
        database password
    host : str
        database host
    port : str
        database port
    database : str
        database name
    """
    # The insert query for the artist database
    track_insert_query = """ 
        INSERT INTO track (id, 
                           name, 
                           artist_id,
                           popularity,
                           release_date,
                           update,
                           danceability,
                           energy,
                           key,
                           loudness,
                           mode,
                           speechiness,
                           acousticness,
                           instrumentalness,
                           liveness,
                           valence,
                           tempo,
                           duration_ms,
                           time_signature) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (id)
        DO UPDATE SET
            popularity = EXCLUDED.popularity,
            update = EXCLUDED.update
                           """
                           
    # Try to connect to a database
    try:
        connection = psycopg2.connect(user = user,
                                      password = password,
                                      host = host,
                                      port = port,
                                      database = database)
    except psycopg2.OperationalError as err:
        # pass exception to function
        print(err)
        # set the connection to 'None' in case of error
        connection = None
        
    if connection:
        connection.autocommit = True
        # create the cursor
        cursor = connection.cursor()
        # iterate through the rows
        for row in track_df.itertuples():
            # fill the rectord to insert from a row
            record_to_insert = (getattr(row, 'Index'), 
                                getattr(row, 'name'), 
                                getattr(row, 'artist_id'),
                                getattr(row, 'popularity'), 
                                getattr(row, 'release_date'), 
                                getattr(row, 'update'),
                                round(getattr(row, 'danceability'), 3),
                                round(getattr(row, 'energy'), 3),
                                getattr(row, 'key'),
                                round(getattr(row, 'loudness'), 3),
                                bool(getattr(row, 'mode')),
                                round(getattr(row, 'speechiness'), 3),
                                round(getattr(row, 'acousticness'), 3),
                                round(float(getattr(row, 'instrumentalness')), 7),
                                round(getattr(row, 'liveness'), 3),
                                round(getattr(row, 'valence'), 3),
                                round(getattr(row, 'tempo'), 3),
                                getattr(row, 'duration_ms'),
                                getattr(row, 'time_signature'))
            # insert a row
            try:
                cursor.execute(track_insert_query, record_to_insert)
            except psycopg2.IntegrityError as err:
                #cursor.execute('rollback')
                print(err)
                    
        cursor.close() # close the cursor
        
        connection.close() # close the connection
            
        
        
