#!/bin/bash

# Deploy the trading journal application to Vercel
echo "Deploying Trading Journal to Vercel..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null
then
    echo "Vercel CLI is not installed. Installing..."
    npm install -g vercel
fi

# Deploy to Vercel
vercel --prod

echo "Deployment completed. Visit Vercel dashboard to check your deployment status."