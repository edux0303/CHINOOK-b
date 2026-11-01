from database.DB_connect import DBConnect
from model.album import Album

class DAO():

    @staticmethod
    def getNodi():
        conn = DBConnect.get_connection()
        results = []
        if conn is None:
            return results

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT ab.AlbumId AS abId, ab.Title AS titolo, ab.ArtistId AS arId, COUNT(*) as numero
                FROM  album ab, track t
                WHERE ab.AlbumId = t.AlbumId
                GROUP by ab.AlbumId,ab.Title,ab.ArtistId
                """
        cursor.execute(query)
        for row in cursor:
            a = Album(int(row["abId"]), row["titolo"], int(row["arId"]),int(row["numero"]))
            results.append(a)
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAlbumTrack():
        conn = DBConnect.get_connection()
        results = []
        if conn is None:
            return results

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT t.AlbumId AS abId, t.TrackId as tId
                FROM track t
                """
        cursor.execute(query)
        for row in cursor:

            results.append((int(row["abId"]), int(row["tId"])))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getEdges():
        conn = DBConnect.get_connection()
        results = []
        if conn is None:
            return results

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT ab1.AlbumId AS id1, ab2.AlbumId AS id2
                FROM album ab1, album ab2, track t1, track t2
                WHERE ab1.AlbumId < ab2.AlbumId AND t1.GenreId = t2.GenreId AND ab1.AlbumId = t1.AlbumId AND ab2.AlbumId = t2.AlbumId AND t1.TrackId <> t2.TrackId       
                """
        cursor.execute(query)
        for row in cursor:
            results.append((int(row["id1"]), int(row["id2"])))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getGeneriAlbum():
        conn = DBConnect.get_connection()
        if conn is None:
            return []
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT DISTINCT t.AlbumId AS idA, t.GenreId AS idG
                FROM Track t
                """
        cursor.execute(query)
        for row in cursor:
            results.append((row["idA"], row["idG"]))
        cursor.close()
        conn.close()
        return results
