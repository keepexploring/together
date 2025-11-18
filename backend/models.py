from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum as SQLEnum, Table
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class ImpactCategory(str, enum.Enum):
    CARBON_REDUCTION = "carbon_reduction"
    PLASTIC_REDUCTION = "plastic_reduction"
    WATER_CONSERVATION = "water_conservation"
    ECOSYSTEM_RESTORATION = "ecosystem_restoration"
    WASTE_REDUCTION = "waste_reduction"
    ENERGY_CONSERVATION = "energy_conservation"

class FrequencyType(str, enum.Enum):
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

class PledgeStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    IN_PROGRESS = "in_progress"
    MISSED = "missed"

class BadgeCategory(str, enum.Enum):
    CARBON = "carbon"
    PLASTIC = "plastic"
    WATER = "water"
    WASTE = "waste"
    ECOSYSTEM = "ecosystem"
    ENERGY = "energy"
    COMMUNITY = "community"
    COMMITMENT = "commitment"
    MILESTONE = "milestone"

class BadgeTier(str, enum.Enum):
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    DIAMOND = "diamond"

# Association table for organization members
organization_members = Table(
    'organization_members',
    Base.metadata,
    Column('organization_id', Integer, ForeignKey('organizations.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=True)  # Nullable for simple pledge users
    is_organizer = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    pledges = relationship("Pledge", back_populates="user")
    organizations_owned = relationship("Organization", back_populates="owner")
    organizations_member = relationship("Organization", secondary=organization_members, back_populates="members")
    campaign_signatures = relationship("CampaignSignature", back_populates="user")
    badges = relationship("UserBadge", back_populates="user")
    milestones = relationship("Milestone", back_populates="user")
    success_stories = relationship("SuccessStory", back_populates="user")
    photos = relationship("PledgePhoto", back_populates="user")
    activities = relationship("ActivityFeed", back_populates="user")

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    access_code = Column(String, unique=True, index=True, nullable=False)
    simple_url = Column(String, unique=True, index=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationships
    owner = relationship("User", back_populates="organizations_owned")
    members = relationship("User", secondary=organization_members, back_populates="organizations_member")
    pledges = relationship("Pledge", back_populates="organization")
    campaigns = relationship("Campaign", back_populates="organization")
    custom_actions = relationship("EnvironmentalAction", back_populates="organization")
    milestones = relationship("Milestone", back_populates="organization")
    activities = relationship("ActivityFeed", back_populates="organization")

class EnvironmentalAction(Base):
    __tablename__ = "environmental_actions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(SQLEnum(ImpactCategory), nullable=False)

    # Impact measurements (per occurrence based on frequency)
    carbon_saved_kg = Column(Float, default=0.0)  # kg CO2 equivalent
    plastic_saved_kg = Column(Float, default=0.0)  # kg of plastic
    water_saved_liters = Column(Float, default=0.0)  # liters
    trees_equivalent = Column(Float, default=0.0)  # tree planting equivalent
    ecosystem_points = Column(Float, default=0.0)  # generic ecosystem restoration points

    # Parametric action support (for customizable actions)
    is_parametric = Column(Boolean, default=False)  # Does user specify current/target?
    parameter_name = Column(String, nullable=True)  # e.g., "days_per_week", "km_per_day"
    parameter_unit = Column(String, nullable=True)  # e.g., "days/week", "km", "times/week"
    parameter_description = Column(Text, nullable=True)  # Help text for users
    base_impact_per_unit = Column(Float, default=0.0)  # Impact per unit of reduction

    # Metadata
    frequency_type = Column(SQLEnum(FrequencyType), default=FrequencyType.DAILY)
    is_global = Column(Boolean, default=True)  # Global actions vs org-specific
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    source_info = Column(Text)  # Citations for impact data

    # Relationships
    pledges = relationship("Pledge", back_populates="action")
    organization = relationship("Organization", back_populates="custom_actions")

class Pledge(Base):
    __tablename__ = "pledges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action_id = Column(Integer, ForeignKey("environmental_actions.id"))
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)

    # Pledge details
    commitment_text = Column(Text)  # Custom commitment from user
    duration_days = Column(Integer, default=30)  # How long they commit for
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)
    status = Column(SQLEnum(PledgeStatus), default=PledgeStatus.ACTIVE)

    # Parametric action values (for customizable actions)
    parameter_current_value = Column(Float, nullable=True)  # Current behavior (e.g., 5 days/week)
    parameter_target_value = Column(Float, nullable=True)  # Goal (e.g., 2 days/week)

    # Follow-up
    follow_up_frequency_days = Column(Integer, default=7)  # Check-in every N days
    last_follow_up = Column(DateTime, nullable=True)
    next_follow_up = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="pledges")
    action = relationship("EnvironmentalAction", back_populates="pledges")
    organization = relationship("Organization", back_populates="pledges")
    follow_ups = relationship("FollowUp", back_populates="pledge")
    success_stories = relationship("SuccessStory", back_populates="pledge")
    photos = relationship("PledgePhoto", back_populates="pledge")

class FollowUp(Base):
    __tablename__ = "follow_ups"

    id = Column(Integer, primary_key=True, index=True)
    pledge_id = Column(Integer, ForeignKey("pledges.id"))

    # Follow-up details
    sent_at = Column(DateTime, default=datetime.utcnow)
    responded_at = Column(DateTime, nullable=True)
    is_successful = Column(Boolean, nullable=True)  # Did they keep their pledge?
    progress_notes = Column(Text, nullable=True)

    # Relationships
    pledge = relationship("Pledge", back_populates="follow_ups")

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    goal = Column(Text, nullable=False)  # What the campaign aims to achieve

    # Campaign details
    target_signatures = Column(Integer, default=100)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    # Impact category for tracking
    primary_category = Column(SQLEnum(ImpactCategory), nullable=False)

    # Relationships
    organization = relationship("Organization", back_populates="campaigns")
    signatures = relationship("CampaignSignature", back_populates="campaign")

class CampaignSignature(Base):
    __tablename__ = "campaign_signatures"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Signature details
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    comment = Column(Text, nullable=True)
    signed_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    campaign = relationship("Campaign", back_populates="signatures")
    user = relationship("User", back_populates="campaign_signatures")

class Badge(Base):
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(SQLEnum(BadgeCategory), nullable=False)
    tier = Column(SQLEnum(BadgeTier), nullable=False)
    icon = Column(String, nullable=False)  # Icon name or emoji
    color = Column(String, default="#4CAF50")  # Hex color code

    # Criteria for earning
    criteria_type = Column(String, nullable=False)  # e.g., "carbon_saved", "pledges_completed", "streak_days"
    criteria_value = Column(Float, nullable=False)  # Threshold to achieve

    # Order and display
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    can_order_physical = Column(Boolean, default=False)  # Can user order physical version?
    physical_cost = Column(Float, default=0.0)  # Cost if orderable

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user_badges = relationship("UserBadge", back_populates="badge")

class UserBadge(Base):
    __tablename__ = "user_badges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    badge_id = Column(Integer, ForeignKey("badges.id"))

    earned_at = Column(DateTime, default=datetime.utcnow)
    progress = Column(Float, default=0.0)  # Progress towards next tier
    is_displayed = Column(Boolean, default=True)  # Show on profile?
    physical_ordered = Column(Boolean, default=False)
    physical_ordered_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="badges")
    badge = relationship("Badge", back_populates="user_badges")

