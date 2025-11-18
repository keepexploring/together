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
    Campaign, CampaignSignature, ImpactCategory, PledgeStatus, organization_members
)
import schemas
from seed_data import ENVIRONMENTAL_ACTIONS

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
    # Seed environmental actions if database is empty
    async for db in get_db():
        result = await db.execute(select(EnvironmentalAction).where(EnvironmentalAction.is_global == True))
        if not result.scalars().first():
            for action_data in ENVIRONMENTAL_ACTIONS:
                action = EnvironmentalAction(**action_data, is_global=True)
                db.add(action)
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
    result = await db.execute(select(Pledge).where(Pledge.id == pledge_id))
    pledge = result.scalars().first()
    if not pledge:
        raise HTTPException(status_code=404, detail="Pledge not found")

    pledge.status = status_update
    await db.commit()
    await db.refresh(pledge)
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
