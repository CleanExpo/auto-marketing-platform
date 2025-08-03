# 🌐 OpenRouter Integration Guide

## 🚀 Overview

Your Auto Marketing Agent now includes **OpenRouter Horizon Alpha** integration! This gives you access to powerful AI models including the free Horizon Alpha model during its testing period.

## 🔑 Setup Instructions

### Step 1: Get Your OpenRouter API Key

1. Visit [OpenRouter.ai](https://openrouter.ai)
2. Sign up for a free account
3. Navigate to your API Keys section
4. Generate a new API key

### Step 2: Configure Your Environment

Add your OpenRouter API key to your `.env` file:

```env
# OpenRouter API Configuration
OPENROUTER_API_KEY=your_actual_openrouter_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_SITE_URL=http://localhost:3000
OPENROUTER_SITE_NAME=Auto Marketing Agent
```

### Step 3: Restart Your Server

```bash
npm run dev
```

## 🎯 Available Models

### Horizon Alpha (Recommended)
- **Model ID**: `openrouter/horizon-alpha`
- **Context**: 256k tokens
- **Cost**: **FREE** during testing period
- **Best for**: General marketing tasks, content generation
- **Note**: Responses are logged for model improvement

### Other Available Models
- **Horizon Beta**: Improved version of Alpha
- **Auto Router**: Automatically selects best model
- **Cypher Alpha**: Code generation focused
- **Optimus Alpha**: Real-world use cases
- **Quasar Alpha**: Long-context tasks

## 📡 API Endpoints

### Status & Information

#### Check OpenRouter Status
```bash
GET /api/openrouter/status
```

#### Get Available Models
```bash
GET /api/openrouter/models
```

#### Test Connection
```bash
GET /api/openrouter/test
```

### Chat & Content Generation

#### Basic Chat
```bash
POST /api/openrouter/chat
```
```json
{
  "message": "Hello! Create a marketing slogan for a coffee shop.",
  "model": "openrouter/horizon-alpha",
  "temperature": 0.7
}
```

#### Generate Marketing Content
```bash
POST /api/openrouter/marketing/generate
```
```json
{
  "prompt": "Create a social media post for a new eco-friendly product launch",
  "contentType": "social_post",
  "model": "openrouter/horizon-alpha"
}
```

#### Optimize Existing Content
```bash
POST /api/openrouter/marketing/optimize
```
```json
{
  "content": "Buy our product now! It's great!",
  "platform": "instagram",
  "goals": ["engagement", "conversions"]
}
```

#### Generate Content Variations
```bash
POST /api/openrouter/marketing/variations
```
```json
{
  "prompt": "Summer sale announcement",
  "count": 3,
  "contentType": "email"
}
```

## 🛠️ Usage Examples

### Example 1: Generate Social Media Post
```bash
curl -X POST http://localhost:3000/api/openrouter/marketing/generate \\
  -H "Content-Type: application/json" \\
  -d '{
    "prompt": "Create an engaging Instagram post for a fitness app launch",
    "contentType": "social_post"
  }'
```

### Example 2: Optimize Email Subject Line
```bash
curl -X POST http://localhost:3000/api/openrouter/marketing/optimize \\
  -H "Content-Type: application/json" \\
  -d '{
    "content": "Newsletter #47",
    "platform": "email",
    "goals": ["open_rate", "engagement"]
  }'
```

### Example 3: Generate Blog Variations
```bash
curl -X POST http://localhost:3000/api/openrouter/marketing/variations \\
  -H "Content-Type: application/json" \\
  -d '{
    "prompt": "10 productivity tips for remote workers",
    "count": 5,
    "contentType": "blog"
  }'
```

## 🎨 Content Types

The system supports these content types:

- **`social_post`**: Social media posts (Twitter, Instagram, LinkedIn)
- **`email`**: Email marketing content
- **`blog`**: Blog posts and articles
- **`ad_copy`**: Advertising copy
- **`general`**: General marketing content

## ⚙️ Advanced Configuration

### Custom Model Parameters

```json
{
  "prompt": "Your marketing prompt here",
  "model": "openrouter/horizon-alpha",
  "temperature": 0.8,
  "max_tokens": 500,
  "top_p": 0.9
}
```

### Parameter Explanations

- **`temperature`** (0.0-2.0): Controls creativity
  - `0.3`: More focused, consistent
  - `0.7`: Balanced creativity
  - `1.2`: More creative, varied
  
- **`max_tokens`**: Maximum response length
  - Social posts: 100-200
  - Emails: 300-500
  - Blog content: 800-1500

- **`top_p`** (0.0-1.0): Controls response diversity

## 🔍 Testing Your Setup

### Quick Test
```bash
# Test connection
curl http://localhost:3000/api/openrouter/test

# Check status
curl http://localhost:3000/api/openrouter/status

# Simple chat test
curl -X POST http://localhost:3000/api/openrouter/chat \\
  -H "Content-Type: application/json" \\
  -d '{"message": "Hello! Please write a short marketing tagline."}'
```

## 📊 Response Format

All endpoints return JSON responses:

### Success Response
```json
{
  "content": "Generated marketing content here...",
  "model": "openrouter/horizon-alpha",
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 150,
    "total_tokens": 175
  },
  "timestamp": "2025-08-02T12:00:00.000Z"
}
```

### Error Response
```json
{
  "error": "Content generation failed",
  "message": "API key not configured"
}
```

## 🚨 Important Notes

### Free Usage
- Horizon Alpha is **FREE** during testing period
- Responses are logged by OpenRouter for improvement
- No rate limits during testing phase

### Production Considerations
- Monitor your usage as models may transition to paid
- Consider upgrading to paid models for production use
- Keep your API key secure

### Privacy
- Horizon Alpha logs all prompts and responses
- Don't send sensitive or personal information
- Use for marketing content generation only

## 🎉 Quick Start Checklist

- [ ] ✅ Get OpenRouter API key from [openrouter.ai](https://openrouter.ai)
- [ ] ✅ Add `OPENROUTER_API_KEY` to your `.env` file
- [ ] ✅ Restart your development server
- [ ] ✅ Test connection: `GET /api/openrouter/test`
- [ ] ✅ Generate your first marketing content!

## 🆘 Troubleshooting

### "API key not configured"
- Check your `.env` file has `OPENROUTER_API_KEY`
- Restart your server after adding the key
- Verify the key is valid on OpenRouter.ai

### "Request failed"
- Check your internet connection
- Verify OpenRouter API status
- Try a simpler prompt first

### TypeScript errors
- Run `npm install` to ensure all dependencies
- Check that `@types/express` is installed

---

## 🎯 Start Creating Amazing Marketing Content!

Your Auto Marketing Agent is now powered by OpenRouter's Horizon Alpha model. Start generating professional marketing content with AI assistance!

```bash
# Start your server
npm run dev

# Test the integration
curl http://localhost:3000/api/openrouter/test

# Generate your first marketing content!
curl -X POST http://localhost:3000/api/openrouter/marketing/generate \\
  -H "Content-Type: application/json" \\
  -d '{"prompt": "Create a compelling product launch announcement", "contentType": "social_post"}'
```

Happy marketing! 🚀
