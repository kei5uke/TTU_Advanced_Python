from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Time
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime
import os


"""
1. Create SQLite database DINERS, with two related tables CANTEEN and PROVIDER
Table CANTEEN fields: ID, ProviderID, Name, Location,  time_open, time_closed (weekday doesn't matter).
Table Provider fields: ID, ProviderName.
"""
# Initialize the db file
if os.path.exists("part_b.db"):
    os.remove("part_b.db")
# Create engine obj
engine = create_engine('sqlite:///part_b.db', echo=False)
# Create base
Base = declarative_base()

# Create table structures


class PROVIDER(Base):
    __tablename__ = 'PROVIDER'
    ID = Column(Integer, primary_key=True)
    ProviderName = Column(String)
    Canteen = relationship("CANTEEN", back_populates="Provider")


class CANTEEN(Base):
    __tablename__ = 'CANTEEN'
    ID = Column(Integer, primary_key=True)
    ProviderID = Column(Integer, ForeignKey('PROVIDER.ID'))
    Provider = relationship("PROVIDER", back_populates="Canteen")
    Name = Column(String)
    Location = Column(String)
    time_open = Column(Time)
    time_closed = Column(Time)


Base.metadata.create_all(engine)

# Create session
make = sessionmaker(bind=engine)
session = make()

"""
2. Insert IT College canteen data by separate statement, other canteens as one list.
"""
# Create IT college provider data
prov_obj = PROVIDER()
prov_obj.ID = 1
prov_obj.ProviderName = 'bitStop Kohvik OÜ'
# Create IT college canteen data
canteen_obj = CANTEEN()
canteen_obj.ID = 1
canteen_obj.Name = 'bitStop Kohvik'
canteen_obj.Location = 'IT College, Raja 4c'
canteen_obj.time_open = datetime.time(9, 30, 0)
canteen_obj.time_closed = datetime.time(16, 0, 0)
canteen_obj.ProviderID = 1

session.add(prov_obj)
session.add(canteen_obj)

# Others
# Create provider list
provider_list = ["Rahva Toit",
                 "Baltic Restaurants Estonia AS",
                 "TTÜ Sport OÜ"
                 ]
count = 2
for i in range(len(provider_list)):
    prov_obj = PROVIDER()
    prov_obj.ID = count + i
    prov_obj.ProviderName = provider_list[i]
    session.add(prov_obj)

# Update providerID dict
providerID = {}
for r in session.query(PROVIDER):
    providerID.update({r.ProviderName: r.ID})

# Create canteens list
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
                  None,
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

# Insert canteens
count = 2
for q in canteens_list:
    canteen_obj = CANTEEN()
    canteen_obj.ID = count
    canteen_obj.Name = q[0]
    canteen_obj.Location = q[1]
    canteen_obj.time_open = datetime.datetime.strptime(q[2], '%H:%M').time()
    canteen_obj.time_closed = datetime.datetime.strptime(q[3], '%H:%M').time()
    canteen_obj.ProviderID = providerID.get(q[4])
    session.add(canteen_obj)
    count += 1


print("PROVIDER")
for r in session.query(PROVIDER):
    print(r.ID, r.ProviderName)
print("---")

print("CANTEEN")
for r in session.query(CANTEEN):
    print(r.ID, r.ProviderID, r.Name, r.Location, r.time_open, r.time_closed)
print("---")


"""
3. Create query for canteens which are open 16.15-18.00
"""
print("Canteens which are open 16:15 - 18:00")
query = session.query(CANTEEN).filter(
    CANTEEN.time_open < datetime.time(16, 15, 00),
    CANTEEN.time_closed > datetime.time(18, 00, 00))
for r in query:
    print(r.Name)
print("---")


"""
4. Create query for canteens which are serviced by Rahva Toit.
NB! Create query by string "Rahva Toit" not by direct ID!.
"""
print("Canteens which are serviced by Rahva Toit")
query = session.query(CANTEEN).join(
    PROVIDER, CANTEEN.ProviderID == PROVIDER.ID).filter(
    PROVIDER.ProviderName == "Rahva Toit")
for r in query:
    print(r.Name)
print("---")

session.commit()
