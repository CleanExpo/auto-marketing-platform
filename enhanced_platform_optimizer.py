"""
Enhanced Platform Optimizer
Integrates detailed platform specifications for maximum optimization
"""

import json
import asyncio
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import random
from collections import defaultdict

# Import existing modules
from content_transformation_engine import ContentIdea, ContentType, PlatformName
from viral_content_analyzer import ViralContentAnalyzer
from automated_content_system import AutomatedContentSystem
from cpu_manager import get_cpu_manager

@dataclass
class PlatformOptimization:
    """Enhanced platform optimization with detailed specs"""
    platform: str
    category: str
    algorithm_weights: Dict[str, int]
    content_specs: Dict[str, Any]
    winning_formulas: List[Dict]
    optimization_score: float = 0.0
    recommended_template: Optional[str] = None
    estimated_engagement: float = 0.0
    posting_time: Optional[str] = None

class EnhancedPlatformOptimizer:
    """Advanced platform optimization using master configuration"""
    
    def __init__(self):
        self.base_path = Path("C:/Auto Marketing")
        self.config_path = self.base_path / "platform_master_config.json"
        
        # Load master configuration
        self.master_config = self._load_master_config()
        
        # Initialize components
        self.viral_analyzer = ViralContentAnalyzer()
        self.automation_system = AutomatedContentSystem()
        self.cpu_manager = get_cpu_manager(max_cpu=75.0)
        
        # Performance cache
        self.optimization_cache = {}
        self.template_performance = defaultdict(list)
    
    def _load_master_config(self) -> Dict:
        """Load the master platform configuration"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    async def optimize_for_platform(self, 
                                   content_idea: ContentIdea,
                                   platform: str) -> PlatformOptimization:
        """Optimize content for specific platform using detailed specs"""
        
        await self.cpu_manager.check_and_throttle()
        
        platform_config = self.master_config["platforms"].get(platform, {})
        
        if not platform_config:
            raise ValueError(f"Platform {platform} not found in configuration")
        
        # Create optimization object
        optimization = PlatformOptimization(
            platform=platform,
            category=platform_config["category"],
            algorithm_weights=platform_config["algorithm_weights"],
            content_specs=platform_config["content_specs"],
            winning_formulas=platform_config["winning_formulas"]
        )
        
        # Select best template based on content type
        optimization.recommended_template = self._select_best_template(
            content_idea, 
            platform_config["winning_formulas"]
        )
        
        # Calculate optimization score
        optimization.optimization_score = await self._calculate_optimization_score(
            content_idea,
            platform_config,
            optimization.recommended_template
        )
        
        # Estimate engagement
        optimization.estimated_engagement = self._estimate_engagement(
            platform_config,
            optimization.recommended_template,
            optimization.optimization_score
        )
        
        # Determine optimal posting time
        if "posting_schedule" in platform_config:
            optimization.posting_time = self._get_optimal_time(
                platform_config["posting_schedule"]
            )
        
        return optimization
    
    def _select_best_template(self, 
                             content_idea: ContentIdea,
                             formulas: List[Dict]) -> str:
        """Select the best winning formula for the content"""
        
        best_template = None
        best_score = 0
        
        for formula in formulas:
            score = 0
            
            # Check if content type matches template best_for
            if "best_for" in formula:
                content_keywords = content_idea.keywords
                for use_case in formula["best_for"]:
                    if any(keyword in use_case.lower() for keyword in content_keywords):
                        score += 2
            
            # Consider engagement rate
            engagement_rate = float(formula.get("engagement_rate", "0%").rstrip("%"))
            score += engagement_rate
            
            if score > best_score:
                best_score = score
                best_template = formula["template"]
        
        return best_template or formulas[0]["template"]
    
    async def _calculate_optimization_score(self,
                                           content_idea: ContentIdea,
                                           platform_config: Dict,
                                           template: str) -> float:
        """Calculate comprehensive optimization score"""
        
        score = 0.0
        max_score = 100.0
        
        # Algorithm weight alignment (40% of score)
        algorithm_weights = platform_config.get("algorithm_weights", {})
        
        # Check content alignment with algorithm priorities
        if "watch_time" in algorithm_weights and content_idea.content_type == ContentType.EDUCATIONAL:
            score += algorithm_weights["watch_time"] * 0.4
        
        if "engagement_rate" in algorithm_weights:
            # Estimate based on content quality indicators
            if len(content_idea.keywords) > 5:
                score += algorithm_weights["engagement_rate"] * 0.2
        
        # Template performance (30% of score)
        for formula in platform_config.get("winning_formulas", []):
            if formula["template"] == template:
                engagement = float(formula.get("engagement_rate", "0%").rstrip("%"))
                score += (engagement / 10) * 30  # Normalize to 30 points max
                break
        
        # Content specification compliance (20% of score)
        specs_score = 20.0  # Assume full compliance for now
        score += specs_score
        
        # Trending elements (10% of score)
        if "trending_elements" in platform_config or "viral_elements" in platform_config:
            score += 10.0  # Bonus for platforms with viral potential
        
        return min(score, max_score)
    
    def _estimate_engagement(self,
                           platform_config: Dict,
                           template: str,
                           optimization_score: float) -> float:
        """Estimate engagement rate based on optimization"""
        
        base_engagement = 0.01  # 1% base
        
        # Get template engagement rate
        for formula in platform_config.get("winning_formulas", []):
            if formula["template"] == template:
                template_engagement = float(formula.get("engagement_rate", "1%").rstrip("%")) / 100
                base_engagement = template_engagement
                break
        
        # Adjust based on optimization score
        multiplier = 1 + (optimization_score / 100)
        
        estimated = base_engagement * multiplier
        
        # Cap at realistic maximum
        category_caps = {
            "video_authority": 0.08,
            "visual_storytelling": 0.06,
            "entertainment_discovery": 0.15,
            "real_time_conversation": 0.10,
            "community_connection": 0.05,
            "professional_authority": 0.04,
            "inspiration_discovery": 0.07,
            "community_discussion": 0.08
        }
        
        max_engagement = category_caps.get(platform_config.get("category", ""), 0.10)
        
        return min(estimated, max_engagement)
    
    def _get_optimal_time(self, schedule: Dict) -> str:
        """Get optimal posting time from schedule"""
        
        optimal_times = schedule.get("optimal_times", [])
        
        if isinstance(optimal_times, list) and optimal_times:
            return optimal_times[0]
        elif isinstance(optimal_times, dict):
            # Get first available time slot
            for day, times in optimal_times.items():
                if times:
                    return f"{day}: {times[0] if isinstance(times, list) else times}"
        
        return "12:00 PM EST"
    
    async def generate_platform_specific_content(self,
                                                content_idea: ContentIdea,
                                                platforms: List[str]) -> Dict[str, Dict]:
        """Generate highly optimized content for multiple platforms"""
        
        results = {}
        
        for platform in platforms:
            optimization = await self.optimize_for_platform(content_idea, platform)
            
            # Generate platform-specific content
            platform_content = await self._generate_content_for_platform(
                content_idea,
                platform,
                optimization
            )
            
            results[platform] = {
                "content": platform_content,
                "optimization": {
                    "score": optimization.optimization_score,
                    "template": optimization.recommended_template,
                    "estimated_engagement": optimization.estimated_engagement,
                    "posting_time": optimization.posting_time,
                    "category": optimization.category
                },
                "specs": optimization.content_specs,
                "algorithm_focus": optimization.algorithm_weights
            }
        
        return results
    
    async def _generate_content_for_platform(self,
                                            content_idea: ContentIdea,
                                            platform: str,
                                            optimization: PlatformOptimization) -> Dict:
        """Generate platform-specific content using optimization data"""
        
        platform_config = self.master_config["platforms"][platform]
        
        # Get the winning formula structure
        formula = None
        for f in optimization.winning_formulas:
            if f["template"] == optimization.recommended_template:
                formula = f
                break
        
        if not formula:
            formula = optimization.winning_formulas[0]
        
        # Generate content based on formula structure
        content = {
            "title": self._generate_title(content_idea, platform, formula),
            "description": self._generate_description(content_idea, platform, formula),
            "structure": formula.get("structure", ""),
            "format": self._select_content_format(platform_config),
            "hashtags": self._generate_hashtags(content_idea, platform),
            "media_specs": self._get_media_specs(platform_config),
            "optimization_elements": self._get_optimization_elements(platform_config)
        }
        
        return content
    
    def _generate_title(self, 
                       content_idea: ContentIdea,
                       platform: str,
                       formula: Dict) -> str:
        """Generate platform-optimized title"""
        
        base_title = content_idea.title
        
        # Platform-specific title formats
        title_formats = {
            "youtube": {
                "educational_authority": f"How to {base_title} (Complete Guide)",
                "transformation_story": f"{base_title}: The Transformation"
            },
            "instagram": {
                "transformation_reveal": f"Wait for it... {base_title}",
                "educational_carousel": f"Swipe for {base_title} →"
            },
            "tiktok": {
                "trend_adaptation": f"POV: {base_title}",
                "educational_quick": f"{base_title} in 30 seconds!"
            },
            "twitter": {
                "controversial_take": f"Hot take: {base_title}",
                "thread_story": f"{base_title} - A Thread 🧵"
            },
            "facebook": {
                "discussion_starter": f"Let's talk about {base_title}",
                "behind_scenes": f"Behind the scenes: {base_title}"
            },
            "linkedin": {
                "industry_insight": f"Industry Insight: {base_title}",
                "professional_story": f"My Journey with {base_title}"
            },
            "pinterest": {
                "how_to_guide": f"How to {base_title} | Step by Step",
                "inspiration_board": f"{base_title} Ideas You'll Love"
            },
            "reddit": {
                "value_sharing": f"[Resource] {base_title}",
                "discussion_deep": f"Discussion: {base_title}"
            }
        }
        
        platform_titles = title_formats.get(platform, {})
        template = formula.get("template", "")
        
        return platform_titles.get(template, base_title)
    
    def _generate_description(self,
                            content_idea: ContentIdea,
                            platform: str,
                            formula: Dict) -> str:
        """Generate platform-optimized description"""
        
        base_desc = content_idea.description
        structure = formula.get("structure", "")
        
        # Add platform-specific elements
        platform_elements = {
            "youtube": "\n\n📚 Chapters:\n0:00 Intro\n\n🔔 Subscribe for more!",
            "instagram": "\n\n💾 Save this for later!\n.\n.\n.",
            "tiktok": "\n\n♥️ Double tap if this helped!",
            "twitter": "",  # Keep short
            "facebook": "\n\nWhat are your thoughts? 💭",
            "linkedin": "\n\nWhat's your experience with this?",
            "pinterest": "\n\n📌 Pin for later!",
            "reddit": "\n\nEDIT: Thanks for the awards!"
        }
        
        # Structure-based description
        desc = f"{base_desc}\n\n{structure}"
        
        # Add platform element
        desc += platform_elements.get(platform, "")
        
        return desc
    
    def _select_content_format(self, platform_config: Dict) -> str:
        """Select optimal content format"""
        
        specs = platform_config.get("content_specs", {})
        
        # Prioritize video formats for higher engagement
        if "video" in specs or "reels" in specs or "shorts" in specs:
            if "shorts" in specs:
                return "shorts"
            elif "reels" in specs:
                return "reels"
            else:
                return "video"
        
        # Default formats
        return list(specs.keys())[0] if specs else "standard"
    
    def _generate_hashtags(self,
                          content_idea: ContentIdea,
                          platform: str) -> List[str]:
        """Generate platform-optimized hashtags"""
        
        base_hashtags = content_idea.hashtags[:5]
        
        # Platform-specific hashtag strategies
        platform_hashtags = {
            "instagram": ["#reels", "#explore", "#viral"],
            "tiktok": ["#fyp", "#foryou", "#viral"],
            "twitter": [],  # Minimal hashtags
            "linkedin": ["#business", "#professional"],
            "facebook": ["#community"],
            "pinterest": ["#ideas", "#inspiration"],
            "youtube": ["#shorts", "#youtube"],
            "reddit": []  # No hashtags
        }
        
        platform_tags = platform_hashtags.get(platform, [])
        
        # Combine and limit based on platform
        hashtag_limits = {
            "instagram": 10,
            "tiktok": 5,
            "twitter": 2,
            "linkedin": 5,
            "facebook": 5,
            "pinterest": 20,
            "youtube": 15,
            "reddit": 0
        }
        
        limit = hashtag_limits.get(platform, 5)
        combined = (base_hashtags + platform_tags)[:limit]
        
        return combined
    
    def _get_media_specs(self, platform_config: Dict) -> Dict:
        """Get detailed media specifications"""
        
        specs = platform_config.get("content_specs", {})
        
        # Return first available format specs
        for format_name, format_specs in specs.items():
            if isinstance(format_specs, dict):
                return format_specs
        
        return {}
    
    def _get_optimization_elements(self, platform_config: Dict) -> List[str]:
        """Get platform-specific optimization elements"""
        
        elements = []
        
        # Add from optimization checklist
        if "optimization_checklist" in platform_config:
            elements.extend(platform_config["optimization_checklist"][:5])
        
        # Add from trending elements
        if "trending_elements" in platform_config:
            for key, value in platform_config["trending_elements"].items():
                elements.append(f"{key}: {value}")
        
        # Add from viral elements
        if "viral_elements" in platform_config:
            for key, value in platform_config["viral_elements"].items():
                elements.append(f"{key}: {value}")
        
        return elements[:10]  # Limit to 10 elements
    
    async def analyze_formula_performance(self, platform: str) -> Dict[str, Any]:
        """Analyze performance of different winning formulas"""
        
        platform_config = self.master_config["platforms"].get(platform, {})
        formulas = platform_config.get("winning_formulas", [])
        
        analysis = {
            "platform": platform,
            "category": platform_config.get("category", ""),
            "formula_performance": [],
            "recommendations": []
        }
        
        for formula in formulas:
            perf = {
                "template": formula["template"],
                "structure": formula["structure"],
                "base_engagement": formula.get("engagement_rate", "0%"),
                "best_for": formula.get("best_for", []),
                "key_elements": formula.get("key_elements", []),
                "estimated_reach": self._estimate_reach_from_engagement(
                    float(formula.get("engagement_rate", "0%").rstrip("%"))
                )
            }
            analysis["formula_performance"].append(perf)
        
        # Generate recommendations
        best_formula = max(formulas, 
                         key=lambda x: float(x.get("engagement_rate", "0%").rstrip("%")))
        
        analysis["recommendations"] = [
            f"Use '{best_formula['template']}' template for highest engagement",
            f"Structure content as: {best_formula['structure']}",
            f"Focus on: {', '.join(best_formula.get('key_elements', [])[:3])}"
        ]
        
        return analysis
    
    def _estimate_reach_from_engagement(self, engagement_rate: float) -> int:
        """Estimate potential reach from engagement rate"""
        
        # Simple estimation model
        base_reach = 1000
        
        if engagement_rate > 5:
            return base_reach * 100  # Viral potential
        elif engagement_rate > 3:
            return base_reach * 50   # High engagement
        elif engagement_rate > 1:
            return base_reach * 20   # Good engagement
        else:
            return base_reach * 10   # Standard reach
    
    async def get_automation_recommendations(self, 
                                            content_type: ContentType) -> Dict[str, Any]:
        """Get automation recommendations based on content type"""
        
        automation_settings = self.master_config.get("automation_settings", {})
        content_strategy = self.master_config.get("content_strategy", {})
        
        recommendations = {
            "content_type": content_type.value,
            "platform_priorities": [],
            "optimal_models": {},
            "posting_strategy": {},
            "cost_optimization": {}
        }
        
        # Determine platform priorities
        content_pillars = content_strategy.get("content_pillars", {})
        
        for pillar, config in content_pillars.items():
            if content_type.value.lower() in pillar:
                recommendations["platform_priorities"] = config.get("platforms", [])
                break
        
        # Model recommendations
        cost_opt = automation_settings.get("cost_optimization", {})
        
        if content_type in [ContentType.EDUCATIONAL, ContentType.INSPIRATIONAL]:
            recommendations["optimal_models"] = {
                "primary": cost_opt.get("complex_tasks", "claude-3-opus"),
                "secondary": cost_opt.get("primary_model", "claude-3-haiku")
            }
        else:
            recommendations["optimal_models"] = {
                "primary": cost_opt.get("primary_model", "claude-3-haiku"),
                "secondary": cost_opt.get("bulk_processing", "llama-70b-instruct")
            }
        
        # Posting strategy
        adaptation_rules = content_strategy.get("adaptation_rules", {})
        
        if content_type == ContentType.NEWS:
            recommendations["posting_strategy"] = adaptation_rules.get("simultaneous", {})
        elif content_type == ContentType.EDUCATIONAL:
            recommendations["posting_strategy"] = adaptation_rules.get("waterfall", {})
        else:
            recommendations["posting_strategy"] = adaptation_rules.get("test_and_scale", {})
        
        # Cost optimization tips
        recommendations["cost_optimization"] = {
            "batch_processing": "Group similar content for bulk processing",
            "model_selection": f"Use {recommendations['optimal_models']['primary']} for quality, "
                             f"{recommendations['optimal_models']['secondary']} for volume",
            "caching": "Cache platform optimizations for similar content",
            "scheduling": "Process during off-peak hours for better performance"
        }
        
        return recommendations


# Example usage
async def main():
    """Test the Enhanced Platform Optimizer"""
    
    optimizer = EnhancedPlatformOptimizer()
    
    # Create sample content
    content_idea = ContentIdea(
        title="5 AI Tools That Will Transform Your Business",
        description="Discover the latest AI tools that can automate your workflow and boost productivity",
        content_type=ContentType.EDUCATIONAL,
        target_audience="Business owners and marketers",
        key_message="AI can transform your business operations",
        call_to_action="Start using these tools today",
        keywords=["ai", "tools", "business", "automation", "productivity"],
        hashtags=["#AITools", "#BusinessAutomation", "#Productivity"]
    )
    
    print("="*60)
    print("ENHANCED PLATFORM OPTIMIZER - DEMONSTRATION")
    print("="*60)
    
    # Test platform optimization
    platforms = ["youtube", "instagram", "tiktok", "linkedin"]
    
    print(f"\nOptimizing content for {len(platforms)} platforms...")
    
    results = await optimizer.generate_platform_specific_content(content_idea, platforms)
    
    for platform, data in results.items():
        print(f"\n{platform.upper()}:")
        print(f"  Category: {data['optimization']['category']}")
        print(f"  Template: {data['optimization']['template']}")
        print(f"  Optimization Score: {data['optimization']['score']:.1f}/100")
        print(f"  Est. Engagement: {data['optimization']['estimated_engagement']:.2%}")
        print(f"  Best Time: {data['optimization']['posting_time']}")
        print(f"  Title: {data['content']['title']}")
        print(f"  Format: {data['content']['format']}")
    
    # Analyze formula performance
    print("\n" + "-"*40)
    print("FORMULA PERFORMANCE ANALYSIS")
    print("-"*40)
    
    for platform in ["youtube", "tiktok"]:
        analysis = await optimizer.analyze_formula_performance(platform)
        print(f"\n{platform.upper()}:")
        for formula in analysis["formula_performance"][:2]:
            print(f"  {formula['template']}: {formula['base_engagement']} engagement")
        print(f"  Recommendation: {analysis['recommendations'][0]}")
    
    # Get automation recommendations
    print("\n" + "-"*40)
    print("AUTOMATION RECOMMENDATIONS")
    print("-"*40)
    
    auto_recs = await optimizer.get_automation_recommendations(ContentType.EDUCATIONAL)
    print(f"\nContent Type: {auto_recs['content_type']}")
    print(f"Priority Platforms: {', '.join(auto_recs['platform_priorities'])}")
    print(f"Optimal Model: {auto_recs['optimal_models']['primary']}")
    print(f"Cost Optimization: {auto_recs['cost_optimization']['model_selection']}")
    
    print("\n" + "="*60)
    print("OPTIMIZATION COMPLETE!")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(main())