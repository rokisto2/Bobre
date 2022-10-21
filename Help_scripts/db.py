import pymysql
import math

class BotDB:

    def __init__(self):
        self.connect = pymysql.connect(host='localhost', user='root', password='1111', database='bobr_city')

    def close(self):
        print("Работа с базой данных завершена")
        self.connect.close()



    def user_add(self, user_id: int) -> object:
        # Добавляем юзера в бд
        try:

            with self.connect.cursor() as cursor:
                cursor.execute("INSERT INTO users (Telegram_id,Number_of_likes) VALUES (%s,0)", user_id)
            self.connect.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def get_all_attractions(self):
        # Берем все достопримечательности
        with self.connect.cursor() as cursor:
            cursor.execute("SELECT id, Name, Address FROM attractions ORDER BY Visited DESC")
            rows = cursor.fetchall()
            cursor.close()
            return rows

    def get_attraction(self, attraction_id):
        # Берем определённую достопримечательность
        with self.connect.cursor() as cursor:
            cursor.execute('UPDATE attractions SET Visited = Visited+1 WHERE id = %s', attraction_id)
            cursor.execute("SELECT * FROM attractions WHERE id = %s", attraction_id)
            info_attraction = cursor.fetchone()
            cursor.close()
            return info_attraction

    def get_attraction_img(self, attraction_id):
        # Берем картинки достопримечательность
        with self.connect.cursor() as cursor:
            cursor.execute("SELECT Img_Src FROM imgs WHERE Attraction_id = %s", attraction_id)
            img_attraction = cursor.fetchall()
            cursor.close()
            return img_attraction

    def add_attraction_from_user(self, user_id, attraction_id):
        # Добавляем избранные места пользователю
        with self.connect.cursor() as cursor:
            cursor.execute("UPDATE users SET Number_of_likes = Number_of_likes+1 WHERE Telegram_id = %s", user_id)
            cursor.execute('INSERT INTO users_like (Attraction_id, Telegram_user_id) VALUES (%s,%s)',
                           (attraction_id, user_id))
        self.connect.commit()

    def del_attraction_from_user(self, user_id, attraction_id):
        # Удаляем из избранного пользователя достопримечательность
        with self.connect.cursor() as cursor:
            cursor.execute("UPDATE users SET Number_of_likes = Number_of_likes-1 WHERE Telegram_id = %s", user_id)
            cursor.execute('DELETE FROM users_like WHERE Attraction_id = %s AND Telegram_user_id = %s',
                           (attraction_id, user_id))
        self.connect.commit()

    def get_user_Number_of_likes(self, user_id):
        with self.connect.cursor() as cursor:
            cursor.execute('SELECT Number_of_likes FROM users WHERE Telegram_id = %s', user_id)
            count = int(cursor.fetchone()[0])
            cursor.close()
            return count

    def get_like_attraction_from_user(self, user_id):
        # Показываем избронные достопримечательности пользователя
        with self.connect.cursor() as cursor:
            cursor.execute(
                'SELECT attractions.id, attractions.Name, attractions.Address from attractions, users_like  WHERE attractions.id = users_like.Attraction_id AND users_like.Telegram_user_id = %s',
                user_id)
            like_attractions = cursor.fetchall()
            cursor.close()
            return like_attractions

    def is_user_like_attraction(self, user_id, attraction_id):
        # Проверяем есть ли достопримечательность в избранном пользователя
        with self.connect.cursor() as cursor:
            cursor.execute('SELECT * FROM users_like WHERE Telegram_user_id = %s AND Attraction_id = %s',
                           (user_id, attraction_id))
            like_attractions = cursor.fetchall()
            cursor.close()
        if len(like_attractions) == 1:
            return False
        else:
            return True
    #Ишем ближашую достопримечательность
    def get_attraction_with_location(self, latitude, longitude):
        with self.connect.cursor() as cursor:
            cursor.execute(
                'SELECT id, latitude, longitude from attractions')
            attractions = cursor.fetchall()
            id = 0
            maxx:float = 10000000.1
            for attraction in attractions:
                latitude1 = attraction[1]
                longitude1 = attraction[2]
                length = math.sqrt(abs(latitude1 - latitude)*abs(latitude1 - latitude)+abs(longitude1 - longitude)*abs(longitude1-longitude))
                if maxx>length:
                    maxx = length
                    id = attraction[0]
            cursor.close()
            print(id)
            return id