class Milestone(Base):
    __tablename__ = "milestones"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)

    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    milestone_type = Column(String, nullable=False)  # e.g., "carbon_100kg", "pledge_streak_30"
    value_achieved = Column(Float, nullable=False)

    celebrated_at = Column(DateTime, default=datetime.utcnow)
    is_public = Column(Boolean, default=True)

    # Relationships
    user = relationship("User", back_populates="milestones")
    organization = relationship("Organization", back_populates="milestones")

class SuccessStory(Base):
    __tablename__ = "success_stories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    pledge_id = Column(Integer, ForeignKey("pledges.id"), nullable=True)

    title = Column(String, nullable=False)
    story = Column(Text, nullable=False)
    image_url = Column(String, nullable=True)
    impact_highlight = Column(String, nullable=True)  # e.g., "Saved 500kg CO2"

    is_featured = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=False)  # Moderation
    submitted_at = Column(DateTime, default=datetime.utcnow)
    approved_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="success_stories")
    pledge = relationship("Pledge", back_populates="success_stories")

class PledgePhoto(Base):
    __tablename__ = "pledge_photos"

    id = Column(Integer, primary_key=True, index=True)
    pledge_id = Column(Integer, ForeignKey("pledges.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    photo_url = Column(String, nullable=False)
    caption = Column(Text, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    # Peer verification
    verified_by_peers = Column(Integer, default=0)

    # Relationships
    pledge = relationship("Pledge", back_populates="photos")
    user = relationship("User", back_populates="photos")

class ActivityFeed(Base):
    __tablename__ = "activity_feed"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)

    activity_type = Column(String, nullable=False)  # "pledge_created", "badge_earned", "milestone_reached"
    activity_text = Column(String, nullable=False)  # Display text
    related_id = Column(Integer, nullable=True)  # ID of related entity (pledge_id, badge_id, etc.)

    created_at = Column(DateTime, default=datetime.utcnow)
    is_public = Column(Boolean, default=True)

    # Relationships
    user = relationship("User", back_populates="activities")
    organization = relationship("Organization", back_populates="activities")
