@echo off
echo Resetting and Seeding FulfillIQ Database...
python -m database.seed_data
echo Database Seeded Successfully!
pause
