# Stories of Stories

An interactive storytelling platform where users can navigate branching narratives, make meaningful choices, and create their own story paths.

## Project Overview

This is a full-stack application built with:
- **Backend**: Python (Flask/FastAPI)
- **Frontend**: Next.js with TypeScript
- **Database**: SQL

## Features

- 📖 Interactive branching narratives
- 🎮 Player choice-driven gameplay
- 👤 User authentication and profiles
- 💾 Story progression tracking
- 🌍 World-building engine

## Project Structure

```
backend/          - Python API server
├── app/
│   ├── main.py   - Entry point
│   ├── engine/   - Story and game logic
│   └── routes/   - API endpoints
└── requirements.txt

frontend/         - Next.js React app
├── app/          - Pages and layouts
├── components/   - React components
└── lib/          - Utilities and API client

database/         - Database schemas and seeds
├── schema.sql    - Database structure
└── seed.json     - Initial data
```

## Getting Started

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app/main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Database Setup
```bash
# Run schema.sql against your database
```

## Development

- Main branch is `main`
- Create feature branches for new work: `feature/feature-name`
- All PRs require review before merging

## License

TBD

## Author

@stanleyreysa-commits
