import dotenv from 'dotenv';
import express, { Request, Response, NextFunction } from 'express';
import path from 'path';
import rateLimit from 'express-rate-limit';
import openRouterRoutes from './routes/openrouter';
import mcpTtdRoutes from './routes/mcp-ttd';
import enhancementRoutes from './routes/enhancement-research';
import mleStarRoutes from './routes/mle-star';
import { openRouterService } from './services/openrouter';
import { mcpIntegration } from './services/mcp-integration';
import { ttdRd } from './services/ttd-rd-framework';
import { mcpContext7 } from './services/mcp-context7-integration';

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;
const NODE_ENV = process.env.NODE_ENV || 'development';

// Rate limiting configuration
const generalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again later.',
  standardHeaders: true, // Return rate limit info in the `RateLimit-*` headers
  legacyHeaders: false, // Disable the `X-RateLimit-*` headers
});

// Stricter rate limiting for API endpoints
const apiLimiter = rateLimit({
  windowMs: 1 * 60 * 1000, // 1 minute
  max: 20, // Limit each IP to 20 API requests per minute
  message: 'API rate limit exceeded. Please wait before making more requests.',
  standardHeaders: true,
  legacyHeaders: false,
  skipSuccessfulRequests: false,
});

// Very strict rate limiting for content generation endpoints
const contentGenerationLimiter = rateLimit({
  windowMs: 1 * 60 * 1000, // 1 minute
  max: 10, // Limit each IP to 10 content generation requests per minute
  message: 'Content generation rate limit exceeded. Please wait before generating more content.',
  standardHeaders: true,
  legacyHeaders: false,
});

// Serve static files from public directory
app.use(express.static(path.join(__dirname, '..', 'public')));

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Apply general rate limiting to all requests
app.use(generalLimiter);

// CORS middleware for development
if (NODE_ENV === 'development') {
  app.use((req: Request, res: Response, next: NextFunction) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization');
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    next();
  });
}

// Logging middleware
app.use((req: Request, res: Response, next: NextFunction) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
  next();
});

// Health check endpoint
app.get('/health', (req: Request, res: Response) => {
  res.status(200).json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    environment: NODE_ENV,
    version: '1.0.0'
  });
});

// Main endpoint - redirect to modern UI
app.get('/', (req: Request, res: Response) => {
  res.sendFile('app.html', { root: path.join(__dirname, '..', 'public') });
});

// Classic UI endpoint
app.get('/classic', (req: Request, res: Response) => {
  res.sendFile('index.html', { root: path.join(__dirname, '..', 'public') });
});

// API info endpoint
app.get('/api-info', (req: Request, res: Response) => {
  res.json({
    message: '🤖 Auto Marketing Agent is running!',
    status: 'active',
    environment: NODE_ENV,
    endpoints: {
      health: '/health',
      api: '/api',
      modernUI: '/',
      classicUI: '/classic'
    }
  });
});

// API routes placeholder
app.get('/api', (req: Request, res: Response) => {
  res.json({
    message: 'Auto Marketing Agent API',
    version: '1.0.0',
    availableEndpoints: [
      'GET /health - Health check',
      'GET /api - API information',
      'GET /api/openrouter/status - OpenRouter status',
      'GET /api/openrouter/models - Available AI models',
      'GET /api/openrouter/test - Test OpenRouter connection',
      'POST /api/openrouter/chat - Chat with AI',
      'POST /api/openrouter/marketing/generate - Generate marketing content',
      'POST /api/openrouter/marketing/optimize - Optimize content',
      'POST /api/openrouter/marketing/variations - Generate variations',
      'GET /api/mcp-ttd/mcp/status - MCP integration status',
      'POST /api/mcp-ttd/mcp/sequential-think - Sequential thinking with MCP',
      'POST /api/mcp-ttd/ttd/create-tests - Create test-first development tests',
      'POST /api/mcp-ttd/ttd/implement-feature - Implement feature with TTD',
      'POST /api/mcp-ttd/ttd/rapid-deploy - Rapid deployment with TTD RD',
      'POST /api/mcp-ttd/ttd/integrate-mcp - Integrate feature with MCP',
      'POST /api/mle-star/evaluate/* - MLE Star dimension evaluation',
      'GET /api/mle-star/score - Get MLE Star score',
      'POST /api/mle-star/pipeline/create - Create ML pipeline',
      'POST /api/mle-star/model/train - Train marketing model',
      'POST /api/mle-star/context7/sequential-think - Context7 sequential thinking',
      'GET /api/mle-star/report - Generate MLE report',
      'POST /api/campaign - Create marketing campaign (coming soon)',
      'GET /api/analytics - Get analytics data (coming soon)'
    ]
  });
});

