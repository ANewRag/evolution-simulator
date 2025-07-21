#!/bin/bash

# Run backend
cd backend
source venv/bin/activate
uvicorn api:app --reload &
cd ../frontend
npm run dev
