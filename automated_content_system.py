"""
Automated Content Adaptation System
Automatically adapts, schedules, and publishes content across all platforms
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import random
import hashlib
from collections import defaultdict

# Import our modules
from content_transformation_engine import (
    ContentTransformationEngine, 
    ContentIdea, 
    ContentType, 
    PlatformName,
    PlatformContent
)
from viral_content_analyzer import ViralContentAnalyzer, ContentMetrics
from platform_automation import PlatformSpecialist
from cpu_manager import get_cpu_manager

class PublishStatus(Enum):
    """Content publish status"""
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"
    PENDING = "pending"
    CANCELLED = "cancelled"

class AdaptationStrategy(Enum):
    """Content adaptation strategies"""
    WATERFALL = "waterfall"  # Start with long-form, cascade to short
    SIMULTANEOUS = "simultaneous"  # Publish everywhere at once
    TEST_AND_SCALE = "test_and_scale"  # Test on one platform first
    VIRAL_CHASE = "viral_chase"  # Focus on trending platforms
    AUDIENCE_FIRST = "audience_first"  # Prioritize by audience presence

@dataclass
class ScheduledContent:
    """Scheduled content item"""
    content_id: str
    platform: PlatformName
    title: str
    description: str
    scheduled_time: datetime
    status: PublishStatus
    platform_content: PlatformContent
    parent_content_id: Optional[str] = None
    performance_metrics: Dict[str, Any] = field(default_factory=dict)
    
@dataclass
class ContentCampaign:
    """Automated content campaign"""
    campaign_id: str
    name: str
    content_ideas: List[ContentIdea]
    strategy: AdaptationStrategy
    platforms: List[PlatformName]
    start_date: datetime
    end_date: datetime
    target_metrics: Dict[str, float]
    scheduled_content: List[ScheduledContent] = field(default_factory=list)
    performance_data: Dict[str, Any] = field(default_factory=dict)

class AutomatedContentSystem:
    """Automated content adaptation and publishing system"""
    
    def __init__(self, project_id: str = None):
        self.project_id = project_id or "auto-marketing"
        self.base_path = Path("C:/Auto Marketing")
        self.automation_path = self.base_path / "automation"
        self.automation_path.mkdir(exist_ok=True)
        
        # Initialize components
        self.transformation_engine = ContentTransformationEngine(project_id)
        self.viral_analyzer = ViralContentAnalyzer(project_id)
        self.platform_specialist = PlatformSpecialist(project_id)
        self.cpu_manager = get_cpu_manager(max_cpu=75.0)
        
        # Content queue and scheduling
        self.content_queue: List[ScheduledContent] = []
        self.active_campaigns: Dict[str, ContentCampaign] = {}
        self.publishing_calendar: Dict[str, List[ScheduledContent]] = defaultdict(list)
        
        # Performance tracking
        self.performance_history: List[Dict] = []
        self.optimization_rules: Dict[str, Any] = self._load_optimization_rules()
        
        # Load existing data
        self._load_automation_data()
    
    def _load_optimization_rules(self) -> Dict[str, Any]:
        """Load content optimization rules"""
        
        return {
            "engagement_thresholds": {
                PlatformName.TIKTOK: 0.15,
                PlatformName.INSTAGRAM: 0.06,
                PlatformName.YOUTUBE: 0.04,
                PlatformName.TWITTER: 0.03,
                PlatformName.LINKEDIN: 0.04,
                PlatformName.FACEBOOK: 0.03,
                PlatformName.PINTEREST: 0.05,
                PlatformName.REDDIT: 0.10
            },
            "repost_intervals": {
                PlatformName.TWITTER: 8,  # hours
                PlatformName.FACEBOOK: 24,
                PlatformName.INSTAGRAM: 48,
                PlatformName.LINKEDIN: 72,
                PlatformName.PINTEREST: 168  # 1 week
            },
            "cross_promotion_delay": {
                "hero_to_support": 2,  # hours
                "support_to_tertiary": 4
            },
            "auto_boost_criteria": {
                "min_engagement_rate": 0.05,
                "min_viral_score": 70,
                "boost_budget": 50  # USD
            }
        }
    
    def _load_automation_data(self):
        """Load existing automation data"""
        
        # Load active campaigns
        campaigns_file = self.automation_path / "active_campaigns.json"
        if campaigns_file.exists():
            with open(campaigns_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for campaign_id, campaign_data in data.items():
                    self.active_campaigns[campaign_id] = self._dict_to_campaign(campaign_data)
        
        # Load content queue
        queue_file = self.automation_path / "content_queue.json"
        if queue_file.exists():
            with open(queue_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data:
                    self.content_queue.append(self._dict_to_scheduled(item))
    
    def _dict_to_campaign(self, data: Dict) -> ContentCampaign:
        """Convert dictionary to ContentCampaign"""
        
        return ContentCampaign(
            campaign_id=data["campaign_id"],
            name=data["name"],
            content_ideas=[ContentIdea(**idea) for idea in data["content_ideas"]],
            strategy=AdaptationStrategy(data["strategy"]),
            platforms=[PlatformName(p) for p in data["platforms"]],
            start_date=datetime.fromisoformat(data["start_date"]),
            end_date=datetime.fromisoformat(data["end_date"]),
            target_metrics=data["target_metrics"],
            scheduled_content=[self._dict_to_scheduled(s) for s in data.get("scheduled_content", [])],
            performance_data=data.get("performance_data", {})
        )
    
    def _dict_to_scheduled(self, data: Dict) -> ScheduledContent:
        """Convert dictionary to ScheduledContent"""
        
        return ScheduledContent(
            content_id=data["content_id"],
            platform=PlatformName(data["platform"]),
            title=data["title"],
            description=data["description"],
            scheduled_time=datetime.fromisoformat(data["scheduled_time"]),
            status=PublishStatus(data["status"]),
            platform_content=PlatformContent(**data["platform_content"]),
            parent_content_id=data.get("parent_content_id"),
            performance_metrics=data.get("performance_metrics", {})
        )
    
    def _generate_content_id(self, title: str, platform: str) -> str:
        """Generate unique content ID"""
        
        timestamp = datetime.now().isoformat()
        hash_input = f"{title}_{platform}_{timestamp}"
        return hashlib.md5(hash_input.encode()).hexdigest()[:12]
    
    async def create_campaign(self,
                            name: str,
                            content_ideas: List[ContentIdea],
                            platforms: List[PlatformName],
                            strategy: AdaptationStrategy = AdaptationStrategy.WATERFALL,
                            duration_days: int = 30,
                            target_metrics: Dict[str, float] = None) -> ContentCampaign:
        """Create and launch an automated content campaign"""
        
        await self.cpu_manager.check_and_throttle()
        
        # Generate campaign ID
        campaign_id = self._generate_content_id(name, "campaign")
        
        # Set default target metrics
        if not target_metrics:
            target_metrics = {
                "total_reach": 100000,
                "avg_engagement_rate": 0.05,
                "viral_content_rate": 0.1
            }
        
        # Create campaign
        campaign = ContentCampaign(
            campaign_id=campaign_id,
            name=name,
            content_ideas=content_ideas,
            strategy=strategy,
            platforms=platforms,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=duration_days),
            target_metrics=target_metrics
        )
        
        # Generate content adaptations for all platforms
        for idea in content_ideas:
            adapted_content = await self.transformation_engine.transform_content(idea)
            
            # Schedule content based on strategy
            scheduled = await self._schedule_content(
                adapted_content,
                campaign,
                idea
            )
            
            campaign.scheduled_content.extend(scheduled)
        
        # Add to active campaigns
        self.active_campaigns[campaign_id] = campaign
        
        # Save campaign
        await self._save_campaign(campaign)
        
        print(f"Campaign '{name}' created with {len(campaign.scheduled_content)} scheduled posts")
        
        return campaign
    
    async def _schedule_content(self,
                               adapted_content: Dict[str, PlatformContent],
                               campaign: ContentCampaign,
                               original_idea: ContentIdea) -> List[ScheduledContent]:
        """Schedule content based on campaign strategy"""
        
        scheduled = []
        
        if campaign.strategy == AdaptationStrategy.WATERFALL:
            scheduled = await self._schedule_waterfall(adapted_content, campaign, original_idea)
            
        elif campaign.strategy == AdaptationStrategy.SIMULTANEOUS:
            scheduled = await self._schedule_simultaneous(adapted_content, campaign, original_idea)
            
        elif campaign.strategy == AdaptationStrategy.TEST_AND_SCALE:
            scheduled = await self._schedule_test_and_scale(adapted_content, campaign, original_idea)
            
        elif campaign.strategy == AdaptationStrategy.VIRAL_CHASE:
            scheduled = await self._schedule_viral_chase(adapted_content, campaign, original_idea)
            
        elif campaign.strategy == AdaptationStrategy.AUDIENCE_FIRST:
            scheduled = await self._schedule_audience_first(adapted_content, campaign, original_idea)
        
        return scheduled
    
    async def _schedule_waterfall(self,
                                 adapted_content: Dict[str, PlatformContent],
                                 campaign: ContentCampaign,
                                 original_idea: ContentIdea) -> List[ScheduledContent]:
        """Schedule content in waterfall pattern"""
        
        scheduled = []
        base_time = datetime.now() + timedelta(hours=1)
        
        # Priority order for waterfall
        platform_order = [
            PlatformName.YOUTUBE,
            PlatformName.LINKEDIN,
            PlatformName.FACEBOOK,
            PlatformName.INSTAGRAM,
            PlatformName.TWITTER,
            PlatformName.TIKTOK,
            PlatformName.PINTEREST,
            PlatformName.REDDIT
        ]
        
        parent_id = None
        delay_hours = 0
        
        for platform in platform_order:
            if platform in campaign.platforms and platform.value in adapted_content:
                content = adapted_content[platform.value]
                
                # Calculate optimal time with waterfall delay
                scheduled_time = base_time + timedelta(hours=delay_hours)
                
                # Parse optimal time string and adjust
                scheduled_time = self._parse_optimal_time(
                    content.optimal_time,
                    scheduled_time
                )
                
                # Create scheduled content
                scheduled_item = ScheduledContent(
                    content_id=self._generate_content_id(content.title, platform.value),
                    platform=platform,
                    title=content.title,
                    description=content.description,
                    scheduled_time=scheduled_time,
                    status=PublishStatus.SCHEDULED,
                    platform_content=content,
                    parent_content_id=parent_id
                )
                
                scheduled.append(scheduled_item)
                
                # Set as parent for next platforms
                if not parent_id:
                    parent_id = scheduled_item.content_id
                
                # Add delay for next platform
                delay_hours += self.optimization_rules["cross_promotion_delay"]["hero_to_support"]
        
        return scheduled
    
    async def _schedule_simultaneous(self,
                                    adapted_content: Dict[str, PlatformContent],
                                    campaign: ContentCampaign,
                                    original_idea: ContentIdea) -> List[ScheduledContent]:
        """Schedule content simultaneously across platforms"""
        
        scheduled = []
        
        # Find best common time
        base_time = self._find_best_common_time(campaign.platforms)
        
        for platform in campaign.platforms:
            if platform.value in adapted_content:
                content = adapted_content[platform.value]
                
                scheduled_item = ScheduledContent(
                    content_id=self._generate_content_id(content.title, platform.value),
                    platform=platform,
                    title=content.title,
                    description=content.description,
                    scheduled_time=base_time,
                    status=PublishStatus.SCHEDULED,
                    platform_content=content
                )
                
                scheduled.append(scheduled_item)
        
        return scheduled
    
    async def _schedule_test_and_scale(self,
                                      adapted_content: Dict[str, PlatformContent],
                                      campaign: ContentCampaign,
                                      original_idea: ContentIdea) -> List[ScheduledContent]:
        """Test on one platform first, then scale if successful"""
        
        scheduled = []
        
        # Choose test platform (highest viral potential)
        test_platform = max(
            campaign.platforms,
            key=lambda p: adapted_content.get(p.value, PlatformContent(
                platform=p, format="", title="", description="", hashtags=[],
                optimal_time="", media_specs={}, engagement_hooks=[],
                estimated_reach=0, viral_potential=0
            )).viral_potential
        )
        
        if test_platform.value in adapted_content:
            test_content = adapted_content[test_platform.value]
            test_time = datetime.now() + timedelta(hours=1)
            
            # Schedule test content
            test_item = ScheduledContent(
                content_id=self._generate_content_id(test_content.title, test_platform.value),
                platform=test_platform,
                title=test_content.title,
                description=test_content.description,
                scheduled_time=test_time,
                status=PublishStatus.SCHEDULED,
                platform_content=test_content
            )
            
            scheduled.append(test_item)
            
            # Schedule others for later (pending test results)
            scale_time = test_time + timedelta(hours=24)
            
            for platform in campaign.platforms:
                if platform != test_platform and platform.value in adapted_content:
                    content = adapted_content[platform.value]
                    
                    scheduled_item = ScheduledContent(
                        content_id=self._generate_content_id(content.title, platform.value),
                        platform=platform,
                        title=content.title,
                        description=content.description,
                        scheduled_time=scale_time,
                        status=PublishStatus.PENDING,  # Pending test results
                        platform_content=content,
                        parent_content_id=test_item.content_id
                    )
                    
                    scheduled.append(scheduled_item)
        
        return scheduled
    
    async def _schedule_viral_chase(self,
                                  adapted_content: Dict[str, PlatformContent],
                                  campaign: ContentCampaign,
                                  original_idea: ContentIdea) -> List[ScheduledContent]:
        """Focus on platforms with highest viral potential"""
        
        scheduled = []
        
        # Sort platforms by viral potential
        sorted_platforms = sorted(
            campaign.platforms,
            key=lambda p: adapted_content.get(p.value, PlatformContent(
                platform=p, format="", title="", description="", hashtags=[],
                optimal_time="", media_specs={}, engagement_hooks=[],
                estimated_reach=0, viral_potential=0
            )).viral_potential,
            reverse=True
        )
        
        base_time = datetime.now() + timedelta(hours=1)
        
        for i, platform in enumerate(sorted_platforms[:3]):  # Focus on top 3
            if platform.value in adapted_content:
                content = adapted_content[platform.value]
                
                # Stagger high-potential content slightly
                scheduled_time = base_time + timedelta(hours=i * 2)
                
                scheduled_item = ScheduledContent(
                    content_id=self._generate_content_id(content.title, platform.value),
                    platform=platform,
                    title=content.title,
                    description=content.description,
                    scheduled_time=scheduled_time,
                    status=PublishStatus.SCHEDULED,
                    platform_content=content
                )
                
                scheduled.append(scheduled_item)
        
        return scheduled
    
    async def _schedule_audience_first(self,
                                     adapted_content: Dict[str, PlatformContent],
                                     campaign: ContentCampaign,
                                     original_idea: ContentIdea) -> List[ScheduledContent]:
        """Prioritize platforms by audience presence"""
        
        scheduled = []
        
        # Audience size estimates (would be from analytics in production)
        audience_sizes = {
            PlatformName.FACEBOOK: 10000,
            PlatformName.INSTAGRAM: 8000,
            PlatformName.YOUTUBE: 5000,
            PlatformName.TIKTOK: 3000,
            PlatformName.LINKEDIN: 2000,
            PlatformName.TWITTER: 1500,
            PlatformName.PINTEREST: 1000,
            PlatformName.REDDIT: 500
        }
        
        # Sort by audience size
        sorted_platforms = sorted(
            campaign.platforms,
            key=lambda p: audience_sizes.get(p, 0),
            reverse=True
        )
        
        base_time = datetime.now() + timedelta(hours=1)
        
        for platform in sorted_platforms:
            if platform.value in adapted_content:
                content = adapted_content[platform.value]
                
                scheduled_item = ScheduledContent(
                    content_id=self._generate_content_id(content.title, platform.value),
                    platform=platform,
                    title=content.title,
                    description=content.description,
                    scheduled_time=base_time,
                    status=PublishStatus.SCHEDULED,
                    platform_content=content
                )
                
                scheduled.append(scheduled_item)
        
        return scheduled
    
    def _parse_optimal_time(self, time_str: str, base_date: datetime) -> datetime:
        """Parse optimal time string and create datetime"""
        
        # Simple parsing - in production, use more sophisticated parsing
        if "AM" in time_str or "PM" in time_str:
            # Extract hour
            parts = time_str.split()
            for part in parts:
                if ":" in part:
                    hour_str = part.split(":")[0]
                    try:
                        hour = int(hour_str)
                        if "PM" in time_str and hour < 12:
                            hour += 12
                        return base_date.replace(hour=hour, minute=0)
                    except:
                        pass
        
        # Default to base date
        return base_date
    
    def _find_best_common_time(self, platforms: List[PlatformName]) -> datetime:
        """Find best time that works for multiple platforms"""
        
        # Simple approach - find overlap in optimal times
        # In production, use more sophisticated algorithm
        
        tomorrow = datetime.now() + timedelta(days=1)
        
        # Common good times across platforms
        if PlatformName.LINKEDIN in platforms:
            return tomorrow.replace(hour=9, minute=0)  # Morning for professionals
        elif PlatformName.TIKTOK in platforms:
            return tomorrow.replace(hour=19, minute=0)  # Evening for Gen Z
        else:
            return tomorrow.replace(hour=12, minute=0)  # Noon as default
    
    async def auto_optimize_content(self, content_id: str) -> Dict[str, Any]:
        """Automatically optimize content based on performance"""
        
        await self.cpu_manager.check_and_throttle()
        
        # Find content in queue
        content = next((c for c in self.content_queue if c.content_id == content_id), None)
        
        if not content:
            return {"error": "Content not found"}
        
        # Analyze current performance
        metrics = ContentMetrics(
            platform=content.platform,
            content_id=content.content_id,
            title=content.title,
            content_type=ContentType.EDUCATIONAL,  # Would be determined from content
            posted_at=content.scheduled_time,
            views=content.performance_metrics.get("views", 0),
            likes=content.performance_metrics.get("likes", 0),
            comments=content.performance_metrics.get("comments", 0),
            shares=content.performance_metrics.get("shares", 0),
            saves=content.performance_metrics.get("saves", 0)
        )
        
        analysis = await self.viral_analyzer.analyze_content(metrics)
        
        optimizations = {}
        
        # Check if content meets boost criteria
        if (analysis["engagement_rate"] >= self.optimization_rules["auto_boost_criteria"]["min_engagement_rate"] or
            analysis["viral_score"] >= self.optimization_rules["auto_boost_criteria"]["min_viral_score"]):
            
            optimizations["boost"] = {
                "recommended": True,
                "budget": self.optimization_rules["auto_boost_criteria"]["boost_budget"],
                "reason": "High engagement/viral potential"
            }
        
        # Check for reposting opportunity
        platform = content.platform
        if platform in self.optimization_rules["repost_intervals"]:
            hours_since = (datetime.now() - content.scheduled_time).total_seconds() / 3600
            if hours_since >= self.optimization_rules["repost_intervals"][platform]:
                optimizations["repost"] = {
                    "recommended": True,
                    "timing": datetime.now() + timedelta(hours=1),
                    "modifications": analysis["improvement_suggestions"]
                }
        
        # Cross-promotion recommendations
        if analysis["viral_score"] >= 70:
            optimizations["cross_promote"] = {
                "recommended": True,
                "platforms": self._get_cross_promotion_platforms(content.platform),
                "timing": "immediate"
            }
        
        # Content modifications
        if analysis["improvement_suggestions"]:
            optimizations["modifications"] = {
                "suggestions": analysis["improvement_suggestions"],
                "priority": "high" if analysis["virality_status"] == "underperforming" else "medium"
            }
        
        return optimizations
    
    def _get_cross_promotion_platforms(self, current_platform: PlatformName) -> List[str]:
        """Get recommended platforms for cross-promotion"""
        
        cross_promotion_map = {
            PlatformName.TIKTOK: [PlatformName.INSTAGRAM, PlatformName.YOUTUBE],
            PlatformName.INSTAGRAM: [PlatformName.FACEBOOK, PlatformName.TIKTOK],
            PlatformName.YOUTUBE: [PlatformName.TWITTER, PlatformName.LINKEDIN],
            PlatformName.TWITTER: [PlatformName.LINKEDIN, PlatformName.REDDIT],
            PlatformName.LINKEDIN: [PlatformName.TWITTER, PlatformName.FACEBOOK],
            PlatformName.FACEBOOK: [PlatformName.INSTAGRAM, PlatformName.LINKEDIN],
            PlatformName.PINTEREST: [PlatformName.INSTAGRAM, PlatformName.FACEBOOK],
            PlatformName.REDDIT: [PlatformName.TWITTER, PlatformName.YOUTUBE]
        }
        
        platforms = cross_promotion_map.get(current_platform, [])
        return [p.value for p in platforms]
    
    async def execute_publishing_queue(self):
        """Execute scheduled content publishing"""
        
        while True:
            await self.cpu_manager.check_and_throttle()
            
            current_time = datetime.now()
            
            # Check for content ready to publish
            for content in self.content_queue:
                if (content.status == PublishStatus.SCHEDULED and 
                    content.scheduled_time <= current_time):
                    
                    # Publish content
                    success = await self._publish_content(content)
                    
                    if success:
                        content.status = PublishStatus.PUBLISHED
                        print(f"Published: {content.title} on {content.platform.value}")
                    else:
                        content.status = PublishStatus.FAILED
                        print(f"Failed to publish: {content.title} on {content.platform.value}")
            
            # Check for pending content (test and scale)
            for content in self.content_queue:
                if content.status == PublishStatus.PENDING and content.parent_content_id:
                    # Check parent performance
                    parent = next((c for c in self.content_queue 
                                 if c.content_id == content.parent_content_id), None)
                    
                    if parent and parent.status == PublishStatus.PUBLISHED:
                        # Check if parent performed well
                        if parent.performance_metrics.get("engagement_rate", 0) >= 0.05:
                            content.status = PublishStatus.SCHEDULED
                            print(f"Approved for publishing: {content.title}")
            
            # Save state
            await self._save_queue_state()
            
            # Wait before next check
            await asyncio.sleep(60)  # Check every minute
    
    async def _publish_content(self, content: ScheduledContent) -> bool:
        """Publish content to platform (simulation)"""
        
        # In production, this would use actual platform APIs
        # For now, we'll simulate publishing
        
        await asyncio.sleep(1)  # Simulate API call
        
        # Simulate performance metrics
        content.performance_metrics = {
            "views": random.randint(100, 10000),
            "likes": random.randint(10, 1000),
            "comments": random.randint(1, 100),
            "shares": random.randint(1, 50),
            "engagement_rate": random.uniform(0.01, 0.15)
        }
        
        # 90% success rate
        return random.random() < 0.9
    
    async def generate_performance_report(self, 
                                         campaign_id: Optional[str] = None) -> Dict[str, Any]:
        """Generate performance report for campaigns"""
        
        await self.cpu_manager.check_and_throttle()
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "campaigns": {},
            "platform_performance": defaultdict(dict),
            "content_performance": [],
            "recommendations": []
        }
        
        # Filter campaigns
        campaigns = {campaign_id: self.active_campaigns[campaign_id]} if campaign_id else self.active_campaigns
        
        for cid, campaign in campaigns.items():
            published_content = [c for c in campaign.scheduled_content 
                               if c.status == PublishStatus.PUBLISHED]
            
            if published_content:
                total_views = sum(c.performance_metrics.get("views", 0) for c in published_content)
                total_engagement = sum(
                    c.performance_metrics.get("likes", 0) +
                    c.performance_metrics.get("comments", 0) +
                    c.performance_metrics.get("shares", 0)
                    for c in published_content
                )
                
                avg_engagement_rate = sum(c.performance_metrics.get("engagement_rate", 0) 
                                         for c in published_content) / len(published_content)
                
                report["campaigns"][cid] = {
                    "name": campaign.name,
                    "strategy": campaign.strategy.value,
                    "total_posts": len(published_content),
                    "total_views": total_views,
                    "total_engagement": total_engagement,
                    "avg_engagement_rate": avg_engagement_rate,
                    "target_achievement": {
                        "reach": total_views / campaign.target_metrics.get("total_reach", 1),
                        "engagement": avg_engagement_rate / campaign.target_metrics.get("avg_engagement_rate", 1)
                    }
                }
                
                # Platform breakdown
                for content in published_content:
                    platform = content.platform.value
                    if platform not in report["platform_performance"]:
                        report["platform_performance"][platform] = {
                            "posts": 0,
                            "total_views": 0,
                            "total_engagement": 0,
                            "avg_engagement_rate": []
                        }
                    
                    report["platform_performance"][platform]["posts"] += 1
                    report["platform_performance"][platform]["total_views"] += content.performance_metrics.get("views", 0)
                    report["platform_performance"][platform]["total_engagement"] += (
                        content.performance_metrics.get("likes", 0) +
                        content.performance_metrics.get("comments", 0) +
                        content.performance_metrics.get("shares", 0)
                    )
                    report["platform_performance"][platform]["avg_engagement_rate"].append(
                        content.performance_metrics.get("engagement_rate", 0)
                    )
        
        # Calculate platform averages
        for platform, data in report["platform_performance"].items():
            if data["avg_engagement_rate"]:
                data["avg_engagement_rate"] = sum(data["avg_engagement_rate"]) / len(data["avg_engagement_rate"])
            else:
                data["avg_engagement_rate"] = 0
        
        # Top performing content
        all_content = []
        for campaign in campaigns.values():
            all_content.extend([c for c in campaign.scheduled_content 
                              if c.status == PublishStatus.PUBLISHED])
        
        top_content = sorted(all_content, 
                           key=lambda x: x.performance_metrics.get("engagement_rate", 0), 
                           reverse=True)[:10]
        
        for content in top_content:
            report["content_performance"].append({
                "title": content.title,
                "platform": content.platform.value,
                "engagement_rate": content.performance_metrics.get("engagement_rate", 0),
                "views": content.performance_metrics.get("views", 0)
            })
        
        # Generate recommendations
        report["recommendations"] = self._generate_performance_recommendations(report)
        
        # Save report
        await self._save_performance_report(report)
        
        return report
    
    def _generate_performance_recommendations(self, report: Dict) -> List[str]:
        """Generate recommendations based on performance data"""
        
        recommendations = []
        
        # Platform performance recommendations
        best_platform = max(report["platform_performance"].items(), 
                          key=lambda x: x[1].get("avg_engagement_rate", 0)) if report["platform_performance"] else None
        
        if best_platform:
            recommendations.append(f"Focus more on {best_platform[0]} - highest engagement rate")
        
        # Campaign strategy recommendations
        for campaign_data in report["campaigns"].values():
            if campaign_data["target_achievement"]["reach"] < 0.5:
                recommendations.append(f"Campaign '{campaign_data['name']}' needs reach optimization")
            
            if campaign_data["avg_engagement_rate"] < 0.03:
                recommendations.append(f"Improve content quality for '{campaign_data['name']}'")
        
        # Content recommendations
        if report["content_performance"]:
            top_performer = report["content_performance"][0]
            recommendations.append(
                f"Replicate success factors from '{top_performer['title']}' "
                f"({top_performer['engagement_rate']:.2%} engagement)"
            )
        
        return recommendations[:5]
    
    async def _save_campaign(self, campaign: ContentCampaign):
        """Save campaign data"""
        
        campaigns_file = self.automation_path / f"campaign_{campaign.campaign_id}.json"
        
        campaign_data = {
            "campaign_id": campaign.campaign_id,
            "name": campaign.name,
            "content_ideas": [
                {
                    "title": idea.title,
                    "description": idea.description,
                    "content_type": idea.content_type.value,
                    "target_audience": idea.target_audience,
                    "key_message": idea.key_message,
                    "call_to_action": idea.call_to_action,
                    "keywords": idea.keywords,
                    "hashtags": idea.hashtags
                }
                for idea in campaign.content_ideas
            ],
            "strategy": campaign.strategy.value,
            "platforms": [p.value for p in campaign.platforms],
            "start_date": campaign.start_date.isoformat(),
            "end_date": campaign.end_date.isoformat(),
            "target_metrics": campaign.target_metrics,
            "scheduled_content": [
                {
                    "content_id": sc.content_id,
                    "platform": sc.platform.value,
                    "title": sc.title,
                    "description": sc.description[:500],  # Truncate for storage
                    "scheduled_time": sc.scheduled_time.isoformat(),
                    "status": sc.status.value,
                    "platform_content": {
                        "platform": sc.platform_content.platform.value,
                        "format": sc.platform_content.format,
                        "title": sc.platform_content.title,
                        "description": sc.platform_content.description[:500],
                        "hashtags": sc.platform_content.hashtags,
                        "optimal_time": sc.platform_content.optimal_time,
                        "media_specs": sc.platform_content.media_specs,
                        "engagement_hooks": sc.platform_content.engagement_hooks,
                        "estimated_reach": sc.platform_content.estimated_reach,
                        "viral_potential": sc.platform_content.viral_potential
                    },
                    "parent_content_id": sc.parent_content_id,
                    "performance_metrics": sc.performance_metrics
                }
                for sc in campaign.scheduled_content
            ],
            "performance_data": campaign.performance_data
        }
        
        with open(campaigns_file, 'w', encoding='utf-8') as f:
            json.dump(campaign_data, f, indent=2)
    
    async def _save_queue_state(self):
        """Save content queue state"""
        
        queue_data = [
            {
                "content_id": item.content_id,
                "platform": item.platform.value,
                "title": item.title,
                "description": item.description[:500],
                "scheduled_time": item.scheduled_time.isoformat(),
                "status": item.status.value,
                "platform_content": {
                    "platform": item.platform_content.platform.value,
                    "format": item.platform_content.format,
                    "title": item.platform_content.title,
                    "description": item.platform_content.description[:500],
                    "hashtags": item.platform_content.hashtags,
                    "optimal_time": item.platform_content.optimal_time,
                    "media_specs": item.platform_content.media_specs,
                    "engagement_hooks": item.platform_content.engagement_hooks,
                    "estimated_reach": item.platform_content.estimated_reach,
                    "viral_potential": item.platform_content.viral_potential
                },
                "parent_content_id": item.parent_content_id,
                "performance_metrics": item.performance_metrics
            }
            for item in self.content_queue
        ]
        
        queue_file = self.automation_path / "content_queue.json"
        with open(queue_file, 'w', encoding='utf-8') as f:
            json.dump(queue_data, f, indent=2)
    
    async def _save_performance_report(self, report: Dict):
        """Save performance report"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.automation_path / f"performance_report_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        print(f"Performance report saved to: {report_file}")


