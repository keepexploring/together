from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import datetime, timedelta
import secrets
import string

from database import get_db, init_db
from models import (
    User, Organization, EnvironmentalAction, Pledge, FollowUp,
    Campaign, CampaignSignature, ImpactCategory, PledgeStatus, organization_members,
    Badge, UserBadge, Milestone, SuccessStory, PledgePhoto, ActivityFeed,
    BadgeCategory, BadgeTier
)
import schemas
from seed_data import ENVIRONMENTAL_ACTIONS
from badge_seed_data import BADGES

app = FastAPI(
    title="Planet Pledge API",
    description="API for environmental pledge tracking and impact calculation",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event to initialize database
@app.on_event("startup")
async def startup_event():
    await init_db()
    async for db in get_db():
        # Seed environmental actions if database is empty
        result = await db.execute(select(EnvironmentalAction).where(EnvironmentalAction.is_global == True))
        if not result.scalars().first():
            for action_data in ENVIRONMENTAL_ACTIONS:
                action = EnvironmentalAction(**action_data, is_global=True)
                db.add(action)
            await db.commit()

        # Seed badges if database is empty
        result = await db.execute(select(Badge))
        if not result.scalars().first():
            for badge_data in BADGES:
                badge = Badge(**badge_data)
                db.add(badge)
            await db.commit()
        break

# Utility functions
def generate_access_code(length: int = 6) -> str:
    """Generate a random access code"""
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def generate_simple_url(name: str) -> str:
    """Generate a simple URL from organization name"""
    return name.lower().replace(' ', '-').replace('_', '-')[:30]

# ==================== USER ENDPOINTS ====================

@app.post("/api/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    """Create a new user (simplified - no password hashing for pledge-only users)"""
    # Check if user exists
    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalars().first()
    if existing_user:
        return existing_user

    db_user = User(
        email=user.email,
        name=user.name,
        hashed_password=user.password,  # In production, hash this properly
        is_organizer=False
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@app.get("/api/users/{user_id}", response_model=schemas.User)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get user by ID"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ==================== ORGANIZATION ENDPOINTS ====================

@app.post("/api/organizations/", response_model=schemas.Organization, status_code=status.HTTP_201_CREATED)
async def create_organization(
    org: schemas.OrganizationCreate,
    owner_email: str,
    db: AsyncSession = Depends(get_db)
):
    """Create a new organization"""
    # Get or create owner
    result = await db.execute(select(User).where(User.email == owner_email))
    owner = result.scalars().first()

    if not owner:
        raise HTTPException(status_code=404, detail="Owner user not found. Create user first.")

    # Update user to be organizer
    owner.is_organizer = True

    # Generate unique access code and URL
    access_code = generate_access_code()
    simple_url = generate_simple_url(org.name)

    # Ensure uniqueness
    counter = 1
    original_url = simple_url
    while True:
        result = await db.execute(
            select(Organization).where(Organization.simple_url == simple_url)
        )
        if not result.scalars().first():
            break
        simple_url = f"{original_url}-{counter}"
        counter += 1

    db_org = Organization(
        name=org.name,
        description=org.description,
        access_code=access_code,
        simple_url=simple_url,
        owner_id=owner.id
    )
    db.add(db_org)
    await db.commit()
    await db.refresh(db_org)
    return db_org

@app.get("/api/organizations/", response_model=List[schemas.Organization])
async def list_organizations(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """List all organizations"""
    result = await db.execute(select(Organization).offset(skip).limit(limit))
    return result.scalars().all()

@app.get("/api/organizations/{org_id}", response_model=schemas.Organization)
async def get_organization(org_id: int, db: AsyncSession = Depends(get_db)):
    """Get organization by ID"""
    result = await db.execute(select(Organization).where(Organization.id == org_id))
    org = result.scalars().first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

@app.get("/api/organizations/code/{access_code}", response_model=schemas.Organization)
async def get_organization_by_code(access_code: str, db: AsyncSession = Depends(get_db)):
    """Get organization by access code"""
    result = await db.execute(
        select(Organization).where(Organization.access_code == access_code.upper())
    )
    org = result.scalars().first()
    if not org:
        raise HTTPException(status_code=404, detail="Invalid access code")
    return org

@app.get("/api/organizations/url/{simple_url}", response_model=schemas.Organization)
async def get_organization_by_url(simple_url: str, db: AsyncSession = Depends(get_db)):
    """Get organization by simple URL"""
    result = await db.execute(
        select(Organization).where(Organization.simple_url == simple_url)
    )
    org = result.scalars().first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

# ==================== ENVIRONMENTAL ACTION ENDPOINTS ====================

@app.get("/api/actions/", response_model=List[schemas.EnvironmentalAction])
async def list_actions(
    category: Optional[ImpactCategory] = None,
    organization_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """List environmental actions, optionally filtered by category or organization"""
    query = select(EnvironmentalAction)

    if category:
        query = query.where(EnvironmentalAction.category == category)

    if organization_id:
        query = query.where(
            (EnvironmentalAction.is_global == True) |
            (EnvironmentalAction.organization_id == organization_id)
        )
    else:
        query = query.where(EnvironmentalAction.is_global == True)

    result = await db.execute(query)
    return result.scalars().all()

@app.get("/api/actions/{action_id}", response_model=schemas.EnvironmentalAction)
async def get_action(action_id: int, db: AsyncSession = Depends(get_db)):
    """Get specific environmental action"""
    result = await db.execute(select(EnvironmentalAction).where(EnvironmentalAction.id == action_id))
    action = result.scalars().first()
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    return action

@app.post("/api/actions/", response_model=schemas.EnvironmentalAction, status_code=status.HTTP_201_CREATED)
async def create_action(
    action: schemas.EnvironmentalActionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new custom environmental action (for organizers)"""
    db_action = EnvironmentalAction(
        **action.dict(),
        is_global=False if action.organization_id else True
    )
    db.add(db_action)
    await db.commit()
    await db.refresh(db_action)
    return db_action

# ==================== PLEDGE ENDPOINTS ====================

@app.post("/api/pledges/", response_model=schemas.Pledge, status_code=status.HTTP_201_CREATED)
async def create_pledge(pledge: schemas.PledgeCreate, db: AsyncSession = Depends(get_db)):
    """Create a new pledge"""
    # Get or create user
    result = await db.execute(select(User).where(User.email == pledge.user_email))
    user = result.scalars().first()

    if not user:
        user = User(email=pledge.user_email, name=pledge.user_name)
        db.add(user)
        await db.flush()

    # Verify action exists
    result = await db.execute(select(EnvironmentalAction).where(EnvironmentalAction.id == pledge.action_id))
    action = result.scalars().first()
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")

    # Calculate dates
    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=pledge.duration_days)
    next_follow_up = start_date + timedelta(days=pledge.follow_up_frequency_days)

    db_pledge = Pledge(
        user_id=user.id,
        action_id=pledge.action_id,
        organization_id=pledge.organization_id,
        commitment_text=pledge.commitment_text,
        duration_days=pledge.duration_days,
        start_date=start_date,
        end_date=end_date,
        follow_up_frequency_days=pledge.follow_up_frequency_days,
        next_follow_up=next_follow_up,
        parameter_current_value=pledge.parameter_current_value,
        parameter_target_value=pledge.parameter_target_value,
        status=PledgeStatus.ACTIVE
    )
    db.add(db_pledge)
    await db.commit()
    await db.refresh(db_pledge)

    # Create activity feed entry
    activity = ActivityFeed(
        user_id=user.id,
        organization_id=pledge.organization_id,
        activity_type="pledge_created",
        activity_text=f"Made a new pledge: {action.title}",
        related_id=db_pledge.id,
        is_public=True
    )
    db.add(activity)
    await db.commit()

    # Check and award badges
    await award_badges_for_user(db, user.id)

    return db_pledge

@app.post("/api/pledges/simple", response_model=schemas.Pledge, status_code=status.HTTP_201_CREATED)
async def create_simple_pledge(pledge: schemas.SimplePledgeEntry, db: AsyncSession = Depends(get_db)):
    """Create a pledge using simple access code (for events)"""
    # Verify organization
    result = await db.execute(
        select(Organization).where(Organization.access_code == pledge.access_code.upper())
    )
    org = result.scalars().first()
    if not org:
        raise HTTPException(status_code=404, detail="Invalid access code")

    # Create pledge
    pledge_create = schemas.PledgeCreate(
        user_email=pledge.user_email,
        user_name=pledge.user_name,
        action_id=pledge.action_id,
        organization_id=org.id,
        commitment_text=pledge.commitment_text,
        duration_days=pledge.duration_days
    )
    return await create_pledge(pledge_create, db)

@app.get("/api/pledges/", response_model=List[schemas.PledgeWithDetails])
async def list_pledges(
    organization_id: Optional[int] = None,
    user_id: Optional[int] = None,
    status_filter: Optional[PledgeStatus] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List pledges with filters"""
    query = select(Pledge).options(
        selectinload(Pledge.action),
        selectinload(Pledge.user)
    )

    if organization_id:
        query = query.where(Pledge.organization_id == organization_id)
    if user_id:
        query = query.where(Pledge.user_id == user_id)
    if status_filter:
        query = query.where(Pledge.status == status_filter)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@app.get("/api/pledges/{pledge_id}", response_model=schemas.PledgeWithDetails)
async def get_pledge(pledge_id: int, db: AsyncSession = Depends(get_db)):
    """Get specific pledge"""
    result = await db.execute(
        select(Pledge)
        .options(selectinload(Pledge.action), selectinload(Pledge.user))
        .where(Pledge.id == pledge_id)
    )
    pledge = result.scalars().first()
    if not pledge:
        raise HTTPException(status_code=404, detail="Pledge not found")
    return pledge

@app.patch("/api/pledges/{pledge_id}/status")
async def update_pledge_status(
    pledge_id: int,
    status_update: PledgeStatus,
    db: AsyncSession = Depends(get_db)
):
    """Update pledge status"""
    result = await db.execute(
        select(Pledge).options(selectinload(Pledge.action)).where(Pledge.id == pledge_id)
    )
    pledge = result.scalars().first()
    if not pledge:
        raise HTTPException(status_code=404, detail="Pledge not found")

    old_status = pledge.status
    pledge.status = status_update
    await db.commit()
    await db.refresh(pledge)

    # Create activity feed entry for completed pledges
    if status_update == PledgeStatus.COMPLETED and old_status != PledgeStatus.COMPLETED:
        activity = ActivityFeed(
            user_id=pledge.user_id,
            organization_id=pledge.organization_id,
            activity_type="pledge_completed",
            activity_text=f"Completed pledge: {pledge.action.title}",
            related_id=pledge.id,
            is_public=True
        )
        db.add(activity)
        await db.commit()

        # Check and award badges
        await award_badges_for_user(db, pledge.user_id)

    return pledge

# ==================== FOLLOW-UP ENDPOINTS ====================

@app.post("/api/follow-ups/", response_model=schemas.FollowUp, status_code=status.HTTP_201_CREATED)
async def create_follow_up(follow_up: schemas.FollowUpCreate, db: AsyncSession = Depends(get_db)):
    """Record a follow-up check-in"""
    db_follow_up = FollowUp(**follow_up.dict())
    db.add(db_follow_up)

    # Update pledge last_follow_up and next_follow_up
    result = await db.execute(select(Pledge).where(Pledge.id == follow_up.pledge_id))
    pledge = result.scalars().first()
    if pledge:
        pledge.last_follow_up = datetime.utcnow()
        pledge.next_follow_up = datetime.utcnow() + timedelta(days=pledge.follow_up_frequency_days)

        # Update status based on follow-up
        if follow_up.is_successful is False:
            pledge.status = PledgeStatus.MISSED

    await db.commit()
    await db.refresh(db_follow_up)
    return db_follow_up

@app.get("/api/pledges/{pledge_id}/follow-ups", response_model=List[schemas.FollowUp])
async def get_pledge_follow_ups(pledge_id: int, db: AsyncSession = Depends(get_db)):
    """Get all follow-ups for a pledge"""
    result = await db.execute(
        select(FollowUp).where(FollowUp.pledge_id == pledge_id).order_by(FollowUp.sent_at.desc())
    )
    return result.scalars().all()

# ==================== IMPACT CALCULATION ENDPOINTS ====================

@app.get("/api/impact/global", response_model=schemas.ImpactSummary)
async def get_global_impact(db: AsyncSession = Depends(get_db)):
    """Calculate total global impact from all pledges"""
    return await calculate_impact(db)

@app.get("/api/impact/organization/{org_id}", response_model=schemas.OrganizationImpact)
async def get_organization_impact(org_id: int, db: AsyncSession = Depends(get_db)):
    """Calculate impact for a specific organization"""
    result = await db.execute(select(Organization).where(Organization.id == org_id))
    org = result.scalars().first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    impact = await calculate_impact(db, org_id)
    return schemas.OrganizationImpact(
        organization_id=org_id,
        organization_name=org.name,
        **impact.dict()
    )

async def calculate_impact(db: AsyncSession, organization_id: Optional[int] = None) -> schemas.ImpactSummary:
    """Helper function to calculate impact"""
    query = select(Pledge).options(selectinload(Pledge.action))

    if organization_id:
        query = query.where(Pledge.organization_id == organization_id)

    result = await db.execute(query)
    pledges = result.scalars().all()

    total_carbon = 0.0
    total_plastic = 0.0
    total_water = 0.0
    total_trees = 0.0
    total_ecosystem = 0.0
    active_count = 0
    completed_count = 0

    for pledge in pledges:
        # Handle parametric actions
        if pledge.action.is_parametric and pledge.parameter_current_value is not None and pledge.parameter_target_value is not None:
            # Calculate impact based on reduction amount (current - target) * base_impact_per_unit
            reduction = pledge.parameter_current_value - pledge.parameter_target_value
            if reduction > 0:  # Only count if it's actually a reduction
                # For parametric actions, multiply by duration factor
                duration_factor = pledge.duration_days / 365.0
                total_carbon += pledge.action.base_impact_per_unit * reduction * duration_factor
                # Parametric actions primarily affect carbon; could extend to other metrics if needed
        else:
            # Standard non-parametric actions
            multiplier = pledge.duration_days / 365.0  # Convert to yearly fraction

            if pledge.action.frequency_type.value == "daily":
                multiplier *= 365
            elif pledge.action.frequency_type.value == "weekly":
                multiplier *= 52
            elif pledge.action.frequency_type.value == "monthly":
                multiplier *= 12
            elif pledge.action.frequency_type.value == "once":
                multiplier = 1

            total_carbon += pledge.action.carbon_saved_kg * multiplier
            total_plastic += pledge.action.plastic_saved_kg * multiplier
            total_water += pledge.action.water_saved_liters * multiplier
            total_trees += pledge.action.trees_equivalent * multiplier
            total_ecosystem += pledge.action.ecosystem_points * multiplier

        if pledge.status == PledgeStatus.ACTIVE or pledge.status == PledgeStatus.IN_PROGRESS:
            active_count += 1
        elif pledge.status == PledgeStatus.COMPLETED:
            completed_count += 1

    # Count unique users
    user_query = select(func.count(func.distinct(Pledge.user_id)))
    if organization_id:
        user_query = user_query.where(Pledge.organization_id == organization_id)

    user_result = await db.execute(user_query)
    total_participants = user_result.scalar()

    return schemas.ImpactSummary(
        total_carbon_saved_kg=round(total_carbon, 2),
        total_plastic_saved_kg=round(total_plastic, 2),
        total_water_saved_liters=round(total_water, 2),
        total_trees_equivalent=round(total_trees, 2),
        total_ecosystem_points=round(total_ecosystem, 2),
        total_pledges=len(pledges),
        active_pledges=active_count,
        completed_pledges=completed_count,
        total_participants=total_participants or 0
    )

# ==================== CAMPAIGN ENDPOINTS ====================

@app.post("/api/campaigns/", response_model=schemas.Campaign, status_code=status.HTTP_201_CREATED)
async def create_campaign(
    campaign: schemas.CampaignCreate,
    creator_email: str,
    db: AsyncSession = Depends(get_db)
):
    """Create a new environmental campaign"""
    # Get creator
    result = await db.execute(select(User).where(User.email == creator_email))
    creator = result.scalars().first()
    if not creator:
        raise HTTPException(status_code=404, detail="Creator user not found")

    db_campaign = Campaign(
        **campaign.dict(),
        created_by_id=creator.id
    )
    db.add(db_campaign)
    await db.commit()
    await db.refresh(db_campaign)
    return db_campaign

@app.get("/api/campaigns/", response_model=List[schemas.Campaign])
async def list_campaigns(
    organization_id: Optional[int] = None,
    is_active: bool = True,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List campaigns"""
    query = select(Campaign)

    if organization_id:
        query = query.where(Campaign.organization_id == organization_id)
    if is_active is not None:
        query = query.where(Campaign.is_active == is_active)

    query = query.offset(skip).limit(limit).order_by(Campaign.created_at.desc())
    result = await db.execute(query)
    campaigns = result.scalars().all()

    # Add signature count
    campaign_list = []
    for campaign in campaigns:
        sig_result = await db.execute(
            select(func.count(CampaignSignature.id)).where(CampaignSignature.campaign_id == campaign.id)
        )
        sig_count = sig_result.scalar()

        campaign_dict = schemas.Campaign.from_orm(campaign).dict()
        campaign_dict['signature_count'] = sig_count
        campaign_list.append(schemas.Campaign(**campaign_dict))

    return campaign_list

@app.get("/api/campaigns/{campaign_id}", response_model=schemas.Campaign)
async def get_campaign(campaign_id: int, db: AsyncSession = Depends(get_db)):
    """Get specific campaign with signature count"""
    result = await db.execute(select(Campaign).where(Campaign.id == campaign_id))
    campaign = result.scalars().first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    # Get signature count
    sig_result = await db.execute(
        select(func.count(CampaignSignature.id)).where(CampaignSignature.campaign_id == campaign_id)
    )
    sig_count = sig_result.scalar()

    campaign_dict = schemas.Campaign.from_orm(campaign).dict()
    campaign_dict['signature_count'] = sig_count
    return schemas.Campaign(**campaign_dict)

@app.post("/api/campaigns/{campaign_id}/sign", response_model=schemas.CampaignSignature, status_code=status.HTTP_201_CREATED)
async def sign_campaign(
    campaign_id: int,
    signature: schemas.CampaignSignatureBase,
    db: AsyncSession = Depends(get_db)
):
    """Sign a campaign"""
    # Verify campaign exists
    result = await db.execute(select(Campaign).where(Campaign.id == campaign_id))
    campaign = result.scalars().first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    if not campaign.is_active:
        raise HTTPException(status_code=400, detail="Campaign is not active")

    # Check if already signed
    result = await db.execute(
        select(CampaignSignature).where(
            and_(
                CampaignSignature.campaign_id == campaign_id,
                CampaignSignature.email == signature.email
            )
        )
    )
    existing = result.scalars().first()
    if existing:
        raise HTTPException(status_code=400, detail="You have already signed this campaign")

    # Get or create user
    result = await db.execute(select(User).where(User.email == signature.email))
    user = result.scalars().first()

    db_signature = CampaignSignature(
        campaign_id=campaign_id,
        user_id=user.id if user else None,
        **signature.dict()
    )
    db.add(db_signature)
    await db.commit()
    await db.refresh(db_signature)
    return db_signature

@app.get("/api/campaigns/{campaign_id}/signatures", response_model=List[schemas.CampaignSignature])
async def get_campaign_signatures(
    campaign_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get signatures for a campaign"""
    result = await db.execute(
        select(CampaignSignature)
        .where(CampaignSignature.campaign_id == campaign_id)
        .order_by(CampaignSignature.signed_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

# ==================== BADGE ENDPOINTS ====================

@app.get("/api/badges/", response_model=List[schemas.Badge])
async def list_badges(
    category: Optional[BadgeCategory] = None,
    tier: Optional[BadgeTier] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all badges, optionally filtered by category or tier"""
    query = select(Badge).where(Badge.is_active == True)

    if category:
        query = query.where(Badge.category == category)
    if tier:
        query = query.where(Badge.tier == tier)

    query = query.order_by(Badge.sort_order).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@app.get("/api/badges/{badge_id}", response_model=schemas.Badge)
async def get_badge(badge_id: int, db: AsyncSession = Depends(get_db)):
    """Get specific badge details"""
    result = await db.execute(select(Badge).where(Badge.id == badge_id))
    badge = result.scalars().first()
    if not badge:
        raise HTTPException(status_code=404, detail="Badge not found")
    return badge

@app.get("/api/users/{user_id}/badges", response_model=List[schemas.UserBadgeWithDetails])
async def get_user_badges(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get all badges earned by a user"""
    result = await db.execute(
        select(UserBadge)
        .options(selectinload(UserBadge.badge))
        .where(UserBadge.user_id == user_id)
        .order_by(UserBadge.earned_at.desc())
    )
    return result.scalars().all()

@app.get("/api/users/{user_id}/badge-progress", response_model=List[schemas.BadgeProgress])
async def get_user_badge_progress(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get user's progress towards all badges"""
    # Get user's current stats
    user_stats = await calculate_user_stats(db, user_id)

    # Get all badges
    result = await db.execute(select(Badge).where(Badge.is_active == True).order_by(Badge.sort_order))
    all_badges = result.scalars().all()

    # Get user's earned badges
    earned_result = await db.execute(
        select(UserBadge.badge_id).where(UserBadge.user_id == user_id)
    )
    earned_badge_ids = set(row[0] for row in earned_result.all())

    progress_list = []
    for badge in all_badges:
        current_value = user_stats.get(badge.criteria_type, 0.0)
        target_value = badge.criteria_value
        progress_percentage = min((current_value / target_value * 100) if target_value > 0 else 0, 100)
        is_earned = badge.id in earned_badge_ids

        progress_list.append(schemas.BadgeProgress(
            badge=badge,
            current_value=current_value,
            target_value=target_value,
            progress_percentage=progress_percentage,
            is_earned=is_earned
        ))

    return progress_list

@app.post("/api/users/{user_id}/badges/check")
async def check_and_award_badges(user_id: int, db: AsyncSession = Depends(get_db)):
    """Check if user has earned any new badges and award them"""
    newly_awarded = await award_badges_for_user(db, user_id)
    return {
        "user_id": user_id,
        "newly_awarded_count": len(newly_awarded),
        "newly_awarded_badges": newly_awarded
    }

@app.patch("/api/users/{user_id}/badges/{badge_id}/order-physical")
async def order_physical_badge(
    user_id: int,
    badge_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Mark a badge as physically ordered"""
    result = await db.execute(
        select(UserBadge).where(
            and_(UserBadge.user_id == user_id, UserBadge.badge_id == badge_id)
        )
    )
    user_badge = result.scalars().first()
    if not user_badge:
        raise HTTPException(status_code=404, detail="Badge not earned by user")

    # Check if badge can be ordered physically
    badge_result = await db.execute(select(Badge).where(Badge.id == badge_id))
    badge = badge_result.scalars().first()
    if not badge or not badge.can_order_physical:
        raise HTTPException(status_code=400, detail="This badge cannot be ordered physically")

    user_badge.physical_ordered = True
    user_badge.physical_ordered_at = datetime.utcnow()
    await db.commit()
    await db.refresh(user_badge)
    return user_badge

# ==================== MILESTONE ENDPOINTS ====================

@app.get("/api/milestones/", response_model=List[schemas.Milestone])
async def list_milestones(
    user_id: Optional[int] = None,
    organization_id: Optional[int] = None,
    is_public: bool = True,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List milestones"""
    query = select(Milestone)

    if user_id:
        query = query.where(Milestone.user_id == user_id)
    if organization_id:
        query = query.where(Milestone.organization_id == organization_id)
    if is_public:
        query = query.where(Milestone.is_public == True)

    query = query.order_by(Milestone.celebrated_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@app.post("/api/milestones/", response_model=schemas.Milestone, status_code=status.HTTP_201_CREATED)
async def create_milestone(milestone: schemas.MilestoneCreate, db: AsyncSession = Depends(get_db)):
    """Create a new milestone celebration"""
    db_milestone = Milestone(**milestone.dict())
    db.add(db_milestone)
    await db.commit()
    await db.refresh(db_milestone)

    # Create activity feed entry
    if milestone.user_id:
        activity = ActivityFeed(
            user_id=milestone.user_id,
            organization_id=milestone.organization_id,
            activity_type="milestone_reached",
            activity_text=f"Reached milestone: {milestone.title}",
            related_id=db_milestone.id,
            is_public=milestone.is_public
        )
        db.add(activity)
        await db.commit()

    return db_milestone

# ==================== SUCCESS STORY ENDPOINTS ====================

@app.get("/api/stories/", response_model=List[schemas.SuccessStoryWithUser])
async def list_success_stories(
    is_approved: bool = True,
    is_featured: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List success stories"""
    query = select(SuccessStory).options(selectinload(SuccessStory.user))

    if is_approved:
        query = query.where(SuccessStory.is_approved == True)
    if is_featured is not None:
        query = query.where(SuccessStory.is_featured == is_featured)

    query = query.order_by(SuccessStory.submitted_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@app.get("/api/stories/{story_id}", response_model=schemas.SuccessStoryWithUser)
async def get_success_story(story_id: int, db: AsyncSession = Depends(get_db)):
    """Get specific success story"""
    result = await db.execute(
        select(SuccessStory)
        .options(selectinload(SuccessStory.user))
        .where(SuccessStory.id == story_id)
    )
    story = result.scalars().first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story

@app.post("/api/stories/", response_model=schemas.SuccessStory, status_code=status.HTTP_201_CREATED)
async def create_success_story(
    story: schemas.SuccessStoryCreate,
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Submit a new success story"""
    db_story = SuccessStory(
        user_id=user_id,
        **story.dict()
    )
    db.add(db_story)
    await db.commit()
    await db.refresh(db_story)
    return db_story

@app.patch("/api/stories/{story_id}/approve")
async def approve_success_story(
    story_id: int,
    is_approved: bool = True,
    is_featured: bool = False,
    db: AsyncSession = Depends(get_db)
):
    """Approve or feature a success story (admin endpoint)"""
    result = await db.execute(select(SuccessStory).where(SuccessStory.id == story_id))
    story = result.scalars().first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    story.is_approved = is_approved
    story.is_featured = is_featured
    if is_approved and not story.approved_at:
        story.approved_at = datetime.utcnow()

    await db.commit()
    await db.refresh(story)
    return story

# ==================== PHOTO UPLOAD ENDPOINTS ====================

@app.get("/api/pledges/{pledge_id}/photos", response_model=List[schemas.PledgePhoto])
async def get_pledge_photos(pledge_id: int, db: AsyncSession = Depends(get_db)):
    """Get all photos for a pledge"""
    result = await db.execute(
        select(PledgePhoto)
        .where(PledgePhoto.pledge_id == pledge_id)
        .order_by(PledgePhoto.uploaded_at.desc())
    )
    return result.scalars().all()

@app.post("/api/photos/", response_model=schemas.PledgePhoto, status_code=status.HTTP_201_CREATED)
async def upload_pledge_photo(
    photo: schemas.PledgePhotoCreate,
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Upload a photo for a pledge"""
    # Verify pledge exists
    result = await db.execute(select(Pledge).where(Pledge.id == photo.pledge_id))
    pledge = result.scalars().first()
    if not pledge:
        raise HTTPException(status_code=404, detail="Pledge not found")

    db_photo = PledgePhoto(
        user_id=user_id,
        **photo.dict()
    )
    db.add(db_photo)
    await db.commit()
    await db.refresh(db_photo)
    return db_photo

@app.post("/api/photos/{photo_id}/verify")
async def verify_pledge_photo(photo_id: int, db: AsyncSession = Depends(get_db)):
    """Peer verification - increment verification count"""
    result = await db.execute(select(PledgePhoto).where(PledgePhoto.id == photo_id))
    photo = result.scalars().first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    photo.verified_by_peers += 1
    await db.commit()
    await db.refresh(photo)
    return photo

# ==================== ACTIVITY FEED ENDPOINTS ====================

@app.get("/api/activity/", response_model=List[schemas.ActivityFeedWithUser])
async def get_activity_feed(
    organization_id: Optional[int] = None,
    is_public: bool = True,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """Get activity feed"""
    query = select(ActivityFeed).options(selectinload(ActivityFeed.user))

    if organization_id:
        query = query.where(ActivityFeed.organization_id == organization_id)
    if is_public:
        query = query.where(ActivityFeed.is_public == True)

    query = query.order_by(ActivityFeed.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@app.post("/api/activity/", response_model=schemas.ActivityFeed, status_code=status.HTTP_201_CREATED)
async def create_activity(activity: schemas.ActivityFeedCreate, db: AsyncSession = Depends(get_db)):
    """Create a new activity feed entry"""
    db_activity = ActivityFeed(**activity.dict())
    db.add(db_activity)
    await db.commit()
    await db.refresh(db_activity)
    return db_activity

# ==================== USER PROFILE ENDPOINTS ====================

@app.get("/api/users/{user_id}/profile", response_model=schemas.UserProfileSummary)
async def get_user_profile(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get comprehensive user profile with stats, badges, and milestones"""
    # Get user
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get pledges
    pledge_result = await db.execute(
        select(Pledge).where(Pledge.user_id == user_id)
    )
    pledges = pledge_result.scalars().all()

    total_pledges = len(pledges)
    active_pledges = sum(1 for p in pledges if p.status in [PledgeStatus.ACTIVE, PledgeStatus.IN_PROGRESS])
    completed_pledges = sum(1 for p in pledges if p.status == PledgeStatus.COMPLETED)

    # Get badges
    badge_result = await db.execute(
        select(UserBadge)
        .options(selectinload(UserBadge.badge))
        .where(UserBadge.user_id == user_id)
        .order_by(UserBadge.earned_at.desc())
    )
    badges_earned = badge_result.scalars().all()

    # Get milestones
    milestone_result = await db.execute(
        select(Milestone)
        .where(Milestone.user_id == user_id)
        .order_by(Milestone.celebrated_at.desc())
        .limit(10)
    )
    milestones = milestone_result.scalars().all()

    # Calculate impact
    user_stats = await calculate_user_stats(db, user_id)

    # Calculate streak (simplified - could be enhanced)
    current_streak_days = 0  # TODO: Implement streak calculation

    return schemas.UserProfileSummary(
        user=user,
        total_pledges=total_pledges,
        active_pledges=active_pledges,
        completed_pledges=completed_pledges,
        badges_earned=badges_earned,
        total_carbon_saved=user_stats.get('carbon_saved', 0.0),
        total_plastic_saved=user_stats.get('plastic_saved', 0.0),
        total_water_saved=user_stats.get('water_saved', 0.0),
        current_streak_days=current_streak_days,
        milestones=milestones
    )

# ==================== HELPER FUNCTIONS ====================

async def calculate_user_stats(db: AsyncSession, user_id: int) -> dict:
    """Calculate various stats for a user for badge criteria checking"""
    # Get user's pledges
    result = await db.execute(
        select(Pledge).options(selectinload(Pledge.action)).where(Pledge.user_id == user_id)
    )
    pledges = result.scalars().all()

    stats = {
        'pledges_made': len(pledges),
        'pledges_completed': sum(1 for p in pledges if p.status == PledgeStatus.COMPLETED),
        'carbon_saved': 0.0,
        'plastic_saved': 0.0,
        'water_saved': 0.0,
        'trees_equivalent': 0.0,
        'ecosystem_points': 0.0,
        'streak_days': 0,  # TODO: Implement streak calculation
        'energy_pledges': 0,
        'waste_pledges': 0,
        'compost_days': 0,
        'renewable_pledge': 0,
        'org_joined': 0,
        'org_created': 0,
        'members_recruited': 0,
    }

    for pledge in pledges:
        # Calculate impact
        if pledge.action.is_parametric and pledge.parameter_current_value is not None:
            reduction = pledge.parameter_current_value - pledge.parameter_target_value
            if reduction > 0:
                duration_factor = pledge.duration_days / 365.0
                stats['carbon_saved'] += pledge.action.base_impact_per_unit * reduction * duration_factor
        else:
            multiplier = pledge.duration_days / 365.0
            if pledge.action.frequency_type.value == "daily":
                multiplier *= 365
            elif pledge.action.frequency_type.value == "weekly":
                multiplier *= 52
            elif pledge.action.frequency_type.value == "monthly":
                multiplier *= 12

            stats['carbon_saved'] += pledge.action.carbon_saved_kg * multiplier
            stats['plastic_saved'] += pledge.action.plastic_saved_kg * multiplier
            stats['water_saved'] += pledge.action.water_saved_liters * multiplier
            stats['trees_equivalent'] += pledge.action.trees_equivalent * multiplier
            stats['ecosystem_points'] += pledge.action.ecosystem_points * multiplier

        # Count category-specific pledges
        if pledge.action.category == ImpactCategory.ENERGY_CONSERVATION:
            stats['energy_pledges'] += 1
        if pledge.action.category == ImpactCategory.WASTE_REDUCTION:
            stats['waste_pledges'] += 1

    # Check organizations
    org_result = await db.execute(
        select(Organization).where(Organization.owner_id == user_id)
    )
    orgs_created = org_result.scalars().all()
    stats['org_created'] = len(orgs_created)

    # Check organization membership
    member_result = await db.execute(
        select(func.count(organization_members.c.organization_id))
        .where(organization_members.c.user_id == user_id)
    )
    stats['org_joined'] = member_result.scalar() or 0

    return stats

async def award_badges_for_user(db: AsyncSession, user_id: int) -> List[schemas.Badge]:
    """Check all badge criteria and award any newly earned badges"""
    user_stats = await calculate_user_stats(db, user_id)

    # Get all badges
    result = await db.execute(select(Badge).where(Badge.is_active == True))
    all_badges = result.scalars().all()

    # Get already earned badges
    earned_result = await db.execute(
        select(UserBadge.badge_id).where(UserBadge.user_id == user_id)
    )
    earned_badge_ids = set(row[0] for row in earned_result.all())

    newly_awarded = []

    for badge in all_badges:
        # Skip if already earned
        if badge.id in earned_badge_ids:
            continue

        # Check if criteria is met
        current_value = user_stats.get(badge.criteria_type, 0.0)
        if current_value >= badge.criteria_value:
            # Award the badge
            user_badge = UserBadge(
                user_id=user_id,
                badge_id=badge.id,
                progress=100.0
            )
            db.add(user_badge)
            newly_awarded.append(badge)

            # Create activity feed entry
            activity = ActivityFeed(
                user_id=user_id,
                activity_type="badge_earned",
                activity_text=f"Earned the '{badge.name}' badge!",
                related_id=badge.id,
                is_public=True
            )
            db.add(activity)

    if newly_awarded:
        await db.commit()

    return newly_awarded

# ==================== HEALTH CHECK ====================

@app.get("/")
async def root():
    return {
        "message": "Planet Pledge API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
