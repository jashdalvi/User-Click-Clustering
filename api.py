from fastapi import FastAPI
from sklearn.cluster import DBSCAN
import mysql.connector
from pydantic import BaseModel

app = FastAPI()

class Point(BaseModel):
    x : float
    y : float
# Connect to the database
db_conn = mysql.connector.connect(user='root', password='****',
                              host='127.0.0.1', database = "clicks")

db_cursor = db_conn.cursor()


# Initialize the DBSCAN algorithm
dbscan = DBSCAN(eps=0.1, min_samples=5)

db_cursor.execute("SELECT x, y FROM coordinates")
coordinates = db_cursor.fetchall()
if len(coordinates) > 0:
    dbscan.fit(coordinates)


@app.post("/add_point")
def add_point(point : Point):
    # Add the new coordinate to the database
    add_coordinate = ("INSERT INTO coordinates (x, y) VALUES (%s, %s)")
    data_coordinate = (round(point.x, 4), round(point.y, 4))
    db_cursor.execute(add_coordinate, data_coordinate)
    db_conn.commit()
    
    # Get all coordinates from the database
    db_cursor.execute("SELECT x, y FROM coordinates")
    coordinates = db_cursor.fetchall()
    
    # Perform clustering on the coordinates
    dbscan.fit(coordinates)

    # Get the cluster ID of the new coordinate
    cluster_id = dbscan.labels_.tolist()[-1]
    
    return {"cluster_id": cluster_id}


@app.get("/clusters")
def get_clusters():
    # Get all coordinates from the database
    db_cursor.execute("SELECT x, y FROM coordinates")
    coordinates = db_cursor.fetchall()
    
    # Organize the coordinates into clusters
    clusters = {}
    for i, label in enumerate(dbscan.labels_.tolist()):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(coordinates[i])
    
    return {"clusters": clusters}

@app.get("/clusterid")
def get_clusterid(x : float, y : float):
    data_coordinate = (round(x,4), round(y,4))
    
    ## Given id is entered in a serial order in a database
    db_cursor.execute("SELECT id FROM coordinates where x = %s and y = %s" % (data_coordinate))
    id_ = db_cursor.fetchall()

    if len(id_) > 0:
        # Get the cluster ID of the new coordinate
        id_ = id_[0][0]
        cluster_id = dbscan.labels_.tolist()[int(id_ - 1)]
    else:
        cluster_id = None
    
    return {"cluster_id": cluster_id}