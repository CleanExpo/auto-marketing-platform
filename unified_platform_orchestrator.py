"""
Unified Platform Orchestrator
Integrates JavaScript and Python components for complete automation
"""

import asyncio
import json
import subprocess
import aiohttp
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import websockets
import logging
from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
import uvicorn
import numpy as np
from collections import defaultdict

# Import our Python modules
from content_transformation_engine import (
    ContentTransformationEngine,
    ContentIdea,
    ContentType,
    PlatformName
)
from viral_content_analyzer import ViralContentAnalyzer
from automated_content_system import AutomatedContentSystem, AdaptationStrategy
from platform_automation import PlatformSpecialist
from cpu_manager import get_cpu_manager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProcessingMode(Enum):
    """Content processing modes"""
    VOICE_TO_CAMPAIGN = "voice_to_campaign"
    TEXT_TO_MULTI = "text_to_multi"
    VIDEO_GENERATION = "video_generation"
    FULL_AUTO = "full_auto"
    ANALYSIS_ONLY = "analysis_only"

class IntegrationStatus(Enum):
    """Integration system status"""
    READY = "ready"
    PROCESSING = "processing"
    ERROR = "error"
    SYNCING = "syncing"

@dataclass
class UnifiedContent:
    """Unified content structure for both systems"""
    id: str
    core_message: str
    target_persona: str
    hook: str
    content_pillars: List[str]
    visual_elements: str
    call_to_action: str
    platforms: List[str]
    tone: str
    branding_elements: str
    
    # Additional fields from Python system
    content_type: ContentType
    keywords: List[str] = field(default_factory=list)
    hashtags: List[str] = field(default_factory=list)
    
    # Performance tracking
    optimization_scores: Dict[str, float] = field(default_factory=dict)
    viral_potential: Dict[str, float] = field(default_factory=dict)
    
    # Generation metadata
    created_at: datetime = field(default_factory=datetime.now)
    processing_mode: ProcessingMode = ProcessingMode.FULL_AUTO
    source_system: str = "unified"

# Pydantic models for API
class VoiceInputRequest(BaseModel):
    audio_data: str  # Base64 encoded audio
    processing_mode: str = "voice_to_campaign"
    target_platforms: List[str] = []

class ContentGenerationRequest(BaseModel):
    message: str
    persona: str
    hook: str
    platforms: List[str] = ["all"]
    generate_video: bool = False
    optimization_level: str = "high"

class CampaignRequest(BaseModel):
    name: str
    ideas: List[Dict[str, Any]]
    platforms: List[str]
    strategy: str = "waterfall"
    duration_days: int = 30
    auto_publish: bool = False