# Example usage
async def main():
    """Example usage of Automated Content System"""
    
    system = AutomatedContentSystem()
    
    # Create sample content ideas
    content_ideas = [
        ContentIdea(
            title="10 Marketing Strategies for 2024",
            description="Discover the top marketing strategies that will dominate in 2024",
            content_type=ContentType.EDUCATIONAL,
            target_audience="marketers and business owners",
            key_message="Stay ahead with innovative marketing",
            call_to_action="Start implementing these strategies today",
            keywords=["marketing", "strategy", "2024", "trends"],
            hashtags=["#Marketing2024", "#DigitalMarketing", "#BusinessGrowth"]
        ),
        ContentIdea(
            title="Behind the Scenes: Building Our Product",
            description="Take a peek at how we build our products from concept to launch",
            content_type=ContentType.BEHIND_SCENES,
            target_audience="customers and tech enthusiasts",
            key_message="Transparency in our process",
            call_to_action="Follow our journey",
            keywords=["behind scenes", "product development", "startup"],
            hashtags=["#BehindTheScenes", "#StartupLife", "#ProductDevelopment"]
        )
    ]
    
    # Create campaign
    print("Creating automated campaign...")
    
    campaign = await system.create_campaign(
        name="Q1 2024 Content Blitz",
        content_ideas=content_ideas,
        platforms=[
            PlatformName.YOUTUBE,
            PlatformName.INSTAGRAM,
            PlatformName.TIKTOK,
            PlatformName.LINKEDIN,
            PlatformName.TWITTER
        ],
        strategy=AdaptationStrategy.WATERFALL,
        duration_days=30
    )
    
    print(f"\nCampaign created: {campaign.name}")
    print(f"Total scheduled posts: {len(campaign.scheduled_content)}")
    
    # Show schedule
    print("\nContent Schedule:")
    for content in campaign.scheduled_content[:5]:  # Show first 5
        print(f"  {content.scheduled_time.strftime('%Y-%m-%d %H:%M')} - "
              f"{content.platform.value}: {content.title[:50]}...")
    
    # Auto-optimize a piece of content
    if campaign.scheduled_content:
        print("\n" + "="*50)
        print("Testing auto-optimization...")
        
        # Simulate some performance data
        test_content = campaign.scheduled_content[0]
        test_content.performance_metrics = {
            "views": 5000,
            "likes": 500,
            "comments": 50,
            "shares": 100,
            "engagement_rate": 0.13
        }
        
        optimizations = await system.auto_optimize_content(test_content.content_id)
        
        print(f"\nOptimization recommendations for '{test_content.title[:30]}...':")
        for key, value in optimizations.items():
            if isinstance(value, dict) and value.get("recommended"):
                print(f"  - {key}: {value.get('reason', 'Recommended')}")
    
    # Generate performance report
    print("\n" + "="*50)
    print("Generating performance report...")
    
    # Add to queue for reporting
    system.content_queue.extend(campaign.scheduled_content)
    
    report = await system.generate_performance_report(campaign.campaign_id)
    
    print(f"\nPerformance Report Summary:")
    if campaign.campaign_id in report["campaigns"]:
        campaign_perf = report["campaigns"][campaign.campaign_id]
        print(f"  Campaign: {campaign_perf['name']}")
        print(f"  Strategy: {campaign_perf['strategy']}")
        print(f"  Total Posts: {campaign_perf.get('total_posts', 0)}")
    
    print(f"\nRecommendations:")
    for rec in report["recommendations"]:
        print(f"  - {rec}")

if __name__ == "__main__":
    asyncio.run(main())