// OpenRouter API routes with rate limiting
// Apply stricter rate limiting to content generation endpoints
app.use('/api/openrouter/marketing/generate', contentGenerationLimiter);
app.use('/api/openrouter/marketing/optimize', contentGenerationLimiter);
app.use('/api/openrouter/marketing/variations', contentGenerationLimiter);
app.use('/api/openrouter/chat', contentGenerationLimiter);

// Apply general API rate limiting to other OpenRouter endpoints
app.use('/api/openrouter', apiLimiter, openRouterRoutes);

// MCP and TTD RD routes
app.use('/api/mcp-ttd', apiLimiter, mcpTtdRoutes);

// Enhancement research and analytics routes
app.use('/api/enhancement', apiLimiter, enhancementRoutes);

// MLE Star and Context7 routes
app.use('/api/mle-star', apiLimiter, mleStarRoutes);

// Error handling middleware
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  console.error('Error:', err.message);
  res.status(500).json({
    error: 'Internal Server Error',
    message: NODE_ENV === 'development' ? err.message : 'Something went wrong'
  });
});

// 404 handler
app.use('*', (req: Request, res: Response) => {
  res.status(404).json({
    error: 'Not Found',
    message: `The endpoint ${req.method} ${req.originalUrl} was not found`
  });
});

// Start server
app.listen(PORT, async () => {
  console.log(`🚀 Auto Marketing Agent server running on port ${PORT}`);
  console.log(`📊 Environment: ${NODE_ENV}`);
  console.log(`🔗 Health check: http://localhost:${PORT}/health`);
  console.log(`📡 API: http://localhost:${PORT}/api`);
  console.log(`🌐 Web UI: http://localhost:${PORT}/`);
  
  console.log('\n🛡️ Rate Limiting Active:');
  console.log('  • General: 100 requests per 15 minutes');
  console.log('  • API: 20 requests per minute');
  console.log('  • Content Generation: 10 requests per minute');
  
  // Initialize MCP Sequential Thinking
  try {
    await mcpIntegration.initializeSequentialThinking();
    console.log('\n✅ MCP Sequential Thinking initialized');
  } catch (error) {
    console.log('\n⚠️  MCP Sequential Thinking initialization failed:', error);
  }
  
  // Initialize Context7 MCP providers
  try {
    await mcpContext7.initializeProviders();
    console.log('✅ Context7 MCP providers initialized');
  } catch (error) {
    console.log('⚠️  Context7 initialization failed:', error);
  }
  
  // Check if Anthropic API key is configured
  if (process.env.ANTHROPIC_API_KEY && process.env.ANTHROPIC_API_KEY !== 'your_anthropic_api_key_here') {
    console.log('\n✅ Anthropic API key configured');
  } else {
    console.log('\n⚠️  Anthropic API key not configured - check your .env file');
  }
  
  // Check if OpenRouter API key is configured
  if (openRouterService.isConfigured()) {
    console.log('✅ OpenRouter API key configured');
    console.log('🌐 OpenRouter endpoints available at /api/openrouter/*');
  } else {
    console.log('⚠️  OpenRouter API key not configured - check your .env file');
    console.log('🔧 To use OpenRouter, set OPENROUTER_API_KEY in your .env file');
  }
});

// Export rate limiters for use in other modules if needed
export { apiLimiter, contentGenerationLimiter, generalLimiter };