class UnifiedPlatformOrchestrator:
    """Orchestrates both JavaScript and Python platform systems"""
    
    def __init__(self):
        self.base_path = Path("C:/Auto Marketing")
        self.node_path = self.base_path / "node_modules"
        
        # Initialize Python components
        self.transformation_engine = ContentTransformationEngine()
        self.viral_analyzer = ViralContentAnalyzer()
        self.automation_system = AutomatedContentSystem()
        self.platform_specialist = PlatformSpecialist("unified-platform")
        self.cpu_manager = get_cpu_manager(max_cpu=75.0)
        
        # JavaScript bridge
        self.js_engine_port = 3000
        self.js_process = None
        
        # State management
        self.active_sessions: Dict[str, Dict] = {}
        self.processing_queue: List[UnifiedContent] = []
        self.performance_cache: Dict[str, Any] = {}
        
        # API setup
        self.app = FastAPI(title="Unified Platform Orchestrator")
        self._setup_api_routes()
        
        # WebSocket for real-time updates
        self.websocket_clients = set()
        
        # Status
        self.status = IntegrationStatus.READY
    
    def _setup_api_routes(self):
        """Setup FastAPI routes"""
        
        # CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        @self.app.get("/")
        async def root():
            return {"status": self.status.value, "message": "Unified Platform Orchestrator Active"}
        
        @self.app.post("/api/voice-input")
        async def process_voice(request: VoiceInputRequest):
            """Process voice input to generate content"""
            return await self.process_voice_input(request)
        
        @self.app.post("/api/generate-content")
        async def generate_content(request: ContentGenerationRequest):
            """Generate multi-platform content"""
            return await self.generate_unified_content(request)
        
        @self.app.post("/api/create-campaign")
        async def create_campaign(request: CampaignRequest):
            """Create automated campaign"""
            return await self.create_unified_campaign(request)
        
        @self.app.get("/api/analytics/viral-report")
        async def get_viral_report(platform: Optional[str] = None):
            """Get viral content analysis report"""
            return await self.get_viral_analysis(platform)
        
        @self.app.get("/api/performance/{campaign_id}")
        async def get_performance(campaign_id: str):
            """Get campaign performance metrics"""
            return await self.get_campaign_performance(campaign_id)
        
        @self.app.post("/api/veo3/storyboard")
        async def generate_storyboard(content: Dict[str, Any]):
            """Generate Veo3 video storyboard"""
            return await self.generate_veo_storyboard(content)
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket):
            """WebSocket for real-time updates"""
            await self.handle_websocket(websocket)
        
        @self.app.get("/api/status")
        async def get_status():
            """Get system status"""
            return {
                "status": self.status.value,
                "js_engine": "running" if self.js_process else "stopped",
                "active_sessions": len(self.active_sessions),
                "queue_size": len(self.processing_queue)
            }
        
        @self.app.post("/api/optimize/{content_id}")
        async def optimize_content(content_id: str):
            """Auto-optimize content based on performance"""
            return await self.automation_system.auto_optimize_content(content_id)
    
    async def start_js_engine(self):
        """Start the JavaScript platform engine"""
        try:
            # Create Node.js server file if it doesn't exist
            await self._create_js_server()
            
            # Start Node.js process
            self.js_process = subprocess.Popen(
                ["node", "platform_server.js"],
                cwd=self.base_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for server to start
            await asyncio.sleep(2)
            
            # Test connection
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://localhost:{self.js_engine_port}/health") as resp:
                    if resp.status == 200:
                        logger.info("JavaScript engine started successfully")
                        return True
                        
        except Exception as e:
            logger.error(f"Failed to start JavaScript engine: {e}")
            return False
    
    async def _create_js_server(self):
        """Create Node.js server wrapper for the JavaScript engine"""
        
        server_code = """
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const PlatformAutomationEngine = require('./PlatformAutomationEngine');

const app = express();
const port = 3000;

app.use(cors());
app.use(bodyParser.json({ limit: '50mb' }));
app.use(bodyParser.urlencoded({ extended: true, limit: '50mb' }));

const engine = new PlatformAutomationEngine();

// Health check
app.get('/health', (req, res) => {
    res.json({ status: 'healthy', engine: 'running' });
});

// Generate platform content
app.post('/generate', async (req, res) => {
    try {
        const { content, platforms } = req.body;
        const result = await engine.generatePlatformContent(content, platforms);
        res.json(result);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Generate Veo storyboard
app.post('/veo-storyboard', async (req, res) => {
    try {
        const { content, platform } = req.body;
        const result = await engine.generateVeoStoryboard(content, platform);
        res.json(result);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Process voice input
app.post('/voice-process', async (req, res) => {
    try {
        const { audioBuffer } = req.body;
        const result = await engine.processVoiceInput(audioBuffer);
        res.json(result);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Speech to text
app.post('/speech-to-text', async (req, res) => {
    try {
        const { audioBuffer } = req.body;
        const result = await engine.speechToText(audioBuffer);
        res.json({ transcription: result });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Reason about idea
app.post('/reason-idea', async (req, res) => {
    try {
        const { text } = req.body;
        const result = await engine.reasonAboutIdea(text);
        res.json({ reasoning: result });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Convert to computer language
app.post('/convert-structured', async (req, res) => {
    try {
        const { idea } = req.body;
        const result = await engine.convertToComputerLanguage(idea);
        res.json(result);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.listen(port, () => {
    console.log(`Platform Automation Server running at http://localhost:${port}`);
});
"""
        
        server_file = self.base_path / "platform_server.js"
        with open(server_file, 'w') as f:
            f.write(server_code)
        
        logger.info("JavaScript server file created")
    
    async def call_js_engine(self, endpoint: str, data: Dict) -> Dict:
        """Call JavaScript engine API"""
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"http://localhost:{self.js_engine_port}/{endpoint}"
                async with session.post(url, json=data) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    else:
                        error_text = await resp.text()
                        logger.error(f"JS Engine error: {error_text}")
                        return {"error": error_text}
        except Exception as e:
            logger.error(f"Failed to call JS engine: {e}")
            return {"error": str(e)}
    
    async def process_voice_input(self, request: VoiceInputRequest) -> Dict:
        """Process voice input through both systems"""
        
        await self.cpu_manager.check_and_throttle()
        self.status = IntegrationStatus.PROCESSING
        
        try:
            # Step 1: Convert voice to structured data via JS engine
            voice_result = await self.call_js_engine("voice-process", {
                "audioBuffer": request.audio_data
            })
            
            if "error" in voice_result:
                raise Exception(voice_result["error"])
            
            # Step 2: Create UnifiedContent from voice data
            unified_content = UnifiedContent(
                id=self._generate_content_id(),
                core_message=voice_result.get("coreMessage", ""),
                target_persona=voice_result.get("targetPersona", ""),
                hook=voice_result.get("hook", ""),
                content_pillars=voice_result.get("contentPillars", []),
                visual_elements=voice_result.get("visualElements", ""),
                call_to_action=voice_result.get("callToAction", ""),
                platforms=voice_result.get("platforms", request.target_platforms),
                tone=voice_result.get("tone", ""),
                branding_elements=voice_result.get("brandingElements", ""),
                content_type=self._determine_content_type(voice_result),
                processing_mode=ProcessingMode.VOICE_TO_CAMPAIGN
            )
            
            # Step 3: Generate platform-specific content
            platform_content = await self._generate_platform_content(unified_content)
            
            # Step 4: Analyze viral potential
            viral_analysis = await self._analyze_viral_potential(unified_content, platform_content)
            
            # Step 5: Create campaign if requested
            campaign_result = None
            if request.processing_mode == "voice_to_campaign":
                campaign_result = await self._create_campaign_from_voice(
                    unified_content,
                    platform_content
                )
            
            # Broadcast to WebSocket clients
            await self._broadcast_update({
                "type": "voice_processed",
                "content_id": unified_content.id,
                "platforms": unified_content.platforms
            })
            
            self.status = IntegrationStatus.READY
            
            return {
                "success": True,
                "content_id": unified_content.id,
                "structured_content": {
                    "core_message": unified_content.core_message,
                    "hook": unified_content.hook,
                    "platforms": unified_content.platforms
                },
                "platform_content": platform_content,
                "viral_analysis": viral_analysis,
                "campaign": campaign_result
            }
            
        except Exception as e:
            self.status = IntegrationStatus.ERROR
            logger.error(f"Voice processing error: {e}")
            return {"success": False, "error": str(e)}
    
    async def generate_unified_content(self, request: ContentGenerationRequest) -> Dict:
        """Generate content using both systems"""
        
        await self.cpu_manager.check_and_throttle()
        self.status = IntegrationStatus.PROCESSING
        
        try:
            # Use JS engine for initial generation
            js_content = await self.call_js_engine("generate", {
                "content": {
                    "message": request.message,
                    "persona": request.persona,
                    "hook": request.hook
                },
                "platforms": request.platforms
            })
            
            # Create ContentIdea for Python system
            content_idea = ContentIdea(
                title=request.hook,
                description=request.message,
                content_type=ContentType.EDUCATIONAL,  # Default, could be dynamic
                target_audience=request.persona,
                key_message=request.message,
                call_to_action="Learn more and take action",
                keywords=self._extract_keywords(request.message),
                hashtags=self._generate_hashtags(request.message)
            )
            
            # Use Python system for optimization
            python_content = await self.transformation_engine.transform_content(content_idea)
            
            # Merge results from both systems
            merged_results = self._merge_platform_content(js_content, python_content)
            
            # Generate video storyboard if requested
            video_storyboard = None
            if request.generate_video:
                video_storyboard = await self.generate_veo_storyboard({
                    "content": request.dict(),
                    "platform": "youtube"  # Default to YouTube for video
                })
            
            # Analyze viral potential
            viral_scores = {}
            for platform in merged_results:
                score = await self._calculate_unified_viral_score(
                    merged_results[platform],
                    platform
                )
                viral_scores[platform] = score
            
            # Store in session
            session_id = self._generate_content_id()
            self.active_sessions[session_id] = {
                "content": merged_results,
                "viral_scores": viral_scores,
                "created_at": datetime.now().isoformat()
            }
            
            self.status = IntegrationStatus.READY
            
            return {
                "success": True,
                "session_id": session_id,
                "content": merged_results,
                "viral_scores": viral_scores,
                "video_storyboard": video_storyboard,
                "optimization_level": request.optimization_level
            }
            
        except Exception as e:
            self.status = IntegrationStatus.ERROR
            logger.error(f"Content generation error: {e}")
            return {"success": False, "error": str(e)}
    
    async def create_unified_campaign(self, request: CampaignRequest) -> Dict:
        """Create campaign using both systems"""
        
        await self.cpu_manager.check_and_throttle()
        
        try:
            # Convert ideas to ContentIdea objects
            content_ideas = []
            for idea_data in request.ideas:
                content_idea = ContentIdea(
                    title=idea_data.get("title", ""),
                    description=idea_data.get("description", ""),
                    content_type=ContentType[idea_data.get("content_type", "EDUCATIONAL").upper()],
                    target_audience=idea_data.get("target_audience", ""),
                    key_message=idea_data.get("key_message", ""),
                    call_to_action=idea_data.get("call_to_action", ""),
                    keywords=idea_data.get("keywords", []),
                    hashtags=idea_data.get("hashtags", [])
                )
                content_ideas.append(content_idea)
            
            # Convert platform strings to PlatformName enums
            platforms = [PlatformName[p.upper()] for p in request.platforms]
            
            # Create campaign through Python system
            campaign = await self.automation_system.create_campaign(
                name=request.name,
                content_ideas=content_ideas,
                platforms=platforms,
                strategy=AdaptationStrategy[request.strategy.upper()],
                duration_days=request.duration_days
            )
            
            # Enhance with JS engine optimizations
            for scheduled_content in campaign.scheduled_content:
                js_optimization = await self.call_js_engine("generate", {
                    "content": {
                        "message": scheduled_content.description,
                        "persona": content_ideas[0].target_audience,
                        "hook": scheduled_content.title
                    },
                    "platforms": scheduled_content.platform.value
                })
                
                # Update optimization scores
                if scheduled_content.platform.value in js_optimization:
                    platform_data = js_optimization[scheduled_content.platform.value]
                    scheduled_content.platform_content.viral_potential = max(
                        scheduled_content.platform_content.viral_potential,
                        platform_data.get("optimizationScore", 0) / 100
                    )
            
            # Setup auto-publishing if requested
            if request.auto_publish:
                asyncio.create_task(self.automation_system.execute_publishing_queue())
            
            return {
                "success": True,
                "campaign_id": campaign.campaign_id,
                "name": campaign.name,
                "total_posts": len(campaign.scheduled_content),
                "platforms": request.platforms,
                "strategy": request.strategy,
                "auto_publish": request.auto_publish,
                "schedule": [
                    {
                        "platform": sc.platform.value,
                        "title": sc.title,
                        "scheduled_time": sc.scheduled_time.isoformat(),
                        "viral_potential": sc.platform_content.viral_potential
                    }
                    for sc in campaign.scheduled_content[:10]  # First 10 items
                ]
            }
            
        except Exception as e:
            logger.error(f"Campaign creation error: {e}")
            return {"success": False, "error": str(e)}
    
    async def generate_veo_storyboard(self, content: Dict[str, Any]) -> Dict:
        """Generate Veo3 video storyboard"""
        
        await self.cpu_manager.check_and_throttle()
        
        try:
            # Call JS engine for storyboard generation
            storyboard = await self.call_js_engine("veo-storyboard", content)
            
            if "error" in storyboard:
                raise Exception(storyboard["error"])
            
            # Enhance with Python system insights
            platform = content.get("platform", "youtube")
            platform_specs = self.transformation_engine.platform_strategies.get(platform, {})
            
            # Add platform-specific optimizations
            enhanced_storyboard = {
                **storyboard,
                "platform_optimizations": {
                    "duration": platform_specs.get("optimal_duration", "60 seconds"),
                    "aspect_ratio": platform_specs.get("aspect_ratio", "16:9"),
                    "key_moments": self._identify_key_moments(storyboard),
                    "thumbnail_frames": self._suggest_thumbnail_frames(storyboard)
                },
                "generation_ready": True,
                "estimated_viral_score": await self._estimate_video_viral_score(
                    storyboard,
                    platform
                )
            }
            
            return enhanced_storyboard
            
        except Exception as e:
            logger.error(f"Veo3 storyboard error: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_viral_analysis(self, platform: Optional[str] = None) -> Dict:
        """Get comprehensive viral content analysis"""
        
        await self.cpu_manager.check_and_throttle()
        
        try:
            # Get report from Python analyzer
            platform_enum = PlatformName[platform.upper()] if platform else None
            report = await self.viral_analyzer.generate_viral_report(platform_enum)
            
            # Add real-time insights
            report["real_time_trends"] = await self._get_real_time_trends(platform)
            report["optimization_opportunities"] = await self._identify_optimization_opportunities(report)
            
            return report
            
        except Exception as e:
            logger.error(f"Viral analysis error: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_campaign_performance(self, campaign_id: str) -> Dict:
        """Get detailed campaign performance metrics"""
        
        await self.cpu_manager.check_and_throttle()
        
        try:
            # Get performance from Python system
            report = await self.automation_system.generate_performance_report(campaign_id)
            
            # Add advanced analytics
            if campaign_id in report["campaigns"]:
                campaign_data = report["campaigns"][campaign_id]
                
                # Calculate additional metrics
                campaign_data["advanced_metrics"] = {
                    "virality_rate": self._calculate_virality_rate(campaign_data),
                    "engagement_trend": self._calculate_engagement_trend(campaign_data),
                    "platform_efficiency": self._calculate_platform_efficiency(report),
                    "roi_estimate": self._estimate_roi(campaign_data)
                }
            
            return report
            
        except Exception as e:
            logger.error(f"Performance report error: {e}")
            return {"success": False, "error": str(e)}
    
    async def handle_websocket(self, websocket):
        """Handle WebSocket connections for real-time updates"""
        
        self.websocket_clients.add(websocket)
        try:
            await websocket.accept()
            await websocket.send_json({"type": "connected", "status": "ready"})
            
            while True:
                # Keep connection alive and handle messages
                data = await websocket.receive_json()
                
                if data.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})
                elif data.get("type") == "subscribe":
                    # Handle subscription to specific events
                    pass
                    
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
        finally:
            self.websocket_clients.discard(websocket)
    
    async def _broadcast_update(self, message: Dict):
        """Broadcast update to all WebSocket clients"""
        
        for client in self.websocket_clients:
            try:
                await client.send_json(message)
            except:
                self.websocket_clients.discard(client)
    
    def _determine_content_type(self, voice_data: Dict) -> ContentType:
        """Determine content type from voice data"""
        
        tone = voice_data.get("tone", "").lower()
        message = voice_data.get("coreMessage", "").lower()
        
        if "education" in message or "learn" in message or "how" in message:
            return ContentType.EDUCATIONAL
        elif "fun" in tone or "entertain" in message:
            return ContentType.ENTERTAINMENT
        elif "inspire" in tone or "motivat" in message:
            return ContentType.INSPIRATIONAL
        elif "product" in message or "service" in message or "offer" in message:
            return ContentType.PROMOTIONAL
        elif "community" in message or "together" in message:
            return ContentType.COMMUNITY
        elif "news" in message or "announce" in message:
            return ContentType.NEWS
        elif "behind" in message or "process" in message:
            return ContentType.BEHIND_SCENES
        else:
            return ContentType.EDUCATIONAL  # Default
    
    def _generate_content_id(self) -> str:
        """Generate unique content ID"""
        
        import hashlib
        timestamp = datetime.now().isoformat()
        return hashlib.md5(timestamp.encode()).hexdigest()[:12]
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        
        # Simple keyword extraction - in production use NLP
        import re
        words = re.findall(r'\b\w+\b', text.lower())
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        keywords = [w for w in words if w not in stop_words and len(w) > 3]
        
        # Get unique keywords
        return list(set(keywords))[:10]
    
    def _generate_hashtags(self, text: str) -> List[str]:
        """Generate hashtags from text"""
        
        keywords = self._extract_keywords(text)
        hashtags = [f"#{k.capitalize()}" for k in keywords[:5]]
        return hashtags
    
    async def _generate_platform_content(self, unified_content: UnifiedContent) -> Dict:
        """Generate platform-specific content from unified content"""
        
        # Create ContentIdea
        content_idea = ContentIdea(
            title=unified_content.hook,
            description=unified_content.core_message,
            content_type=unified_content.content_type,
            target_audience=unified_content.target_persona,
            key_message=unified_content.core_message,
            call_to_action=unified_content.call_to_action,
            keywords=unified_content.keywords,
            hashtags=unified_content.hashtags
        )
        
        # Transform for all platforms
        platform_content = await self.transformation_engine.transform_content(content_idea)
        
        # Convert to dict format
        result = {}
        for platform, content in platform_content.items():
            result[platform] = {
                "title": content.title,
                "description": content.description,
                "hashtags": content.hashtags,
                "optimal_time": content.optimal_time,
                "viral_potential": content.viral_potential,
                "estimated_reach": content.estimated_reach
            }
        
        return result
    
    async def _analyze_viral_potential(self, 
                                      unified_content: UnifiedContent,
                                      platform_content: Dict) -> Dict:
        """Analyze viral potential across platforms"""
        
        analysis = {}
        
        for platform, content in platform_content.items():
            prediction = await self.viral_analyzer.predict_viral_potential(
                title=content.get("title", ""),
                content_type=unified_content.content_type,
                platform=PlatformName[platform.upper()],
                hashtags=content.get("hashtags", [])
            )
            
            analysis[platform] = {
                "viral_score": prediction["viral_potential_score"],
                "likelihood": prediction["likelihood"],
                "expected_reach": prediction["expected_reach"],
                "recommendations": prediction.get("recommended_optimizations", [])
            }
        
        return analysis
    
    async def _create_campaign_from_voice(self,
                                         unified_content: UnifiedContent,
                                         platform_content: Dict) -> Dict:
        """Create campaign from voice-processed content"""
        
        # Create ContentIdea from unified content
        content_idea = ContentIdea(
            title=unified_content.hook,
            description=unified_content.core_message,
            content_type=unified_content.content_type,
            target_audience=unified_content.target_persona,
            key_message=unified_content.core_message,
            call_to_action=unified_content.call_to_action,
            keywords=unified_content.keywords,
            hashtags=unified_content.hashtags
        )
        
        # Convert platform strings to enums
        platforms = [PlatformName[p.upper()] for p in unified_content.platforms 
                    if p.upper() in [e.name for e in PlatformName]]
        
        # Create campaign
        campaign = await self.automation_system.create_campaign(
            name=f"Voice Campaign - {unified_content.hook[:30]}",
            content_ideas=[content_idea],
            platforms=platforms,
            strategy=AdaptationStrategy.WATERFALL,
            duration_days=7  # Shorter for voice campaigns
        )
        
        return {
            "campaign_id": campaign.campaign_id,
            "name": campaign.name,
            "posts_scheduled": len(campaign.scheduled_content)
        }
    
    def _merge_platform_content(self, js_content: Dict, python_content: Dict) -> Dict:
        """Merge content from both systems for best results"""
        
        merged = {}
        
        for platform in set(list(js_content.keys()) + list(python_content.keys())):
            if platform in js_content and platform in python_content:
                # Merge both sources
                py_data = python_content[platform]
                js_data = js_content.get(platform, {})
                
                merged[platform] = {
                    "title": py_data.title,
                    "description": js_data.get("adaptedContent", py_data.description),
                    "hashtags": py_data.hashtags,
                    "optimal_time": py_data.optimal_time,
                    "viral_potential": max(
                        py_data.viral_potential,
                        js_data.get("optimizationScore", 0) / 100
                    ),
                    "estimated_reach": py_data.estimated_reach,
                    "js_optimization": js_data.get("optimizationScore", 0),
                    "py_viral_score": py_data.viral_potential * 100
                }
            elif platform in python_content:
                # Python only
                py_data = python_content[platform]
                merged[platform] = {
                    "title": py_data.title,
                    "description": py_data.description,
                    "hashtags": py_data.hashtags,
                    "optimal_time": py_data.optimal_time,
                    "viral_potential": py_data.viral_potential,
                    "estimated_reach": py_data.estimated_reach
                }
            elif platform in js_content:
                # JS only
                js_data = js_content[platform]
                merged[platform] = {
                    "title": platform.upper(),
                    "description": js_data.get("adaptedContent", ""),
                    "hashtags": [],
                    "optimal_time": "12:00 PM",
                    "viral_potential": js_data.get("optimizationScore", 0) / 100,
                    "estimated_reach": 1000
                }
        
        return merged
    
    async def _calculate_unified_viral_score(self, content: Dict, platform: str) -> float:
        """Calculate unified viral score combining both systems"""
        
        js_score = content.get("js_optimization", 0) / 100
        py_score = content.get("py_viral_score", 0) / 100
        
        # Weighted average favoring Python's viral analysis
        unified_score = (py_score * 0.7 + js_score * 0.3)
        
        # Platform boost factors
        platform_boosts = {
            "tiktok": 1.2,
            "instagram": 1.1,
            "youtube": 1.15,
            "twitter": 1.05
        }
        
        boost = platform_boosts.get(platform.lower(), 1.0)
        
        return min(unified_score * boost, 1.0)
    
    def _identify_key_moments(self, storyboard: Dict) -> List[Dict]:
        """Identify key moments in video storyboard"""
        
        # Extract key moments from storyboard text
        # This is simplified - in production use more sophisticated analysis
        
        return [
            {"time": "0:00-0:03", "description": "Hook moment"},
            {"time": "0:10-0:15", "description": "Key revelation"},
            {"time": "0:25-0:30", "description": "Call to action"}
        ]
    
    def _suggest_thumbnail_frames(self, storyboard: Dict) -> List[str]:
        """Suggest best frames for video thumbnail"""
        
        return [
            "Opening hook frame with text overlay",
            "Most visually striking moment",
            "Character/presenter close-up with emotion"
        ]
    
    async def _estimate_video_viral_score(self, storyboard: Dict, platform: str) -> float:
        """Estimate viral potential of video from storyboard"""
        
        # Base score
        score = 0.5
        
        # Check for viral elements in storyboard
        storyboard_text = str(storyboard).lower()
        
        viral_elements = {
            "hook": 0.1,
            "transform": 0.1,
            "surprise": 0.1,
            "emotion": 0.1,
            "trend": 0.1
        }
        
        for element, boost in viral_elements.items():
            if element in storyboard_text:
                score += boost
        
        # Platform-specific adjustments
        if platform == "tiktok" or platform == "youtube":
            score *= 1.2
        
        return min(score, 1.0)
    
    async def _get_real_time_trends(self, platform: Optional[str]) -> Dict:
        """Get real-time trending topics (simulated)"""
        
        # In production, this would connect to trend APIs
        trends = {
            "youtube": ["AI tools", "productivity", "tutorials"],
            "tiktok": ["trends", "challenges", "transformations"],
            "instagram": ["reels", "aesthetic", "lifestyle"],
            "twitter": ["tech news", "discussions", "threads"],
            "linkedin": ["career", "leadership", "innovation"]
        }
        
        if platform:
            return {platform: trends.get(platform.lower(), [])}
        return trends
    
    async def _identify_optimization_opportunities(self, report: Dict) -> List[str]:
        """Identify optimization opportunities from report data"""
        
        opportunities = []
        
        # Check platform performance
        for platform, data in report.get("platforms", {}).items():
            if data.get("viral_rate", 0) < 0.1:
                opportunities.append(f"Increase viral content on {platform}")
            
            if data.get("avg_engagement_rate", 0) < 0.05:
                opportunities.append(f"Improve engagement hooks for {platform}")
        
        # Check content patterns
        if report.get("viral_patterns"):
            opportunities.append("Apply identified viral patterns to new content")
        
        return opportunities[:5]
    
    def _calculate_virality_rate(self, campaign_data: Dict) -> float:
        """Calculate virality rate for campaign"""
        
        total_posts = campaign_data.get("total_posts", 1)
        # Simplified calculation
        engagement_rate = campaign_data.get("avg_engagement_rate", 0)
        
        if engagement_rate > 0.1:
            return 0.3  # High virality
        elif engagement_rate > 0.05:
            return 0.15  # Medium virality
        else:
            return 0.05  # Low virality
    
    def _calculate_engagement_trend(self, campaign_data: Dict) -> str:
        """Calculate engagement trend"""
        
        # Simplified - in production, analyze time series data
        engagement = campaign_data.get("avg_engagement_rate", 0)
        
        if engagement > 0.07:
            return "increasing"
        elif engagement > 0.03:
            return "stable"
        else:
            return "decreasing"
    
    def _calculate_platform_efficiency(self, report: Dict) -> Dict:
        """Calculate efficiency score for each platform"""
        
        efficiency = {}
        
        for platform, data in report.get("platform_performance", {}).items():
            views = data.get("total_views", 1)
            engagement = data.get("total_engagement", 0)
            posts = data.get("posts", 1)
            
            # Efficiency = engagement per post / views per post
            efficiency[platform] = (engagement / posts) / max(1, views / posts)
        
        return efficiency
    
    def _estimate_roi(self, campaign_data: Dict) -> float:
        """Estimate ROI for campaign"""
        
        # Simplified ROI calculation
        reach = campaign_data.get("total_views", 0)
        engagement = campaign_data.get("total_engagement", 0)
        
        # Assume value per engagement
        value_per_engagement = 0.1  # $0.10
        value_per_view = 0.001  # $0.001
        
        estimated_value = (engagement * value_per_engagement) + (reach * value_per_view)
        
        # Assume cost (would be actual in production)
        estimated_cost = 100  # $100 campaign cost
        
        roi = ((estimated_value - estimated_cost) / estimated_cost) * 100 if estimated_cost > 0 else 0
        
        return roi
    
    async def start(self):
        """Start the orchestrator"""
        
        logger.info("Starting Unified Platform Orchestrator...")
        
        # Start JS engine
        js_started = await self.start_js_engine()
        if not js_started:
            logger.warning("JavaScript engine failed to start, continuing with Python only")
        
        # Start FastAPI server
        config = uvicorn.Config(
            app=self.app,
            host="0.0.0.0",
            port=8000,
            log_level="info"
        )
        server = uvicorn.Server(config)
        
        # Start server in background
        asyncio.create_task(server.serve())
        
        logger.info("Unified Platform Orchestrator is running on http://localhost:8000")
        logger.info("WebSocket available at ws://localhost:8000/ws")
        
        return True
    
    async def stop(self):
        """Stop the orchestrator"""
        
        logger.info("Stopping Unified Platform Orchestrator...")
        
        # Stop JS engine
        if self.js_process:
            self.js_process.terminate()
            self.js_process.wait()
        
        # Close WebSocket connections
        for client in self.websocket_clients:
            await client.close()
        
        self.status = IntegrationStatus.READY
        logger.info("Orchestrator stopped")


# Main execution
async def main():
    """Run the Unified Platform Orchestrator"""
    
    orchestrator = UnifiedPlatformOrchestrator()
    
    # Start the system
    await orchestrator.start()
    
    print("\n" + "="*60)
    print("🚀 UNIFIED PLATFORM ORCHESTRATOR ACTIVE")
    print("="*60)
    print("\nAPI Endpoints:")
    print("  - Dashboard: http://localhost:8000")
    print("  - Voice Input: POST /api/voice-input")
    print("  - Generate Content: POST /api/generate-content")
    print("  - Create Campaign: POST /api/create-campaign")
    print("  - Viral Analysis: GET /api/analytics/viral-report")
    print("  - WebSocket: ws://localhost:8000/ws")
    print("\nFeatures:")
    print("  ✅ Voice-to-Campaign Processing")
    print("  ✅ Multi-Platform Content Generation")
    print("  ✅ Viral Pattern Analysis")
    print("  ✅ Automated Campaign Management")
    print("  ✅ Real-time Performance Tracking")
    print("  ✅ Veo3 Video Storyboard Generation")
    print("\nPress Ctrl+C to stop")
    print("="*60)
    
    # Keep running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await orchestrator.stop()
        print("\nOrchestrator stopped gracefully")

if __name__ == "__main__":
    asyncio.run(main())