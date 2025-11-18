# Planet Pledge

**An environmental pledge tracking platform that enables people to make commitments to reduce their impact on the planet and collectively measure their progress.**

## Overview

Planet Pledge is a full-stack web application designed to help individuals, churches, community groups, and organizations make and track environmental pledges. The platform calculates real-time collective impact including carbon reduction, plastic prevention, water conservation, and ecosystem restoration.

### Key Features

- **50+ Environmental Actions**: Scientifically-researched actions with real impact data
- **Pledge System**: Make commitments with customizable duration and follow-up schedules
- **Organization Support**: Groups can create access codes for members to join together
- **Impact Tracking**: Real-time calculation of collective environmental impact
- **Campaign System**: Launch environmental campaigns and gather signatures
- **CMS**: Organizers can create custom actions specific to their community
- **Follow-up System**: Honor-based check-ins to track progress
- **Simple Access**: Easy URL/code system for events and gatherings

## Technology Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **SQLAlchemy** - ORM with async support
- **SQLite/PostgreSQL** - Database (easily switchable)
- **Pydantic** - Data validation
- **APScheduler** - Background task scheduling

### Frontend
- **Quasar Framework** - Vue 3 based UI framework
- **Vue 3** - Progressive JavaScript framework
- **Pinia** - State management
- **Axios** - HTTP client
- **Chart.js** - Data visualization

## Project Structure

```
planet-pledge/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   ├── database.py          # Database configuration
│   ├── seed_data.py         # Environmental actions database
│   ├── requirements.txt     # Python dependencies
│   └── README.md            # Backend documentation
│
├── frontend/
│   ├── src/
│   │   ├── components/      # Vue components
│   │   ├── layouts/         # Layout components
│   │   ├── pages/           # Page components
│   │   ├── router/          # Vue Router configuration
│   │   ├── boot/            # Quasar boot files
│   │   └── css/             # Global styles
│   ├── package.json         # Node dependencies
│   ├── quasar.config.js     # Quasar configuration
│   └── index.html           # Entry HTML
│
└── README.md                # This file
```

## Environmental Actions Database

The platform includes **50+ environmental actions** with scientifically-sourced impact data across six categories:

### Categories

1. **Carbon Reduction** (16 actions)
   - Transportation choices (car-free, EV, cycling, carpooling)
   - Diet changes (plant-based, meatless days)
   - Energy efficiency

2. **Plastic Reduction** (8 actions)
   - Reusable products (bottles, bags, containers)
   - Packaging choices
   - Single-use plastic elimination

3. **Water Conservation** (5 actions)
   - Fixture upgrades (low-flow, high-efficiency)
   - Behavioral changes (shower time, leak fixes)
   - Rainwater harvesting

4. **Waste Reduction** (6 actions)
   - Composting
   - Recycling
   - Secondhand purchases
   - Repair over replace

5. **Ecosystem Restoration** (7 actions)
   - Tree planting
   - Pollinator gardens
   - Invasive species removal
   - Native plant landscaping

6. **Energy Conservation** (8 actions)
   - Renewable energy
   - LED bulbs
   - Thermostat management
   - Insulation

### Impact Metrics

Each action includes measurable impact data:
- **Carbon saved** (kg CO2e per year)
- **Plastic prevented** (kg per year)
- **Water saved** (liters per year)
- **Tree equivalents**
- **Ecosystem restoration points**

All data is sourced from peer-reviewed research including:
- Lund University climate studies
- UN Environmental Programme
- OECD environmental reports
- EPA research
- UK Carbon Trust data

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API Documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

3. Run development server:
```bash
npm run dev
# or
yarn dev
```

The app will be available at `http://localhost:9000`

### Production Build

**Backend:**
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm run build
# or
yarn build
```

## Usage Examples

### For Individuals

1. Visit the app
2. Click "Make a Pledge"
3. Browse 50+ environmental actions
4. Select an action and set your commitment duration
5. Track your personal impact

### For Organizations

1. Click "Organize" to create a group
2. Receive a unique access code (e.g., "ABC123")
3. Share code with members via email/events
4. Members join and make pledges
5. View collective organizational impact

### For Events

1. Create organization with simple URL
2. Display code or URL at event
3. Attendees scan/visit and make pledges
4. See real-time collective impact grow

## API Endpoints

### Environmental Actions
- `GET /api/actions/` - List all actions
- `GET /api/actions/{id}` - Get specific action
- `POST /api/actions/` - Create custom action

### Pledges
- `POST /api/pledges/` - Create pledge
- `POST /api/pledges/simple` - Create pledge with access code
- `GET /api/pledges/` - List pledges
- `PATCH /api/pledges/{id}/status` - Update status

### Organizations
- `POST /api/organizations/` - Create organization
- `GET /api/organizations/code/{code}` - Get by access code
- `GET /api/impact/organization/{id}` - Get organization impact

### Campaigns
- `POST /api/campaigns/` - Create campaign
- `POST /api/campaigns/{id}/sign` - Sign campaign
- `GET /api/campaigns/{id}/signatures` - Get signatures

### Impact
- `GET /api/impact/global` - Global impact summary
- `GET /api/impact/organization/{id}` - Organization impact

## Database Schema

**Core Models:**
- `User` - Individual users and organizers
- `Organization` - Groups/communities
- `EnvironmentalAction` - Actions database (global + custom)
- `Pledge` - Individual commitments
- `FollowUp` - Check-in records
- `Campaign` - Environmental campaigns
- `CampaignSignature` - Campaign support

## Follow-up System

The platform includes an honor-based follow-up system:
- Users specify check-in frequency (default: every 7 days)
- System tracks next follow-up date
- Users can update progress via email or app
- Status updates: active, in_progress, completed, missed
- All based on trust - no enforcement

## Future Enhancements

- [ ] Email notification system for follow-ups
- [ ] Mobile app (iOS/Android)
- [ ] Social sharing features
- [ ] Gamification and badges
- [ ] Data export for organizations
- [ ] Integration with carbon offset platforms
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] API for third-party integrations

## Contributing

This is an open platform for environmental action. Contributions welcome:

1. Research and add new environmental actions with sourced data
2. Improve impact calculations
3. Add features for better community engagement
4. Enhance UI/UX
5. Add translations

## Data Sources

Impact data sourced from:
- Lund University: "The four lifestyle choices that most reduce your carbon footprint"
- Columbia Climate School: "35 Easiest Ways to Reduce Your Carbon Footprint"
- UN Environment Programme: "Actions for a healthy planet"
- OECD: "Policies to Reduce Microplastics Pollution in Water"
- Nature: "Assessing the climate change mitigation potential from food waste composting"
- EPA: "Food Waste Management Quantifying Methane Emissions"
- UK Environment Studies: Reusable product impact studies

## License

This project is created to help people make positive environmental impact.

## Contact

For questions, suggestions, or to report issues with impact data, please open an issue in the repository.

---

**Together we can make a difference for our planet. Every action counts.**
