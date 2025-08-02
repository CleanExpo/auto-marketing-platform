"""
Multi-Platform Content Transformation Engine
Transforms single content ideas into optimized campaigns for all 8 major platforms
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import re
from dataclasses import dataclass, field
import asyncio
import aiohttp
from enum import Enum

# Import our existing modules
from platform_automation import PlatformSpecialist
from cpu_manager import get_cpu_manager

class ContentType(Enum):
    """Content type classifications"""
    EDUCATIONAL = "educational"
    ENTERTAINMENT = "entertainment"
    INSPIRATIONAL = "inspirational"
    PROMOTIONAL = "promotional"
    COMMUNITY = "community"
    NEWS = "news"
    BEHIND_SCENES = "behind_scenes"
    USER_GENERATED = "user_generated"

class PlatformName(Enum):
    """Supported platforms"""
    YOUTUBE = "youtube"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    TIKTOK = "tiktok"
    PINTEREST = "pinterest"
    REDDIT = "reddit"

@dataclass
class ContentIdea:
    """Core content idea structure"""
    title: str
    description: str
    content_type: ContentType
    target_audience: str
    key_message: str
    call_to_action: str
    keywords: List[str] = field(default_factory=list)
    hashtags: List[str] = field(default_factory=list)
    media_assets: Dict[str, str] = field(default_factory=dict)
    metrics_goals: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PlatformContent:
    """Platform-specific content adaptation"""
    platform: PlatformName
    format: str
    title: str
    description: str
    hashtags: List[str]
    optimal_time: str
    media_specs: Dict[str, Any]
    engagement_hooks: List[str]
    estimated_reach: int
    viral_potential: float  # 0-1 score

class ContentTransformationEngine:
    """Transform content ideas into multi-platform campaigns"""
    
    def __init__(self, project_id: str = None):
        self.project_id = project_id or "auto-marketing"
        self.base_path = Path("C:/Auto Marketing")
        self.platforms_data_path = self.base_path / "data" / "platforms"
        self.cpu_manager = get_cpu_manager(max_cpu=75.0)
        
        # Load platform strategies
        self.platform_strategies = self._load_platform_strategies()
        self.winning_formulas = self._load_winning_formulas()
        
        # Initialize performance tracking
        self.performance_history = []
        self.viral_patterns = {}
        
    def _load_platform_strategies(self) -> Dict:
        """Load all platform strategy documents"""
        strategies = {}
        
        # Load each platform's strategy file
        platform_files = {
            "youtube": "youtube_framework.json",
            "facebook": "facebook_strategy.md",
            "instagram": "instagram_blueprint.json",
            "twitter": "twitter_templates.md",
            "linkedin": "linkedin_authority.json",
            "tiktok": "tiktok_discovery.md",
            "pinterest": "pinterest_inspiration.json",
            "reddit": "reddit_community.md"
        }
        
        for platform, filename in platform_files.items():
            file_path = self.platforms_data_path / filename
            if file_path.exists():
                if filename.endswith('.json'):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        strategies[platform] = json.load(f)
                else:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        strategies[platform] = f.read()
        
        return strategies
    
    def _load_winning_formulas(self) -> Dict:
        """Load winning formulas document"""
        formulas_path = self.platforms_data_path / "winning_formulas.json"
        if formulas_path.exists():
            with open(formulas_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    async def transform_content(self, content_idea: ContentIdea) -> Dict[str, PlatformContent]:
        """Transform a single content idea into platform-specific content"""
        await self.cpu_manager.check_and_throttle()
        
        transformed_content = {}
        
        # Process each platform
        for platform in PlatformName:
            platform_content = await self._adapt_for_platform(
                content_idea, 
                platform
            )
            transformed_content[platform.value] = platform_content
        
        # Optimize for cross-platform synergy
        transformed_content = self._optimize_cross_platform(transformed_content)
        
        return transformed_content
    
    async def _adapt_for_platform(self, 
                                  content_idea: ContentIdea, 
                                  platform: PlatformName) -> PlatformContent:
        """Adapt content for specific platform"""
        
        # Get platform-specific strategy
        strategy = self.platform_strategies.get(platform.value, {})
        formula = self.winning_formulas.get("platform_winning_formulas", {}).get(platform.value, {})
        
        # Determine optimal format
        optimal_format = self._determine_format(content_idea, platform)
        
        # Adapt content elements
        adapted_title = self._adapt_title(content_idea.title, platform, optimal_format)
        adapted_description = self._adapt_description(content_idea.description, platform, optimal_format)
        adapted_hashtags = self._optimize_hashtags(content_idea.hashtags, platform)
        
        # Calculate optimal posting time
        optimal_time = self._calculate_optimal_time(platform, content_idea.target_audience)
        
        # Generate engagement hooks
        engagement_hooks = self._generate_hooks(content_idea, platform, optimal_format)
        
        # Estimate performance
        estimated_reach = self._estimate_reach(content_idea, platform)
        viral_potential = self._calculate_viral_potential(content_idea, platform, optimal_format)
        
        # Get media specifications
        media_specs = self._get_media_specs(platform, optimal_format)
        
        return PlatformContent(
            platform=platform,
            format=optimal_format,
            title=adapted_title,
            description=adapted_description,
            hashtags=adapted_hashtags,
            optimal_time=optimal_time,
            media_specs=media_specs,
            engagement_hooks=engagement_hooks,
            estimated_reach=estimated_reach,
            viral_potential=viral_potential
        )
    
    def _determine_format(self, content_idea: ContentIdea, platform: PlatformName) -> str:
        """Determine optimal content format for platform"""
        format_map = {
            PlatformName.YOUTUBE: {
                ContentType.EDUCATIONAL: "long_form_tutorial",
                ContentType.ENTERTAINMENT: "shorts",
                ContentType.INSPIRATIONAL: "story_video",
                ContentType.PROMOTIONAL: "product_demo",
                ContentType.COMMUNITY: "live_stream",
                ContentType.NEWS: "breaking_update",
                ContentType.BEHIND_SCENES: "vlog",
                ContentType.USER_GENERATED: "compilation"
            },
            PlatformName.INSTAGRAM: {
                ContentType.EDUCATIONAL: "carousel",
                ContentType.ENTERTAINMENT: "reels",
                ContentType.INSPIRATIONAL: "reels",
                ContentType.PROMOTIONAL: "shopping_post",
                ContentType.COMMUNITY: "stories",
                ContentType.NEWS: "stories",
                ContentType.BEHIND_SCENES: "stories",
                ContentType.USER_GENERATED: "reels"
            },
            PlatformName.TIKTOK: {
                ContentType.EDUCATIONAL: "tutorial",
                ContentType.ENTERTAINMENT: "trend",
                ContentType.INSPIRATIONAL: "transformation",
                ContentType.PROMOTIONAL: "product_showcase",
                ContentType.COMMUNITY: "duet",
                ContentType.NEWS: "breaking",
                ContentType.BEHIND_SCENES: "day_in_life",
                ContentType.USER_GENERATED: "challenge"
            },
            PlatformName.LINKEDIN: {
                ContentType.EDUCATIONAL: "article",
                ContentType.ENTERTAINMENT: "video",
                ContentType.INSPIRATIONAL: "text_post",
                ContentType.PROMOTIONAL: "document",
                ContentType.COMMUNITY: "poll",
                ContentType.NEWS: "article",
                ContentType.BEHIND_SCENES: "video",
                ContentType.USER_GENERATED: "text_post"
            },
            PlatformName.TWITTER: {
                ContentType.EDUCATIONAL: "thread",
                ContentType.ENTERTAINMENT: "meme",
                ContentType.INSPIRATIONAL: "quote",
                ContentType.PROMOTIONAL: "announcement",
                ContentType.COMMUNITY: "poll",
                ContentType.NEWS: "breaking",
                ContentType.BEHIND_SCENES: "thread",
                ContentType.USER_GENERATED: "retweet"
            },
            PlatformName.FACEBOOK: {
                ContentType.EDUCATIONAL: "video",
                ContentType.ENTERTAINMENT: "reel",
                ContentType.INSPIRATIONAL: "photo_story",
                ContentType.PROMOTIONAL: "event",
                ContentType.COMMUNITY: "group_post",
                ContentType.NEWS: "live",
                ContentType.BEHIND_SCENES: "album",
                ContentType.USER_GENERATED: "share"
            },
            PlatformName.PINTEREST: {
                ContentType.EDUCATIONAL: "idea_pin",
                ContentType.ENTERTAINMENT: "video_pin",
                ContentType.INSPIRATIONAL: "standard_pin",
                ContentType.PROMOTIONAL: "product_pin",
                ContentType.COMMUNITY: "board",
                ContentType.NEWS: "standard_pin",
                ContentType.BEHIND_SCENES: "idea_pin",
                ContentType.USER_GENERATED: "board"
            },
            PlatformName.REDDIT: {
                ContentType.EDUCATIONAL: "guide_post",
                ContentType.ENTERTAINMENT: "media_post",
                ContentType.INSPIRATIONAL: "text_post",
                ContentType.PROMOTIONAL: "ama",
                ContentType.COMMUNITY: "discussion",
                ContentType.NEWS: "link_post",
                ContentType.BEHIND_SCENES: "text_post",
                ContentType.USER_GENERATED: "crosspost"
            }
        }
        
        return format_map.get(platform, {}).get(content_idea.content_type, "standard")
    
    def _adapt_title(self, original_title: str, platform: PlatformName, format: str) -> str:
        """Adapt title for platform requirements"""
        title_templates = {
            PlatformName.YOUTUBE: {
                "long_form_tutorial": f"How to {original_title} (Complete Guide)",
                "shorts": f"{original_title} in 60 Seconds! #Shorts",
                "default": original_title
            },
            PlatformName.INSTAGRAM: {
                "carousel": f"Swipe for {original_title} →",
                "reels": original_title[:30] + "...",
                "default": original_title[:40]
            },
            PlatformName.TIKTOK: {
                "tutorial": f"POV: You learn {original_title}",
                "trend": f"{original_title} Challenge",
                "default": original_title[:100]
            },
            PlatformName.LINKEDIN: {
                "article": f"The Complete Guide to {original_title}",
                "text_post": f"Thoughts on {original_title}:",
                "default": original_title
            },
            PlatformName.TWITTER: {
                "thread": f"{original_title} - A Thread 🧵",
                "default": original_title[:100]
            },
            PlatformName.FACEBOOK: {
                "video": f"Watch: {original_title}",
                "default": original_title
            },
            PlatformName.PINTEREST: {
                "idea_pin": f"{original_title} - Step by Step",
                "default": original_title + " | Save for Later"
            },
            PlatformName.REDDIT: {
                "guide_post": f"[Guide] {original_title}",
                "discussion": f"Let's discuss: {original_title}",
                "default": original_title
            }
        }
        
        platform_titles = title_templates.get(platform, {})
        return platform_titles.get(format, platform_titles.get("default", original_title))
    
    def _adapt_description(self, original_desc: str, platform: PlatformName, format: str) -> str:
        """Adapt description for platform requirements"""
        
        # Platform-specific character limits and formatting
        platform_limits = {
            PlatformName.YOUTUBE: 5000,
            PlatformName.INSTAGRAM: 2200,
            PlatformName.TIKTOK: 2200,
            PlatformName.LINKEDIN: 3000,
            PlatformName.TWITTER: 280,
            PlatformName.FACEBOOK: 63206,
            PlatformName.PINTEREST: 500,
            PlatformName.REDDIT: 40000
        }
        
        limit = platform_limits.get(platform, 1000)
        
        # Truncate if needed
        if len(original_desc) > limit:
            truncated = original_desc[:limit-3] + "..."
        else:
            truncated = original_desc
        
        # Add platform-specific CTAs
        platform_ctas = {
            PlatformName.YOUTUBE: "\n\n👍 Like & Subscribe for more!\n🔔 Turn on notifications",
            PlatformName.INSTAGRAM: "\n\n💾 Save this for later!\n📤 Share with a friend who needs this",
            PlatformName.TIKTOK: "\n\n♥️ Double tap if helpful!\n➕ Follow for more",
            PlatformName.LINKEDIN: "\n\nWhat are your thoughts on this?\n\n#thoughtleadership",
            PlatformName.TWITTER: "",  # Too short for CTA
            PlatformName.FACEBOOK: "\n\n👍 Like if you agree!\n💬 Share your thoughts below",
            PlatformName.PINTEREST: "\n\n📌 Pin this for later!",
            PlatformName.REDDIT: "\n\nEDIT: Thanks for the awards!\nEDIT 2: RIP my inbox"
        }
        
        cta = platform_ctas.get(platform, "")
        
        # Ensure we don't exceed limit with CTA
        if len(truncated + cta) <= limit:
            return truncated + cta
        else:
            return truncated[:limit - len(cta)] + cta
    
    def _optimize_hashtags(self, original_hashtags: List[str], platform: PlatformName) -> List[str]:
        """Optimize hashtags for platform"""
        
        # Platform-specific hashtag limits
        hashtag_limits = {
            PlatformName.YOUTUBE: 15,
            PlatformName.INSTAGRAM: 30,
            PlatformName.TIKTOK: 10,
            PlatformName.LINKEDIN: 5,
            PlatformName.TWITTER: 2,
            PlatformName.FACEBOOK: 5,
            PlatformName.PINTEREST: 20,
            PlatformName.REDDIT: 0  # Reddit doesn't use hashtags
        }
        
        limit = hashtag_limits.get(platform, 5)
        
        if platform == PlatformName.REDDIT:
            return []
        
        # Platform-specific trending hashtags
        platform_trending = {
            PlatformName.YOUTUBE: ["#Shorts", "#YouTube", "#Subscribe"],
            PlatformName.INSTAGRAM: ["#InstaDaily", "#PhotoOfTheDay", "#Love"],
            PlatformName.TIKTOK: ["#FYP", "#ForYou", "#Viral"],
            PlatformName.LINKEDIN: ["#Business", "#Leadership", "#Innovation"],
            PlatformName.TWITTER: ["#Trending"],
            PlatformName.FACEBOOK: ["#Facebook"],
            PlatformName.PINTEREST: ["#PinIt", "#DIY", "#Ideas"]
        }
        
        # Combine original with platform-specific
        trending = platform_trending.get(platform, [])
        combined = list(set(original_hashtags[:limit-len(trending)] + trending))
        
        return combined[:limit]
    
    def _calculate_optimal_time(self, platform: PlatformName, target_audience: str) -> str:
        """Calculate optimal posting time based on platform and audience"""
        
        # Default optimal times (EST)
        optimal_times = {
            PlatformName.YOUTUBE: "Tuesday-Thursday 2-4 PM",
            PlatformName.INSTAGRAM: "Weekdays 11 AM-1 PM, 7-9 PM",
            PlatformName.TIKTOK: "Tuesday-Thursday 6-10 AM, 7-11 PM",
            PlatformName.LINKEDIN: "Tuesday-Thursday 8-10 AM",
            PlatformName.TWITTER: "Weekdays 8-10 AM, 7-9 PM",
            PlatformName.FACEBOOK: "Thursday-Sunday 1-4 PM",
            PlatformName.PINTEREST: "Saturday 8-11 PM",
            PlatformName.REDDIT: "Monday-Wednesday 8-10 AM"
        }
        
        # Adjust based on target audience
        audience_adjustments = {
            "gen_z": {"shift": -2, "platforms": [PlatformName.TIKTOK, PlatformName.INSTAGRAM]},
            "millennials": {"shift": 0, "platforms": [PlatformName.INSTAGRAM, PlatformName.TWITTER]},
            "gen_x": {"shift": 1, "platforms": [PlatformName.FACEBOOK, PlatformName.LINKEDIN]},
            "professionals": {"shift": -1, "platforms": [PlatformName.LINKEDIN]},
            "students": {"shift": 3, "platforms": [PlatformName.TIKTOK, PlatformName.YOUTUBE]}
        }
        
        base_time = optimal_times.get(platform, "Weekdays 12 PM")
        
        # Apply audience adjustment if applicable
        for audience_type, adjustment in audience_adjustments.items():
            if audience_type in target_audience.lower() and platform in adjustment["platforms"]:
                # This is simplified - in production, you'd actually shift the time
                return f"{base_time} (adjusted for {audience_type})"
        
        return base_time
    
    def _generate_hooks(self, content_idea: ContentIdea, platform: PlatformName, format: str) -> List[str]:
        """Generate platform-specific engagement hooks"""
        
        hooks_templates = {
            PlatformName.YOUTUBE: [
                f"You won't believe what happens when...",
                f"The secret to {content_idea.key_message} revealed",
                f"Why everyone's talking about {content_idea.title}"
            ],
            PlatformName.INSTAGRAM: [
                f"Save this before it's gone!",
                f"Tag someone who needs to see this",
                f"Double tap if you agree"
            ],
            PlatformName.TIKTOK: [
                f"Wait for it...",
                f"POV: {content_idea.key_message}",
                f"Things that live rent-free in my head"
            ],
            PlatformName.LINKEDIN: [
                f"Here's what 10 years in the industry taught me",
                f"Unpopular opinion: {content_idea.key_message}",
                f"The one thing that changed everything"
            ],
            PlatformName.TWITTER: [
                f"A thread on {content_idea.title} 🧵",
                f"Hot take: {content_idea.key_message}",
                f"RT if you've experienced this"
            ],
            PlatformName.FACEBOOK: [
                f"Type YES if you want more content like this",
                f"Share if this helped you",
                f"What's your opinion on this?"
            ],
            PlatformName.PINTEREST: [
                f"Pin this for later!",
                f"The ultimate guide to {content_idea.title}",
                f"{content_idea.title} ideas you'll love"
            ],
            PlatformName.REDDIT: [
                f"[Serious] {content_idea.title}",
                f"ELI5: {content_idea.key_message}",
                f"YSK about {content_idea.title}"
            ]
        }
        
        return hooks_templates.get(platform, [f"Check out {content_idea.title}"])
    
    def _estimate_reach(self, content_idea: ContentIdea, platform: PlatformName) -> int:
        """Estimate potential reach based on platform and content type"""
        
        # Base reach estimates (these would be refined with actual data)
        base_reach = {
            PlatformName.YOUTUBE: 10000,
            PlatformName.INSTAGRAM: 5000,
            PlatformName.TIKTOK: 20000,
            PlatformName.LINKEDIN: 3000,
            PlatformName.TWITTER: 2000,
            PlatformName.FACEBOOK: 8000,
            PlatformName.PINTEREST: 4000,
            PlatformName.REDDIT: 15000
        }
        
        # Content type multipliers
        content_multipliers = {
            ContentType.EDUCATIONAL: 1.5,
            ContentType.ENTERTAINMENT: 2.0,
            ContentType.INSPIRATIONAL: 1.3,
            ContentType.PROMOTIONAL: 0.7,
            ContentType.COMMUNITY: 1.2,
            ContentType.NEWS: 1.8,
            ContentType.BEHIND_SCENES: 1.1,
            ContentType.USER_GENERATED: 1.4
        }
        
        base = base_reach.get(platform, 1000)
        multiplier = content_multipliers.get(content_idea.content_type, 1.0)
        
        # Add keyword boost
        keyword_boost = 1.0 + (len(content_idea.keywords) * 0.1)
        
        estimated = int(base * multiplier * keyword_boost)
        
        return estimated
    
    def _calculate_viral_potential(self, content_idea: ContentIdea, 
                                  platform: PlatformName, format: str) -> float:
        """Calculate viral potential score (0-1)"""
        
        score = 0.0
        
        # Platform viral tendencies
        platform_scores = {
            PlatformName.TIKTOK: 0.3,
            PlatformName.YOUTUBE: 0.2,
            PlatformName.INSTAGRAM: 0.2,
            PlatformName.TWITTER: 0.25,
            PlatformName.REDDIT: 0.25,
            PlatformName.FACEBOOK: 0.15,
            PlatformName.PINTEREST: 0.1,
            PlatformName.LINKEDIN: 0.05
        }
        
        score += platform_scores.get(platform, 0.1)
        
        # Content type viral potential
        content_scores = {
            ContentType.ENTERTAINMENT: 0.3,
            ContentType.NEWS: 0.25,
            ContentType.INSPIRATIONAL: 0.2,
            ContentType.USER_GENERATED: 0.2,
            ContentType.EDUCATIONAL: 0.15,
            ContentType.COMMUNITY: 0.15,
            ContentType.BEHIND_SCENES: 0.1,
            ContentType.PROMOTIONAL: 0.05
        }
        
        score += content_scores.get(content_idea.content_type, 0.1)
        
        # Format viral boost
        viral_formats = {
            "shorts": 0.2,
            "reels": 0.2,
            "trend": 0.25,
            "thread": 0.15,
            "meme": 0.3
        }
        
        score += viral_formats.get(format, 0.05)
        
        # Trending keywords boost
        if len(content_idea.keywords) > 5:
            score += 0.1
        
        # Cap at 1.0
        return min(score, 1.0)
    
    def _get_media_specs(self, platform: PlatformName, format: str) -> Dict[str, Any]:
        """Get media specifications for platform and format"""
        
        specs = {
            PlatformName.YOUTUBE: {
                "video": {
                    "resolution": "1920x1080",
                    "aspect_ratio": "16:9",
                    "max_length": "12 hours",
                    "format": "MP4"
                },
                "thumbnail": {
                    "resolution": "1280x720",
                    "format": "JPG/PNG"
                }
            },
            PlatformName.INSTAGRAM: {
                "feed": {
                    "resolution": "1080x1080",
                    "aspect_ratio": "1:1",
                    "format": "JPG/PNG"
                },
                "reels": {
                    "resolution": "1080x1920",
                    "aspect_ratio": "9:16",
                    "max_length": "90 seconds",
                    "format": "MP4"
                },
                "stories": {
                    "resolution": "1080x1920",
                    "aspect_ratio": "9:16",
                    "max_length": "15 seconds",
                    "format": "JPG/MP4"
                }
            },
            PlatformName.TIKTOK: {
                "video": {
                    "resolution": "1080x1920",
                    "aspect_ratio": "9:16",
                    "max_length": "10 minutes",
                    "optimal_length": "15-60 seconds",
                    "format": "MP4"
                }
            },
            PlatformName.LINKEDIN: {
                "image": {
                    "resolution": "1200x627",
                    "aspect_ratio": "1.91:1",
                    "format": "JPG/PNG"
                },
                "video": {
                    "resolution": "1920x1080",
                    "max_length": "10 minutes",
                    "format": "MP4"
                }
            },
            PlatformName.TWITTER: {
                "image": {
                    "resolution": "1200x675",
                    "aspect_ratio": "16:9",
                    "format": "JPG/PNG"
                },
                "video": {
                    "max_length": "2:20",
                    "format": "MP4"
                }
            },
            PlatformName.FACEBOOK: {
                "image": {
                    "resolution": "1200x630",
                    "format": "JPG/PNG"
                },
                "video": {
                    "resolution": "1280x720",
                    "max_length": "240 minutes",
                    "format": "MP4"
                }
            },
            PlatformName.PINTEREST: {
                "pin": {
                    "resolution": "1000x1500",
                    "aspect_ratio": "2:3",
                    "format": "JPG/PNG"
                },
                "video": {
                    "max_length": "15 minutes",
                    "format": "MP4"
                }
            },
            PlatformName.REDDIT: {
                "image": {
                    "max_size": "20MB",
                    "format": "JPG/PNG/GIF"
                },
                "video": {
                    "max_length": "15 minutes",
                    "format": "MP4"
                }
            }
        }
        
        platform_specs = specs.get(platform, {})
        
        # Return most relevant spec based on format
        if "video" in format.lower() or "reel" in format.lower() or "short" in format.lower():
            return platform_specs.get("video", platform_specs.get("default", {}))
        else:
            return platform_specs.get("image", platform_specs.get("feed", platform_specs.get("pin", {})))
    
    def _optimize_cross_platform(self, content_dict: Dict[str, PlatformContent]) -> Dict[str, PlatformContent]:
        """Optimize content for cross-platform synergy"""
        
        # Identify hero platform (highest viral potential)
        hero_platform = max(content_dict.items(), 
                          key=lambda x: x[1].viral_potential)[0]
        
        # Create content waterfall strategy
        waterfall_order = [
            "youtube",  # Long-form origin
            "linkedin",  # Professional angle
            "facebook",  # Community discussion
            "instagram",  # Visual storytelling
            "twitter",  # Quick updates
            "tiktok",  # Viral snippets
            "pinterest",  # Evergreen saves
            "reddit"  # Deep discussion
        ]
        
        # Ensure cross-promotion mentions
        for i, platform in enumerate(waterfall_order):
            if platform in content_dict:
                content = content_dict[platform]
                
                # Add cross-platform CTAs
                if i < len(waterfall_order) - 1:
                    next_platform = waterfall_order[i + 1]
                    if next_platform in content_dict:
                        # Add subtle cross-promotion
                        content.description += f"\n\n"
        
        return content_dict
    
    async def generate_campaign(self, 
                               content_ideas: List[ContentIdea],
                               campaign_name: str,
                               duration_days: int = 30) -> Dict[str, Any]:
        """Generate full multi-platform campaign"""
        
        campaign = {
            "name": campaign_name,
            "duration": duration_days,
            "start_date": datetime.now().isoformat(),
            "end_date": (datetime.now() + timedelta(days=duration_days)).isoformat(),
            "content_calendar": {},
            "total_estimated_reach": 0,
            "platforms": {}
        }
        
        # Process each content idea
        for idea in content_ideas:
            transformed = await self.transform_content(idea)
            
            # Add to campaign
            for platform, content in transformed.items():
                if platform not in campaign["platforms"]:
                    campaign["platforms"][platform] = []
                
                campaign["platforms"][platform].append({
                    "title": content.title,
                    "format": content.format,
                    "optimal_time": content.optimal_time,
                    "viral_potential": content.viral_potential,
                    "estimated_reach": content.estimated_reach
                })
                
                campaign["total_estimated_reach"] += content.estimated_reach
        
        # Generate content calendar
        campaign["content_calendar"] = self._generate_calendar(
            campaign["platforms"], 
            duration_days
        )
        
        # Save campaign
        await self._save_campaign(campaign)
        
        return campaign
    
    def _generate_calendar(self, platforms_content: Dict, duration_days: int) -> Dict[str, List]:
        """Generate day-by-day content calendar"""
        
        calendar = {}
        current_date = datetime.now()
        
        for day in range(duration_days):
            date_str = (current_date + timedelta(days=day)).strftime("%Y-%m-%d")
            calendar[date_str] = []
            
            # Distribute content across days
            for platform, contents in platforms_content.items():
                if contents and day % (30 // max(1, min(len(contents), 30))) == 0:
                    content_index = (day // (30 // max(1, min(len(contents), 30)))) % len(contents)
                    if content_index < len(contents):
                        calendar[date_str].append({
                            "platform": platform,
                            "content": contents[content_index]["title"],
                            "time": contents[content_index]["optimal_time"]
                        })
        
        return calendar
    
    async def _save_campaign(self, campaign: Dict[str, Any]):
        """Save campaign to file"""
        campaigns_dir = self.base_path / "campaigns"
        campaigns_dir.mkdir(exist_ok=True)
        
        filename = f"{campaign['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = campaigns_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(campaign, f, indent=2, ensure_ascii=False)
        
        print(f"Campaign saved to: {filepath}")
    
    async def analyze_viral_patterns(self, platform: PlatformName) -> Dict[str, Any]:
        """Analyze viral content patterns for a platform"""
        
        patterns = {
            "platform": platform.value,
            "viral_indicators": {},
            "optimal_conditions": {},
            "content_templates": []
        }
        
        # Platform-specific viral indicators
        viral_indicators = {
            PlatformName.TIKTOK: {
                "completion_rate": ">80%",
                "share_rate": ">5%",
                "comment_rate": ">3%",
                "save_rate": ">2%",
                "first_hour_views": ">1000"
            },
            PlatformName.YOUTUBE: {
                "ctr": ">10%",
                "avg_view_duration": ">50%",
                "like_ratio": ">95%",
                "comment_rate": ">2%",
                "shares": ">1%"
            },
            PlatformName.INSTAGRAM: {
                "engagement_rate": ">6%",
                "save_rate": ">3%",
                "share_rate": ">2%",
                "reach_rate": ">50%",
                "profile_visits": ">5%"
            }
        }
        
        patterns["viral_indicators"] = viral_indicators.get(platform, {})
        
        # Optimal conditions for virality
        patterns["optimal_conditions"] = {
            "timing": self._calculate_optimal_time(platform, "general"),
            "content_length": self._get_optimal_length(platform),
            "hashtag_count": self._get_optimal_hashtag_count(platform),
            "engagement_window": "First 2 hours critical"
        }
        
        # Viral content templates
        patterns["content_templates"] = self._get_viral_templates(platform)
        
        return patterns
    
    def _get_optimal_length(self, platform: PlatformName) -> str:
        """Get optimal content length for platform"""
        
        lengths = {
            PlatformName.TIKTOK: "15-30 seconds",
            PlatformName.YOUTUBE: "8-12 minutes (long-form), 30-60 seconds (Shorts)",
            PlatformName.INSTAGRAM: "7-15 seconds (Reels), 5-7 slides (Carousel)",
            PlatformName.TWITTER: "100-150 characters",
            PlatformName.LINKEDIN: "1300-2000 characters",
            PlatformName.FACEBOOK: "40-80 characters",
            PlatformName.PINTEREST: "200-300 character description",
            PlatformName.REDDIT: "300-1000 words"
        }
        
        return lengths.get(platform, "Varies")
    
    def _get_optimal_hashtag_count(self, platform: PlatformName) -> int:
        """Get optimal number of hashtags for platform"""
        
        counts = {
            PlatformName.INSTAGRAM: 10,
            PlatformName.TIKTOK: 5,
            PlatformName.TWITTER: 2,
            PlatformName.LINKEDIN: 5,
            PlatformName.FACEBOOK: 3,
            PlatformName.PINTEREST: 10,
            PlatformName.YOUTUBE: 10,
            PlatformName.REDDIT: 0
        }
        
        return counts.get(platform, 5)
    
    def _get_viral_templates(self, platform: PlatformName) -> List[str]:
        """Get viral content templates for platform"""
        
        templates = {
            PlatformName.TIKTOK: [
                "POV: [Relatable scenario]",
                "Things that [unexpected outcome]",
                "Wait for it... [surprise ending]"
            ],
            PlatformName.YOUTUBE: [
                "I Tried [Challenge] for 30 Days",
                "[Number] Things You Didn't Know About [Topic]",
                "The Truth About [Controversial Topic]"
            ],
            PlatformName.INSTAGRAM: [
                "Save this for later!",
                "Tag someone who needs to see this",
                "Which one are you? [This or That]"
            ]
        }
        
        return templates.get(platform, ["Create valuable content"])


# Example usage
async def main():
    """Example usage of the Content Transformation Engine"""
    
    engine = ContentTransformationEngine()
    
    # Create sample content idea
    content_idea = ContentIdea(
        title="5 Marketing Strategies That Actually Work",
        description="Discover proven marketing strategies that deliver real results for businesses of all sizes.",
        content_type=ContentType.EDUCATIONAL,
        target_audience="small business owners and marketers",
        key_message="Effective marketing doesn't have to be complicated",
        call_to_action="Start implementing these strategies today",
        keywords=["marketing", "strategy", "business", "growth", "ROI"],
        hashtags=["#MarketingTips", "#BusinessGrowth", "#DigitalMarketing", "#SmallBusiness"]
    )
    
    # Transform for all platforms
    print("Transforming content for all platforms...")
    transformed = await engine.transform_content(content_idea)
    
    # Display results
    for platform_name, content in transformed.items():
        print(f"\n{'='*50}")
        print(f"Platform: {platform_name.upper()}")
        print(f"Format: {content.format}")
        print(f"Title: {content.title}")
        print(f"Optimal Time: {content.optimal_time}")
        print(f"Viral Potential: {content.viral_potential:.2f}")
        print(f"Estimated Reach: {content.estimated_reach:,}")
        print(f"Hashtags: {', '.join(content.hashtags[:5])}")
        print(f"Hook: {content.engagement_hooks[0] if content.engagement_hooks else 'N/A'}")
    
    # Generate full campaign
    print("\n" + "="*50)
    print("Generating full campaign...")
    
    campaign = await engine.generate_campaign(
        content_ideas=[content_idea],
        campaign_name="Q1 Marketing Education",
        duration_days=30
    )
    
    print(f"Campaign created: {campaign['name']}")
    print(f"Total estimated reach: {campaign['total_estimated_reach']:,}")
    print(f"Duration: {campaign['duration']} days")

if __name__ == "__main__":
    asyncio.run(main())