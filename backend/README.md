# Planet Pledge API - Backend

FastAPI backend for the Planet Pledge environmental action tracking platform.

## Features

- **Environmental Actions Database**: 50+ researched actions with real impact data
- **Pledge Management**: Track individual and organizational commitments
- **Impact Calculation**: Real-time aggregation of carbon, plastic, water, and ecosystem impacts
- **Organization Support**: Groups can create custom access codes and URLs
- **Campaign System**: Launch environmental campaigns and collect signatures
- **Follow-up System**: Automated check-ins based on trust

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

4. Run the application:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Key Endpoints

### Environmental Actions
- `GET /api/actions/` - List all environmental actions
- `GET /api/actions/{id}` - Get specific action
- `POST /api/actions/` - Create custom action (for organizers)

### Pledges
- `POST /api/pledges/` - Create a new pledge
- `POST /api/pledges/simple` - Create pledge with access code (for events)
- `GET /api/pledges/` - List pledges (with filters)
- `PATCH /api/pledges/{id}/status` - Update pledge status

### Organizations
- `POST /api/organizations/` - Create organization
- `GET /api/organizations/code/{code}` - Get org by access code
- `GET /api/organizations/url/{url}` - Get org by simple URL

### Impact Tracking
- `GET /api/impact/global` - Global impact summary
- `GET /api/impact/organization/{id}` - Organization impact summary

### Campaigns
- `POST /api/campaigns/` - Create campaign
- `GET /api/campaigns/` - List campaigns
- `POST /api/campaigns/{id}/sign` - Sign a campaign
- `GET /api/campaigns/{id}/signatures` - Get campaign signatures

## Environmental Actions Database

The system includes 50+ environmental actions with scientifically-sourced impact data:

### Categories
- **Carbon Reduction**: Transportation, diet, energy
- **Plastic Reduction**: Reusables, packaging choices
- **Water Conservation**: Fixtures, behavioral changes
- **Waste Reduction**: Composting, recycling, secondhand
- **Ecosystem Restoration**: Tree planting, habitat creation

### Impact Metrics
- Carbon saved (kg CO2e)
- Plastic prevented (kg)
- Water saved (liters)
- Tree equivalents
- Ecosystem restoration points

All data is sourced from peer-reviewed research and official environmental organizations.

## Database

Uses SQLAlchemy with async SQLite (can easily switch to PostgreSQL for production).

Models:
- `User` - Individual users
- `Organization` - Groups/communities
- `EnvironmentalAction` - Actions database
- `Pledge` - Individual commitments
- `FollowUp` - Check-in records
- `Campaign` - Environmental campaigns
- `CampaignSignature` - Campaign support

## Development

The API uses:
- FastAPI for high-performance async endpoints
- SQLAlchemy ORM with async support
- Pydantic for data validation
- Auto-generated OpenAPI documentation
