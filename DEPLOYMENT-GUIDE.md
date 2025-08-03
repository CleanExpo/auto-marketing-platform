# Deployment Guide - Auto Marketing Platform

## 🚀 GitHub Push Instructions

Since there's an authentication issue, you'll need to push manually:

### Option 1: Using GitHub Desktop
1. Open GitHub Desktop
2. It should detect all the changes
3. Review the changes
4. Click "Push origin"

### Option 2: Using Personal Access Token
```bash
# Set up authentication
git remote set-url origin https://YOUR_GITHUB_TOKEN@github.com/PhillMcGurk/SYNTHEX.git

# Push changes
git push origin main
```

### Option 3: Using SSH
```bash
# Change remote to SSH
git remote set-url origin git@github.com:PhillMcGurk/SYNTHEX.git

# Push changes
git push origin main
```

## 🔷 Vercel Deployment

### Prerequisites
1. Vercel account (free at vercel.com)
2. Vercel CLI: `npm i -g vercel`

### Method 1: Vercel CLI Deployment

```bash
# Login to Vercel
vercel login

# Deploy to production
vercel --prod

# Follow the prompts:
# - Link to existing project or create new
# - Select the directory (current)
# - Override settings if needed
```

### Method 2: GitHub Integration (Recommended)

1. Go to [vercel.com](https://vercel.com)
2. Click "Import Project"
3. Select "Import Git Repository"
4. Authorize GitHub and select `PhillMcGurk/SYNTHEX`
5. Configure:
   - Framework Preset: `Other`
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

### Method 3: Manual Deployment

1. Build locally:
```bash
npm run build
```

2. Deploy using Vercel CLI:
```bash
vercel deploy --prod
```

## 🔐 Environment Variables

Add these in Vercel Dashboard > Settings > Environment Variables:

```env
# Required
NODE_ENV=production
PORT=3000

# API Keys (Add your actual keys)
ANTHROPIC_API_KEY=your_anthropic_api_key
OPENROUTER_API_KEY=your_openrouter_api_key

# Optional
RATE_LIMIT_WINDOW=15
RATE_LIMIT_MAX=100
```

## 📦 Project Structure for Vercel

```
/
├── dist/               # Built TypeScript files
├── public/             # Static files (HTML, CSS, JS)
├── src/                # Source TypeScript files
├── package.json        # Dependencies and scripts
├── vercel.json         # Vercel configuration
├── tsconfig.json       # TypeScript configuration
└── .env.example        # Environment variables template
```

## 🎯 Quick Deploy Steps

1. **Push to GitHub:**
```bash
# If you have authentication set up:
git push origin main
```

2. **Deploy to Vercel:**
```bash
# Install Vercel CLI if not installed
npm i -g vercel

# Deploy
vercel --prod
```

3. **Configure Environment:**
- Go to your Vercel dashboard
- Add environment variables
- Redeploy if needed

## 🔍 Verifying Deployment

After deployment, test these endpoints:

```bash
# Health check
curl https://your-app.vercel.app/health

# API info
curl https://your-app.vercel.app/api

# OpenRouter status
curl https://your-app.vercel.app/api/openrouter/status

# MCP status
curl https://your-app.vercel.app/api/mcp-ttd/mcp/status

# MLE Star score
curl https://your-app.vercel.app/api/mle-star/score
```

## 🚨 Troubleshooting

### Build Fails
- Check TypeScript errors: `npm run build`
- Verify all dependencies: `npm install`
- Check Node version: Should be >=16.0.0

### API Routes Not Working
- Verify environment variables are set
- Check Vercel function logs
- Ensure proper CORS configuration

### Rate Limiting Issues
- Adjust rate limit settings in environment variables
- Check Vercel function execution limits

## 📊 Monitoring

1. **Vercel Dashboard:**
   - Real-time logs
   - Function metrics
   - Error tracking

2. **Application Metrics:**
   - `/health` - System health
   - `/api/mle-star/report` - ML metrics
   - `/api/enhancement/analytics/insights` - Analytics

## 🔄 Continuous Deployment

Once GitHub integration is set up:
1. Every push to `main` triggers deployment
2. Preview deployments for pull requests
3. Automatic rollback on failures

## 📝 Post-Deployment Checklist

- [ ] All API endpoints responding
- [ ] Environment variables configured
- [ ] Rate limiting active
- [ ] Analytics dashboard accessible
- [ ] MCP providers initialized
- [ ] OpenRouter connection verified
- [ ] UI accessible (both Modern and Classic)
- [ ] Test scripts passing

## 🎉 Success Indicators

Your deployment is successful when:
- Health endpoint returns `{"status": "healthy"}`
- API endpoints are accessible
- UI loads at root URL
- No errors in Vercel function logs
- MLE Star score can be calculated

## 📚 Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Project Documentation](./docs/)
- [API Documentation](./README.md)
- [MLE Star Guide](./docs/MLE-STAR-INTEGRATION.md)
- [MCP TTD RD Guide](./docs/MCP-TTD-RD-INTEGRATION.md)