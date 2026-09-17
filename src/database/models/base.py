from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship 
from sqlalchemy import ForeignKey, UniqueConstraint

import datetime

class Base(DeclarativeBase):
    pass 


