import pymysql


USER = "admin"
PASSWORD = "dbuserdbuser"
HOST = "db1.cyl4xx6wpuab.us-east-1.rds.amazonaws.com"
TABLE_NAME = "f22_databases.product"


class Products:

    def __int__(self):
        pass


    def _get_connection():

        conn = pymysql.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn


    def get_products():

        sql = "SELECT * FROM " + TABLE_NAME;
        args = ()
        conn = Products._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=args)
        result = cur.fetchone()
        return result


    def get_product_by_id(self, product_id):

        sql = "SELECT * FROM " + TABLE_NAME + " WHERE id=%s";
        args = (product_id)
        conn = Products._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=args)
        result = cur.fetchone()
        return result


    def add_product(self, name, description, price, inventory, image):

        sql = "INSERT INTO " + TABLE_NAME + " VALUES (%s, %s, %f, %s, %s)";
        args = (name, description, price, inventory, image)
        conn = Products._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=args)
        result = cur.fetchone()
        return result


    def update_product(self, product_id, name, description, price, inventory, image):
        
        sql = "UPDATE " + TABLE_NAME + " SET name=%s, description=%s, price=%s, inventory=%s, image=%s WHERE id=%d";
        args = (name, description, price, inventory, image, product_id)
        conn = Products._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=args)
        result = cur.fetchone()
        return result


    def delete_product(self, product_id):

        sql = "DELETE FROM " + TABLE_NAME + " WHERE id=%d";
        args = (product_id)
        conn = Products._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=args)
        result = cur.fetchone()
        return result
