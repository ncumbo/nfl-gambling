#database
from dataclasses import dataclass
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Team_Trends1(Base):  #All 32 teams will have row entries
    __tablename__ = 'team'
    teamname = Column(String)
    SU_win = Column(Integer)
    SU_loss = Column(Integer)
    spread_win = Column(Integer)
    spread_loss = Column(Integer)
    over = Column(Integer)
    under = Column(Integer)

# class teams:
#     ARI: str
#     ATL: str
#     BAL: str
#     BUF: str
#     CAR: str
#     CIN: str
#     CHI: str
#     CLE: str
#     DAL: str
#     DEN: str
#     DET: str
#     GNB: str
#     HOU: str
#     IND: str
#     KAN: str
#     LAC: str
#     LAR: str
#     JAX: str
#     MIA: str
#     MIN: str
#     NWE: str
#     NOR: str
#     NYG: str
#     NYJ: str
#     OAK: str
#     PHI: str
#     SFO: str
#     SEA: str
#     PIT: str
#     TAM: str
#     TEN: str
#     WSH: str