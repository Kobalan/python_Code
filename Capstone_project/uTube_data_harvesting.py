C:\Windows\system32>git config --global user.name"Kobalan"

C:\Windows\system32>git config --global user.email"kobalanm2705@gmail.com"


python.exe -m pip install --upgrade pip
pip install streamlit
pip list
pip install google-api-python-client
python -m pip install mysql-connector-python
python -m pip install pymongo
#AIzaSyBMJHpVbZCMo65P3qucFfKM9nhYx4_h67A     —---->API Key


from googleapiclient.discovery import build
#API_Connection...
def getAPI_Key():
    api_key = 'AIzaSyBMJHpVbZCMo65P3qucFfKM9nhYx4_h67A'  #Google_API_Key
    youtube = build("youtube", "v3", developerKey=api_key)
    return youtube
    youtube=getAPI_Key()    #Storing function in variable for reusable    


#Channel_Details......
def getchannel_Details(id):
    channel_id = id  # Input Channel_ID.......
   
#Getting Channel_Details using Channel_ID.......
    request = youtube.channels().list(
        id=channel_id,
        part='snippet,statistics,contentDetails'
        )
    response = request.execute()                            #get this details in Google API Reference
    for i in response['items']:
        data=dict(
                Channel_id=channel_id,
                Channel_Name=i['snippet']['title'],
                Channel_description=i['snippet']['description'],
                Subscription_Count=i['statistics']['subscriberCount'],
                Channel_Views=i['statistics']['viewCount'],
                Total_Video_Count=i['statistics']['videoCount'],
                Playlist_Id=i['contentDetails']['relatedPlaylists']['uploads']
              )
    return data
#channel_Details=getchannel_Details('UC8kpe3Voh5besC4CxHRmQqQ')

