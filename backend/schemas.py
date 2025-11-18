from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from models import ImpactCategory, FrequencyType, PledgeStatus

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: Optional[str] = None

class User(UserBase):
    id: int
    is_organizer: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Organization Schemas
class OrganizationBase(BaseModel):
    name: str
    description: Optional[str] = None

class OrganizationCreate(OrganizationBase):
    pass

class Organization(OrganizationBase):
    id: int
    access_code: str
    simple_url: str
    owner_id: int
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

# Environmental Action Schemas
class EnvironmentalActionBase(BaseModel):
    title: str
    description: str
    category: ImpactCategory
    carbon_saved_kg: float = 0.0
    plastic_saved_kg: float = 0.0
    water_saved_liters: float = 0.0
    trees_equivalent: float = 0.0
    ecosystem_points: float = 0.0
    frequency_type: FrequencyType = FrequencyType.DAILY
    source_info: Optional[str] = None

class EnvironmentalActionCreate(EnvironmentalActionBase):
    organization_id: Optional[int] = None

class EnvironmentalAction(EnvironmentalActionBase):
    id: int
    is_global: bool
    organization_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Pledge Schemas
class PledgeBase(BaseModel):
    action_id: int
    commitment_text: Optional[str] = None
    duration_days: int = 30
    follow_up_frequency_days: int = 7

class PledgeCreate(PledgeBase):
    organization_id: Optional[int] = None
    user_email: EmailStr
    user_name: str

class Pledge(PledgeBase):
    id: int
    user_id: int
    organization_id: Optional[int] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    status: PledgeStatus
    last_follow_up: Optional[datetime] = None
    next_follow_up: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class PledgeWithDetails(Pledge):
    action: EnvironmentalAction
    user: User

    class Config:
        from_attributes = True

# Follow-up Schemas
class FollowUpBase(BaseModel):
    is_successful: Optional[bool] = None
    progress_notes: Optional[str] = None

class FollowUpCreate(FollowUpBase):
    pledge_id: int

class FollowUp(FollowUpBase):
    id: int
    pledge_id: int
    sent_at: datetime
    responded_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Campaign Schemas
class CampaignBase(BaseModel):
    title: str
    description: str
    goal: str
    primary_category: ImpactCategory
    target_signatures: int = 100
    end_date: Optional[datetime] = None

class CampaignCreate(CampaignBase):
    organization_id: Optional[int] = None

class Campaign(CampaignBase):
    id: int
    organization_id: Optional[int] = None
    created_by_id: int
    created_at: datetime
    is_active: bool
    signature_count: int = 0

    class Config:
        from_attributes = True

# Campaign Signature Schemas
class CampaignSignatureBase(BaseModel):
    name: str
    email: EmailStr
    comment: Optional[str] = None

class CampaignSignatureCreate(CampaignSignatureBase):
    campaign_id: int

class CampaignSignature(CampaignSignatureBase):
    id: int
    campaign_id: int
    user_id: Optional[int] = None
    signed_at: datetime

    class Config:
        from_attributes = True

# Impact Summary Schema
class ImpactSummary(BaseModel):
    total_carbon_saved_kg: float
    total_plastic_saved_kg: float
    total_water_saved_liters: float
    total_trees_equivalent: float
    total_ecosystem_points: float
    total_pledges: int
    active_pledges: int
    completed_pledges: int
    total_participants: int

class OrganizationImpact(ImpactSummary):
    organization_id: int
    organization_name: str

# Simple Pledge Entry (for event codes)
class SimplePledgeEntry(BaseModel):
    access_code: str
    user_name: str
    user_email: EmailStr
    action_id: int
    commitment_text: Optional[str] = None
    duration_days: int = 30
