import dotenv from 'dotenv';
import express, { Request, Response, NextFunction } from 'express';

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;
const NODE_ENV = process.env.NODE_ENV || 'development';

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

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

// Main endpoint
app.get('/', (req: Request, res: Response) => {
  res.json({
    message: '🤖 Auto Marketing Agent is running!',
    status: 'active',
    environment: NODE_ENV,
    endpoints: {
      health: '/health',
      api: '/api'
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
      'POST /api/campaign - Create marketing campaign (coming soon)',
      'GET /api/analytics - Get analytics data (coming soon)'
    ]
  });
});

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
app.listen(PORT, () => {
  console.log(`🚀 Auto Marketing Agent server running on port ${PORT}`);
  console.log(`📊 Environment: ${NODE_ENV}`);
  console.log(`🔗 Health check: http://localhost:${PORT}/health`);
  console.log(`📡 API: http://localhost:${PORT}/api`);
  
  // Check if Anthropic API key is configured
  if (process.env.ANTHROPIC_API_KEY && process.env.ANTHROPIC_API_KEY !== 'your_anthropic_api_key_here') {
    console.log('✅ Anthropic API key configured');
  } else {
    console.log('⚠️  Anthropic API key not configured - check your .env file');
  }
});
