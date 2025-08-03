# 🚀 Vercel Deployment Steps

## Current Status
✅ All code changes committed
✅ Vercel configuration added (vercel.json)
✅ Environment variables template created
⏳ Ready for deployment

## Step 1: Login to Vercel CLI

Open a new terminal and run:
```bash
npx vercel login
```

This will:
1. Ask for your email
2. Send a verification email
3. Click the link in the email to authenticate

## Step 2: Deploy to Vercel

Once authenticated, run:
```bash
npx vercel --prod
```

Answer the prompts:
- **Set up and deploy "C:\Auto Marketing"?** → Yes
- **Which scope?** → Select your account (admin-cleanexpo247s-projects)
- **Link to existing project?** → No (create new)
- **Project name?** → auto-marketing-platform (or press enter for default)
- **Directory?** → ./ (current directory)
- **Override settings?** → No

## Step 3: Set Environment Variables

After deployment, go to your Vercel dashboard:
1. Visit: https://vercel.com/admin-cleanexpo247s-projects/auto-marketing-platform
2. Go to "Settings" → "Environment Variables"
3. Add these required variables:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
NODE_ENV=production
PORT=3000
```

4. Click "Save" for each variable

## Step 4: Redeploy with Environment Variables

After adding environment variables:
```bash
npx vercel --prod --force
```

## Alternative: Deploy via Vercel Dashboard

1. Go to: https://vercel.com/admin-cleanexpo247s-projects
2. Click "Add New..." → "Project"
3. Import from Git Repository:
   - If GitHub connected: Select "PhillMcGurk/SYNTHEX"
   - If not: Use "Import Third-Party Git Repository"
   - Enter: `https://github.com/PhillMcGurk/SYNTHEX.git`

4. Configure Project:
   - Framework Preset: `Other`
   - Root Directory: `./`
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

5. Add Environment Variables (same as Step 3)

6. Click "Deploy"

## Step 5: Verify Deployment

Once deployed, test these URLs (replace with your actual domain):

```bash
# Check health
curl https://auto-marketing-platform.vercel.app/health

# Check API
curl https://auto-marketing-platform.vercel.app/api

# Check UI
open https://auto-marketing-platform.vercel.app
```

## Quick Deploy Script

Save this as `deploy.sh` and run it:

```bash
#!/bin/bash
echo "🚀 Deploying Auto Marketing Platform to Vercel..."

# Build the project
npm run build

# Deploy to Vercel
npx vercel --prod

echo "✅ Deployment complete!"
echo "📱 Visit your app at the URL provided above"
echo "⚙️  Don't forget to add environment variables in Vercel dashboard!"
```

## Troubleshooting

### Authentication Issues
```bash
# Clear Vercel auth and re-login
npx vercel logout
npx vercel login
```

### Build Errors
```bash
# Test build locally first
npm run build

# Check for TypeScript errors
npm run typecheck
```

### Environment Variables Not Working
- Make sure to redeploy after adding variables
- Check variable names match exactly
- Verify in Vercel dashboard under Settings

## Your Vercel Project URLs

Once deployed, your project will be available at:
- Production: `https://auto-marketing-platform.vercel.app`
- Dashboard: `https://vercel.com/admin-cleanexpo247s-projects/auto-marketing-platform`
- Analytics: `https://vercel.com/admin-cleanexpo247s-projects/auto-marketing-platform/analytics`

## Next Steps After Deployment

1. **Test all endpoints** using the test scripts:
   ```bash
   node test-openrouter.js
   node test-mcp-ttd.js
   node test-mle-star.js
   node test-research.js
   ```

2. **Monitor the deployment**:
   - Check Vercel Functions logs
   - Monitor API response times
   - Track error rates

3. **Set up continuous deployment**:
   - Connect GitHub repository
   - Enable automatic deployments on push

## 🎉 Success Checklist

- [ ] Vercel CLI authenticated
- [ ] Project deployed successfully
- [ ] Environment variables configured
- [ ] Health endpoint responding
- [ ] API endpoints accessible
- [ ] UI loading correctly
- [ ] Test scripts passing

Once all items are checked, your Auto Marketing Platform is live and ready for production use!