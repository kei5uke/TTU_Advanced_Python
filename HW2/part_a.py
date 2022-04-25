import sqlite3 as sql


def main():
    """
    1. Create SQLite database DINERS, with two related tables CANTEEN and PROVIDER
    Table CANTEEN fields:
        ID, ProviderID, Name, Location, time_open, time_closed (weekday doesn't matter).
    Table Provider fields:
        ID, ProviderName.
    """
    # Connect to database DINERS
    connection = sql.connect('part_a.db')
    curser = connection

    # Create table PROVIDER
    curser.execute("drop table if exists provider")
    query = """ create table PROVIDER (
        ID integer primary key autoincrement,
        ProviderName text
    );
    """
    curser.execute(query)

    # Create table CANTEEN
    curser.execute("drop table if exists canteen")
    query = """ create table CANTEEN (
        ID integer primary key autoincrement,
        providerID integer,
        Name text,
        Location text,
        time_open time,
        time_closed time,
        foreign key (providerID)
            references provider (ID)
            on delete set null
    );
    """
    curser.execute(query)

    """
    2. Insert IT College canteen data by separate statement, other canteens as one list.
    """
    # Insert IT college provider data
    query = """ insert into PROVIDER(ProviderName)
    values ('bitStop Kohvik OÜ');
    """
    curser.execute(query)

    # Insert IT college canteen data
    query = """ insert into CANTEEN(providerID, Name, Location, time_open, time_closed)
    values (1,'bitStop KOHVIK', 'IT College, Raja 4c', '09:30', '16:00');
    """
    curser.execute(query)

    # Insert others as a list
    provider_list = ["Rahva Toit",
                     "Baltic Restaurants Estonia AS",
                     "TTÜ Sport OÜ"
                     ]
    canteens_list = [("Economics- and social science building canteen",
                      "Akadeemia tee 3 SOC- building",
                      "08:30",
                      "18:30",
                      "Rahva Toit"),
                     ("Library canteen",
                      "Akadeemia tee 1/Ehitajate tee 7",
                      "08:30",
                      "19:00",
                      "Rahva Toit"),
                     ("Main building Deli cafe",
                      "Ehitajate tee 5 U01 building",
                      "09:00",
                      "16:30",
                      "Baltic Restaurants Estonia AS"),
                     ("Main building Daily lunch restaurant",
                      "Ehitajate tee 5 U01 building",
                      "09:00",
                      "16:00",
                      "Baltic Restaurants Estonia AS"),
                     ("U06 building canteen",
                      "NULL",
                      "09:00",
                      "16:00",
                      "Rahva Toit"),
                     ("Natural Science building canteen",
                      "Akadeemia tee 15 SCI building",
                      "09:00",
                      "16:00",
                      "Baltic Restaurants Estonia AS"),
                     ("ICT building canteen",
                      "Raja 15/Mäepealse 1",
                      "09:00",
                      "16:00",
                      "Baltic Restaurants Estonia AS"),
                     ("Sports building canteen",
                      "Männiliiva 7 S01 building",
                      "11:00",
                      "20:00",
                      "TTÜ Sport OÜ")]

    # Insert providers
    format_str = """ insert into PROVIDER (ProviderName) values ('{name}'); """
    for i in range(len(provider_list)):
        sql_command = format_str.format(name=provider_list[i])
        curser.execute(sql_command)

    # Update providerID dict
    providerID = {}
    query = """ select * from PROVIDER; """
    output = curser.execute(query).fetchall()
    for row in output:
        providerID.update({row[1]: row[0]})

    # Insert canteens
    format_str = """ insert into CANTEEN ({prov_id_str} Name, Location, time_open, time_closed)
        values ({prov_id} '{name}', {location}, {time_open}, {time_closed});
        """
    for q in canteens_list:
        tmp = providerID.get(q[4])
        sql_command = format_str.format(prov_id_str="providerID," if tmp is not None else "",
                                        prov_id=str(tmp) + ',' if tmp is not None else "",
                                        name=q[0],
                                        location="'" + str(q[1]) + "'" if q[1] != "NULL" else "NULL",
                                        time_open="'" + str(q[2]) + "'" if q[2] != "NULL" else "NULL",
                                        time_closed="'" + str(q[3]) + "'" if q[3] != "NULL" else "NULL")
        curser.execute(sql_command)

    print("CANTEEN TABLE")
    output = curser.execute(""" select * from CANTEEN; """).fetchall()
    for row in output:
        print(row)
    print("---")
    print("PRIOVIDER TABLE")
    output = curser.execute(""" select * from PROVIDER; """).fetchall()
    for row in output:
        print(row)
    print("---")

    """
    3. Create query for canteens which are open 16.15-18.00
    """
    print("Canteens which are open 16:15 - 18:00")
    query = """
    select Name from CANTEEN where
    time_open < "16:15:00" and time_closed > "18:00:00";
    """
    output = curser.execute(query).fetchall()
    for row in output:
        print(row)
    print("---")

    """
    4. Create query for canteens which are serviced by Rahva Toit.
    NB! Create query by string "Rahva Toit" not by direct ID!.
    """
    print("Canteens which are serviced by Rahva Toit")
    query = """
    select CANTEEN.name from CANTEEN inner join PROVIDER on CANTEEN.providerID = PROVIDER.id
    where PROVIDER.providerName == 'Rahva Toit'
    """
    output = curser.execute(query).fetchall()
    for row in output:
        print(row)
    print("---")

    connection.commit()
    connection.close()


if __name__ == "__main__":
    main()
