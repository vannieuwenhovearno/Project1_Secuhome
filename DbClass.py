class DbClass:
    def __init__(self):
        import mysql.connector as connector

        self.__dsn = {
            "host": "localhost",
            "user": "Arno",
            "passwd": "",
            "db": "db_project_secuhome"
        }

        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()


    def getUser(self, mail):
        # Query met parameters
        sqlQuery = "SELECT * FROM gebruikers WHERE Email = '{email}'"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(email=mail)

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def setNewUser(self, fullname, mail, Password):
        # Query met parameters
        sqlQuery = "INSERT INTO gebruikers (NaamVoornaam,Email,Wachtwoord) VALUES ('{fullname}','{mail}','{passw}')"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(fullname=fullname, mail=mail, passw=Password)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def getNameLights(self):
        # Query zonder parameters
        sqlQuery = "SELECT * FROM lichtenbinnen"

        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def getNameMusic(self):
        sqlQuery = "SELECT * FROM muziek"

        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def getNameWering(self):
        # Query zonder parameters
        sqlQuery = "SELECT * FROM zonnewering"

        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def getnameLightOUT(self):
        sqlQuery = "SELECT * FROM ldr"

        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def setZonnewering(self, beneden, wering, systeem):
        sqlQuery = "INSERT INTO datazonnewering(DatumIN, TijdIN, WeringBeneden, Zonnewering, Systeem) VALUES ( CURDATE() ,CURTIME() ,'{param3}','{param4}','{param5}')"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(param3=beneden,param4=wering,param5=systeem)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def setBinnenverlichting(self,aan, licht, systeem):
        sqlQuery = "INSERT INTO datalichtin (DatumIN, TijdIN, Aan, LichtBinnen, Systeem) VALUES (CURDATE(), CURTIME(),'{param3}','{param4}','{param5}')"
        sqlCommand = sqlQuery.format(param3=aan, param4=licht, param5=systeem)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def setBuitenverlichting(self, aan,lichtbuiten,systeem):
        sqlQuery = "INSERT INTO datalichtout (DatumIN,TijdIN,Aan,lichtenbuiten_IDLichtenbuiten, systeem_IDSysteem) VALUES (CURDATE(), CURTIME(),'{param3}','{param4}','{param5}')"
        sqlCommand = sqlQuery.format(param3=aan, param4=lichtbuiten,param5=systeem)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def setMuziek(self,aan, muziek,systeem):
        sqlQuery ="INSERT INTO datamuziek(DatumIN,TijdIN,Aan,Muziek,Systeem) VALUES (CURDATE(), CURTIME(),'{param3}','{param4}','{param5}')"
        sqlCommand = sqlQuery.format(param3=aan,param4=muziek,param5=systeem)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def getDataLichtIN(self):
        sqlQuery = "SELECT L.Beschrijving, Count(D.IDDataLichtIN) AS 'aantal' FROM datalichtin AS D JOIN lichtenbinnen AS L ON D.LichtBinnen = L.IDLichtenBinnen GROUP BY L.Beschrijving;"

        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def getDataMuziekGraph(self):
        sqlQuery = "SELECT M.Beschrijving, Count(I.IDDataMuziek) AS 'aantal' FROM datamuziek AS I JOIN muziek AS M on I.Muziek = M.IDMuziek GROUP BY M.Beschrijving;"

        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def getDataZon(self):
        sqlQuery = "SELECT Z.Beschrijving, Count(D.IDDataZon) AS 'aantal' FROM datazonnewering AS D JOIN zonnewering AS Z ON D.Zonnewering = Z.IDZonnewering GROUP BY Z.Beschrijving"

        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def getDataMuziek(self):
        sqlQuery = "SELECT * FROM datamuziek WHERE DatumIN=CURDATE();"

        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def toevoegenContact(self,naam,email,onderwerp,bericht):
        # Query met parameters
        sqlQuery = "INSERT INTO contact(Naam,Email,Onderwerp,Bericht) VALUES('{naam}','{mail}','{onderwerp}','{bericht}')"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(naam=naam, mail=email, onderwerp=onderwerp, bericht=bericht)
        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