#Getting Video IDs.......
def get_VideoID(Channel_id):
    video_ids=[]
    request1 = youtube.channels().list(
            id=Channel_id,
            part='contentDetails')
    response1=request1.execute()
    #For getting Video IDs we need Channel_Playlist ID
    playlist_ID=response1['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    next_page_token=None
    #maxResults does not guarantee the number of results on one page.
    #Incomplete results can be detected by a non-empty nextPageToken field in the result.
    #In order to retrieve the next page, perform the exact same request as previously and append a pageToken field with the value of nextPageToken from the previous page.
    #A new nextPageToken is provided on the following pages until all the results are retrieved.
    while True:
              request2=youtube.playlistItems().list(
                      part='snippet',
                      playlistId=playlist_ID,
                      maxResults=50,
                      pageToken=next_page_token
                  )
              response2=request2.execute()
              for i in range(len(response2['items'])):
                  video_ids.append(response2['items'][i]['snippet']['resourceId']['videoId'])
              next_page_token=response2.get('nextPageToken')
              if next_page_token is None:
                break    
    return video_ids
#video_IDs=get_VideoID('UC8kpe3Voh5besC4CxHRmQqQ')



#Getting Video Details
def get_videoDetails(video_IDs):
    video_data=[]
    for video_id in video_IDs:
        request=youtube.videos().list(
            part="snippet,ContentDetails,statistics",
            id=video_id
        )
       
        response=request.execute()
        for item in response['items']:
             data=dict(
                    Video_ID=item['id'],
                    Video_name=item['snippet']['title'],
                    Description=item['snippet']['description'],
                    Tags=item.get('tags'),                      #Tags Error
                    Published_Date=item['snippet']['publishedAt'],                        
                    Views_Count=item['statistics']['viewCount'],
                    Likes_Count=item['statistics']['likeCount'],                    
                    Favorite_Count=item['statistics']['favoriteCount'], #Dislike Count?
                    Comment_Count=item['statistics']['commentCount'],
                    Duration=item['contentDetails']['duration'],
                    Thumbnail=item['snippet']['thumbnails'],
                    Caption_Status=item['contentDetails']['caption']
                    )
        video_data.append(data)
    return video_data
#video_details=get_videoDetails(video_IDs)



#get Comment_Details
def get_comment_Details(video_IDs):
    try:
        comment_data=[]
        for video_id in video_IDs:
            request=youtube.commentThreads().list(
                        part="snippet",
                        videoId=video_id
            )        
            response=request.execute()
            for item in response['items']:
                data=dict(
                        Comment_ID=item['id'],
                        Comment_Text=item['snippet']['topLevelComment']['snippet']['textDisplay'],
                        Comment_Author=item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                        Comment_PublishedAt=item['snippet']['topLevelComment']['snippet']['publishedAt']
                        )
                comment_data.append(data)  
    except:
        pass              
    return comment_data
#comment_Details=get_comment_Details(video_IDs)


#Getting _playlist Details

def get_playlist_details(Channel_id):
    next_page_token=None
    playlist=[]
    while True:
        request=youtube.playlists().list(
                                part="snippet,contentDetails",
                                channelId=Channel_id,
                                maxResults=50,
                                pageToken=next_page_token
                    )        
        response=request.execute()
       
        for item in response['items']:
            data=dict(
                    Playlist__ID=item['id'],
                    Channel_id=item['snippet']['channelId'],
                    Playlist_name=item['snippet']['title']
                    )
            playlist.append(data)
        next_page_token=response.get('nextPageToken')
        if next_page_token is None:
            break
    return playlist









#Creating a Database in NOSql Database...
client=pymongo.MongoClient("mongodb://localhost:27017")#Connect to local_host db
db=client["Youtube_Data"]  #database name


def channel_info(channel_id):# First we get all data to insert into Collection
    channel_Details=getchannel_Details(channel_id)
    playlist_details=get_playlist_details(channel_id)
    video_IDs=get_VideoID(channel_id)
    video_Details=get_videoDetails(video_IDs)
    comment_Details=get_comment_Details(video_IDs)


    coll1=db["Channel_Info1"]  #Collection creation , in SQL it is called table
    coll1.insert_one({"channel_details":channel_Details,
                      "playlist_details":playlist_details,
                      "video_details":video_Details,
                      "comment_details":comment_Details})
    return "Database Updated"

result=channel_info("UC8kpe3Voh5besC4CxHRmQqQ")
result=channel_info("UCiooWjODnYOq1unQWWjwK9Q")

#      Channel_IDS
#UC8kpe3Voh5besC4CxHRmQqQ 
#UCGsYQnsvuTpWt8_mq-woDRw
#UCUcoxZczeUb7UwEVVGgzQnQ
#UCiooWjODnYOq1unQWWjwK9Q












#Creating a Database in SQL....
database= mysql.connector.connect(host="localhost",user ="root",
  password ="kobalan",auth_plugin="mysql_native_password",database="youtube")
cursor=database.cursor()
# cursor.execute("CREATE DATABASE youtube")


#Dropping the table if already created..
drop_query='''drop table if exists Channels'''
cursor.execute(drop_query)
database.commit()

try:
  Channel_details = """CREATE TABLE  IF NOT EXISTS Channels(
                    Channel_name  VARCHAR(100),
                    Channel_id VARCHAR(50) primary key,
                    Subscribers INT ,
                    Views int,
                    Total_Videos int,
                    Channel_Description text,
                    Playlist_Id varchar(100)
                    )"""
  # table created
  cursor.execute(Channel_details)
  database.commit()
except:
  print(" Table already Created")

#Creating a Dataframe using pandas Library
Ch_list=[]
db=client["Youtube_Data"]
coll1=db["Channel_Info1"]
for ch_data in coll1.find({},{"_id":0,"channel_details":1}):
    Ch_list.append(ch_data["channel_details"])
df=pd.DataFrame(Ch_list)    
df 


#Inserting values into table...

for index,row in df.iterrows():
    insert_values='''insert into Channels(Channel_name,
                    Channel_id,
                    Subscribers,
                    Views,
                    Total_Videos,
                    Channel_Description,
                    Playlist_Id)

                    values(%s,%s,%s,%s,%s,%s,%s)'''
    
    values=(row['Channel_Name'],
            row['Channel_id'],
            row['Subscription_Count'],
            row['Channel_Views'],
            row['Total_Video_Count'],
            row['Channel_description'],
            row['Playlist_Id'])

    try:
      cursor.execute(insert_values,values)
      database.commit()
    except:
      print("Values already inserted") 

                                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                   





















