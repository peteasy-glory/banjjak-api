# -*- coding: utf-8 -*-

from django.db import connection, connections

class TDB:

    def resultDBQuery(self, qryStr, database='default'):
        try:
            cursor = connections[database].cursor()
            query = qryStr
            result = cursor.execute(query)
            column = [desc[0] for desc in cursor.description]
            if result < 2:
                data = cursor.fetchone()
            else:
                data = cursor.fetchall()
            cursor.close()
            return data, result, column
        except Exception as e:
            print(e)
            return None, 0

    def closeDBAll(self):
        try:
            connections.close_all()
        except Exception as e:
            print(e)