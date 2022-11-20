import pymysql


class Products:

    def __int__(self):
        self.table_name = "f22_databases.product"
        self.user = "admin"
        self.password = "dbuserdbuser"
        self.host = "db1.cyl4xx6wpuab.us-east-1.rds.amazonaws.com"


    def _get_connection(self):

        conn = pymysql.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn


    def _execute(self, sql, args):
        conn = Products._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=args)
        result = cur.fetchone()
        return result


    def get_products(self):

        sql = "SELECT * FROM " + self.table_name;
        args = ()
        result = _execute(sql)

        return result


    def get_product_by_id(self, product_id):

        sql = "SELECT * FROM " + self.table_name + " WHERE id=%s";
        args = (product_id)
        result = _execute(sql, args)

        return result


    def add_product(self, name, description, price, inventory, image):

        sql = "INSERT INTO " + self.table_name + " VALUES (%s, %s, %f, %s, %s)";
        args = (name, description, price, inventory, image)
        result = _execute(sql, args)

        return result


    def update_product(self, product_id, name, description, price, inventory, image):
        
        sql = "UPDATE " + self.table_name + " SET name=%s, description=%s, price=%s, inventory=%s, image=%s WHERE id=%d";
        args = (name, description, price, inventory, image, product_id)
        result = _execute(sql, args)

        return result


    def delete_product(self, product_id):

        sql = "DELETE FROM " + self.table_name + " WHERE id=%d";
        args = (product_id)
        result = _execute(sql, args)

        return result
