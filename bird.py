from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
 
Base = declarative_base()
 
class Bird(Base):
   __tablename__ = 'birds'
   id = Column(String(100), primary_key=True)
   name = Column(String(100))
   image = Column(String(100))
   description = Column(String())
   life_history = Column(String())
   distribution_and_habitat = Column(String())
   status = Column(String())
   management_and_research_needs = Column(String())
   locations = Column(String())
 
   def __repr__(self):
       return "<Bird(id='%s', name='%s', description='%s')>" % (self.id, self.name, self.description)
 
