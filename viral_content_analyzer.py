"""
Viral Content Analyzer
Analyzes content performance across platforms to identify viral patterns and optimize future content
"""

import json
import asyncio
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import statistics
import re
from collections import Counter, defaultdict

# Import existing modules
from content_transformation_engine import PlatformName, ContentType
from cpu_manager import get_cpu_manager

class ViralityStatus(Enum):
    """Content virality classification"""
    VIRAL = "viral"  # Top 1% performance
    TRENDING = "trending"  # Top 5% performance
    PERFORMING = "performing"  # Above average
    STANDARD = "standard"  # Average performance
    UNDERPERFORMING = "underperforming"  # Below average

@dataclass
class ContentMetrics:
    """Metrics for analyzing content performance"""
    platform: PlatformName
    content_id: str
    title: str
    content_type: ContentType
    posted_at: datetime
    
    # Engagement metrics
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    saves: int = 0
    
    # Calculated metrics
    engagement_rate: float = 0.0
    viral_velocity: float = 0.0  # Growth rate in first 24 hours
    viral_score: float = 0.0  # Overall viral potential score
    
    # Content attributes
    hashtags: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    media_type: str = ""
    duration_seconds: Optional[int] = None
    word_count: Optional[int] = None
    
    # Performance indicators
    completion_rate: Optional[float] = None
    click_through_rate: Optional[float] = None
    conversion_rate: Optional[float] = None

@dataclass
class ViralPattern:
    """Identified viral content pattern"""
    pattern_name: str
    platform: PlatformName
    content_type: ContentType
    
    # Pattern characteristics
    common_elements: Dict[str, Any]
    success_rate: float
    avg_viral_score: float
    sample_size: int
    
    # Optimal conditions
    best_posting_time: str
    optimal_length: str
    key_hashtags: List[str]
    engagement_hooks: List[str]
    
    # Performance benchmarks
    min_engagement_rate: float
    avg_views: int
    avg_shares: int

class ViralContentAnalyzer:
    """Analyze content performance and identify viral patterns"""
    
    def __init__(self, project_id: str = None):
        self.project_id = project_id or "auto-marketing"
        self.base_path = Path("C:/Auto Marketing")
        self.analytics_path = self.base_path / "analytics"
        self.analytics_path.mkdir(exist_ok=True)
        
        self.cpu_manager = get_cpu_manager(max_cpu=75.0)
        
        # Performance benchmarks by platform
        self.platform_benchmarks = self._load_platform_benchmarks()
        
        # Historical data storage
        self.content_database: List[ContentMetrics] = []
        self.viral_patterns: Dict[str, ViralPattern] = {}
        
        # Load historical data if exists
        self._load_historical_data()
    
    def _load_platform_benchmarks(self) -> Dict[PlatformName, Dict[str, float]]:
        """Load platform-specific performance benchmarks"""
        
        return {
            PlatformName.TIKTOK: {
                "viral_threshold": 1000000,  # views
                "trending_threshold": 100000,
                "engagement_rate_good": 0.15,
                "share_rate_good": 0.05,
                "completion_rate_good": 0.50
            },
            PlatformName.YOUTUBE: {
                "viral_threshold": 1000000,
                "trending_threshold": 100000,
                "engagement_rate_good": 0.04,
                "ctr_good": 0.10,
                "retention_good": 0.50
            },
            PlatformName.INSTAGRAM: {
                "viral_threshold": 100000,
                "trending_threshold": 10000,
                "engagement_rate_good": 0.06,
                "save_rate_good": 0.03,
                "reach_rate_good": 0.50
            },
            PlatformName.TWITTER: {
                "viral_threshold": 50000,
                "trending_threshold": 5000,
                "engagement_rate_good": 0.03,
                "retweet_rate_good": 0.02
            },
            PlatformName.LINKEDIN: {
                "viral_threshold": 50000,
                "trending_threshold": 5000,
                "engagement_rate_good": 0.04,
                "share_rate_good": 0.02
            },
            PlatformName.FACEBOOK: {
                "viral_threshold": 100000,
                "trending_threshold": 10000,
                "engagement_rate_good": 0.03,
                "share_rate_good": 0.01
            },
            PlatformName.PINTEREST: {
                "viral_threshold": 50000,
                "trending_threshold": 5000,
                "save_rate_good": 0.05,
                "click_rate_good": 0.02
            },
            PlatformName.REDDIT: {
                "viral_threshold": 10000,
                "trending_threshold": 1000,
                "upvote_ratio_good": 0.85,
                "comment_rate_good": 0.10
            }
        }
    
    def _load_historical_data(self):
        """Load historical content performance data"""
        
        history_file = self.analytics_path / "content_history.json"
        if history_file.exists():
            with open(history_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Convert to ContentMetrics objects
                for item in data.get("content", []):
                    self.content_database.append(self._dict_to_metrics(item))
        
        patterns_file = self.analytics_path / "viral_patterns.json"
        if patterns_file.exists():
            with open(patterns_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Convert to ViralPattern objects
                for key, pattern_data in data.items():
                    self.viral_patterns[key] = self._dict_to_pattern(pattern_data)
    
    def _dict_to_metrics(self, data: Dict) -> ContentMetrics:
        """Convert dictionary to ContentMetrics object"""
        
        return ContentMetrics(
            platform=PlatformName(data["platform"]),
            content_id=data["content_id"],
            title=data["title"],
            content_type=ContentType(data["content_type"]),
            posted_at=datetime.fromisoformat(data["posted_at"]),
            views=data.get("views", 0),
            likes=data.get("likes", 0),
            comments=data.get("comments", 0),
            shares=data.get("shares", 0),
            saves=data.get("saves", 0),
            engagement_rate=data.get("engagement_rate", 0.0),
            viral_velocity=data.get("viral_velocity", 0.0),
            viral_score=data.get("viral_score", 0.0),
            hashtags=data.get("hashtags", []),
            keywords=data.get("keywords", []),
            media_type=data.get("media_type", ""),
            duration_seconds=data.get("duration_seconds"),
            word_count=data.get("word_count"),
            completion_rate=data.get("completion_rate"),
            click_through_rate=data.get("click_through_rate"),
            conversion_rate=data.get("conversion_rate")
        )
    
    def _dict_to_pattern(self, data: Dict) -> ViralPattern:
        """Convert dictionary to ViralPattern object"""
        
        return ViralPattern(
            pattern_name=data["pattern_name"],
            platform=PlatformName(data["platform"]),
            content_type=ContentType(data["content_type"]),
            common_elements=data["common_elements"],
            success_rate=data["success_rate"],
            avg_viral_score=data["avg_viral_score"],
            sample_size=data["sample_size"],
            best_posting_time=data["best_posting_time"],
            optimal_length=data["optimal_length"],
            key_hashtags=data["key_hashtags"],
            engagement_hooks=data["engagement_hooks"],
            min_engagement_rate=data["min_engagement_rate"],
            avg_views=data["avg_views"],
            avg_shares=data["avg_shares"]
        )
    
    async def analyze_content(self, metrics: ContentMetrics) -> Dict[str, Any]:
        """Analyze a single piece of content for viral potential"""
        
        await self.cpu_manager.check_and_throttle()
        
        # Calculate engagement rate if not provided
        if metrics.engagement_rate == 0 and metrics.views > 0:
            metrics.engagement_rate = (
                metrics.likes + metrics.comments + metrics.shares + metrics.saves
            ) / metrics.views
        
        # Calculate viral velocity (growth in first 24 hours)
        hours_since_post = (datetime.now() - metrics.posted_at).total_seconds() / 3600
        if hours_since_post <= 24 and metrics.views > 0:
            metrics.viral_velocity = metrics.views / max(1, hours_since_post)
        
        # Calculate viral score
        metrics.viral_score = self._calculate_viral_score(metrics)
        
        # Determine virality status
        status = self._determine_virality_status(metrics)
        
        # Identify successful elements
        successful_elements = self._identify_successful_elements(metrics)
        
        # Get improvement suggestions
        suggestions = self._generate_improvement_suggestions(metrics, status)
        
        # Store in database
        self.content_database.append(metrics)
        
        analysis = {
            "content_id": metrics.content_id,
            "platform": metrics.platform.value,
            "viral_score": metrics.viral_score,
            "virality_status": status.value,
            "engagement_rate": metrics.engagement_rate,
            "viral_velocity": metrics.viral_velocity,
            "successful_elements": successful_elements,
            "improvement_suggestions": suggestions,
            "benchmark_comparison": self._compare_to_benchmarks(metrics)
        }
        
        return analysis
    
    def _calculate_viral_score(self, metrics: ContentMetrics) -> float:
        """Calculate overall viral score (0-100)"""
        
        score = 0.0
        benchmarks = self.platform_benchmarks.get(metrics.platform, {})
        
        # Views component (40% weight)
        viral_threshold = benchmarks.get("viral_threshold", 100000)
        views_score = min(40, (metrics.views / viral_threshold) * 40)
        score += views_score
        
        # Engagement rate component (30% weight)
        good_engagement = benchmarks.get("engagement_rate_good", 0.05)
        engagement_score = min(30, (metrics.engagement_rate / good_engagement) * 30)
        score += engagement_score
        
        # Share rate component (20% weight)
        if metrics.views > 0:
            share_rate = metrics.shares / metrics.views
            good_share_rate = benchmarks.get("share_rate_good", 0.02)
            share_score = min(20, (share_rate / good_share_rate) * 20)
            score += share_score
        
        # Velocity component (10% weight)
        if metrics.viral_velocity > 0:
            velocity_benchmark = viral_threshold / 24  # Views per hour for viral
            velocity_score = min(10, (metrics.viral_velocity / velocity_benchmark) * 10)
            score += velocity_score
        
        return min(100, score)
    
    def _determine_virality_status(self, metrics: ContentMetrics) -> ViralityStatus:
        """Determine content's virality status"""
        
        benchmarks = self.platform_benchmarks.get(metrics.platform, {})
        
        if metrics.views >= benchmarks.get("viral_threshold", 1000000):
            return ViralityStatus.VIRAL
        elif metrics.views >= benchmarks.get("trending_threshold", 100000):
            return ViralityStatus.TRENDING
        elif metrics.engagement_rate >= benchmarks.get("engagement_rate_good", 0.05):
            return ViralityStatus.PERFORMING
        elif metrics.engagement_rate >= benchmarks.get("engagement_rate_good", 0.05) * 0.5:
            return ViralityStatus.STANDARD
        else:
            return ViralityStatus.UNDERPERFORMING
    
    def _identify_successful_elements(self, metrics: ContentMetrics) -> List[str]:
        """Identify what made the content successful"""
        
        elements = []
        benchmarks = self.platform_benchmarks.get(metrics.platform, {})
        
        # Check engagement rate
        if metrics.engagement_rate >= benchmarks.get("engagement_rate_good", 0.05):
            elements.append(f"High engagement rate: {metrics.engagement_rate:.2%}")
        
        # Check share rate
        if metrics.views > 0:
            share_rate = metrics.shares / metrics.views
            if share_rate >= benchmarks.get("share_rate_good", 0.02):
                elements.append(f"High share rate: {share_rate:.2%}")
        
        # Check completion rate for video
        if metrics.completion_rate and metrics.completion_rate >= benchmarks.get("completion_rate_good", 0.50):
            elements.append(f"High completion rate: {metrics.completion_rate:.2%}")
        
        # Check viral velocity
        if metrics.viral_velocity > benchmarks.get("viral_threshold", 100000) / 24:
            elements.append(f"Fast viral velocity: {metrics.viral_velocity:.0f} views/hour")
        
        # Check hashtag performance
        if metrics.hashtags:
            elements.append(f"Effective hashtags: {', '.join(metrics.hashtags[:3])}")
        
        return elements
    
    def _generate_improvement_suggestions(self, 
                                         metrics: ContentMetrics, 
                                         status: ViralityStatus) -> List[str]:
        """Generate suggestions for improving content performance"""
        
        suggestions = []
        benchmarks = self.platform_benchmarks.get(metrics.platform, {})
        
        # Engagement rate improvements
        if metrics.engagement_rate < benchmarks.get("engagement_rate_good", 0.05):
            suggestions.append("Improve engagement: Add stronger call-to-action")
            suggestions.append("Use more engaging hooks in the first 3 seconds")
        
        # Share rate improvements
        if metrics.views > 0:
            share_rate = metrics.shares / metrics.views
            if share_rate < benchmarks.get("share_rate_good", 0.02):
                suggestions.append("Make content more shareable: Add value or entertainment")
                suggestions.append("Include share prompts in content")
        
        # Platform-specific suggestions
        platform_suggestions = self._get_platform_specific_suggestions(metrics)
        suggestions.extend(platform_suggestions)
        
        # Content type suggestions
        if status == ViralityStatus.UNDERPERFORMING:
            suggestions.append(f"Consider switching to {self._suggest_better_content_type(metrics)}")
            suggestions.append("Analyze top-performing content in your niche")
        
        return suggestions[:5]  # Return top 5 suggestions
    
    def _get_platform_specific_suggestions(self, metrics: ContentMetrics) -> List[str]:
        """Get platform-specific improvement suggestions"""
        
        suggestions = []
        
        if metrics.platform == PlatformName.TIKTOK:
            if not metrics.completion_rate or metrics.completion_rate < 0.5:
                suggestions.append("Improve video hook in first 3 seconds")
            if metrics.duration_seconds and metrics.duration_seconds > 60:
                suggestions.append("Consider shorter videos (15-30 seconds)")
                
        elif metrics.platform == PlatformName.YOUTUBE:
            if metrics.click_through_rate and metrics.click_through_rate < 0.1:
                suggestions.append("Improve thumbnail and title")
            if metrics.duration_seconds and metrics.duration_seconds < 480:
                suggestions.append("Consider longer videos (8+ minutes) for mid-roll ads")
                
        elif metrics.platform == PlatformName.INSTAGRAM:
            if len(metrics.hashtags) < 5:
                suggestions.append("Use 8-15 relevant hashtags")
            if metrics.saves < metrics.likes * 0.1:
                suggestions.append("Create more save-worthy content")
        
        return suggestions
    
    def _suggest_better_content_type(self, metrics: ContentMetrics) -> str:
        """Suggest a better performing content type"""
        
        # Find best performing content type for this platform
        platform_content = [m for m in self.content_database if m.platform == metrics.platform]
        
        if platform_content:
            type_performance = defaultdict(list)
            for content in platform_content:
                type_performance[content.content_type].append(content.viral_score)
            
            # Calculate average scores
            avg_scores = {
                content_type: statistics.mean(scores) 
                for content_type, scores in type_performance.items()
            }
            
            # Find best performing type
            if avg_scores:
                best_type = max(avg_scores, key=avg_scores.get)
                if best_type != metrics.content_type:
                    return f"{best_type.value} content"
        
        return "trending content formats"
    
    def _compare_to_benchmarks(self, metrics: ContentMetrics) -> Dict[str, str]:
        """Compare metrics to platform benchmarks"""
        
        benchmarks = self.platform_benchmarks.get(metrics.platform, {})
        comparison = {}
        
        # Engagement rate comparison
        good_engagement = benchmarks.get("engagement_rate_good", 0.05)
        if metrics.engagement_rate >= good_engagement:
            comparison["engagement"] = f"Above average ({metrics.engagement_rate:.2%} vs {good_engagement:.2%})"
        else:
            comparison["engagement"] = f"Below average ({metrics.engagement_rate:.2%} vs {good_engagement:.2%})"
        
        # Views comparison
        trending_threshold = benchmarks.get("trending_threshold", 10000)
        if metrics.views >= trending_threshold:
            comparison["reach"] = f"Trending level ({metrics.views:,} views)"
        else:
            comparison["reach"] = f"Building momentum ({metrics.views:,} views)"
        
        return comparison
    
    async def identify_viral_patterns(self, 
                                     platform: Optional[PlatformName] = None,
                                     min_sample_size: int = 10) -> List[ViralPattern]:
        """Identify patterns in viral content"""
        
        await self.cpu_manager.check_and_throttle()
        
        patterns = []
        
        # Filter content by platform if specified
        if platform:
            content_pool = [m for m in self.content_database if m.platform == platform]
        else:
            content_pool = self.content_database
        
        # Group by content type
        type_groups = defaultdict(list)
        for content in content_pool:
            if content.viral_score >= 70:  # Only analyze high-performing content
                type_groups[content.content_type].append(content)
        
        # Analyze each group
        for content_type, contents in type_groups.items():
            if len(contents) >= min_sample_size:
                pattern = self._analyze_pattern(contents, content_type)
                if pattern:
                    patterns.append(pattern)
                    # Store pattern
                    pattern_key = f"{pattern.platform.value}_{pattern.content_type.value}"
                    self.viral_patterns[pattern_key] = pattern
        
        return patterns
    
    def _analyze_pattern(self, contents: List[ContentMetrics], 
                        content_type: ContentType) -> Optional[ViralPattern]:
        """Analyze a group of content to identify patterns"""
        
        if not contents:
            return None
        
        # Find common elements
        common_hashtags = Counter()
        common_keywords = Counter()
        posting_times = []
        lengths = []
        hooks = []
        
        for content in contents:
            common_hashtags.update(content.hashtags)
            common_keywords.update(content.keywords)
            posting_times.append(content.posted_at.hour)
            
            if content.duration_seconds:
                lengths.append(content.duration_seconds)
            elif content.word_count:
                lengths.append(content.word_count)
        
        # Calculate pattern metrics
        pattern = ViralPattern(
            pattern_name=f"{content_type.value}_viral_pattern",
            platform=contents[0].platform,
            content_type=content_type,
            common_elements={
                "hashtags": dict(common_hashtags.most_common(5)),
                "keywords": dict(common_keywords.most_common(5)),
                "posting_hours": Counter(posting_times).most_common(3)
            },
            success_rate=len(contents) / max(1, len([c for c in self.content_database 
                                                    if c.content_type == content_type])),
            avg_viral_score=statistics.mean([c.viral_score for c in contents]),
            sample_size=len(contents),
            best_posting_time=f"{Counter(posting_times).most_common(1)[0][0]}:00" if posting_times else "12:00",
            optimal_length=f"{statistics.mean(lengths):.0f}" if lengths else "N/A",
            key_hashtags=[tag for tag, _ in common_hashtags.most_common(5)],
            engagement_hooks=self._extract_common_hooks(contents),
            min_engagement_rate=min([c.engagement_rate for c in contents]),
            avg_views=int(statistics.mean([c.views for c in contents])),
            avg_shares=int(statistics.mean([c.shares for c in contents]))
        )
        
        return pattern
    
    def _extract_common_hooks(self, contents: List[ContentMetrics]) -> List[str]:
        """Extract common engagement hooks from viral content"""
        
        hooks = []
        
        # Extract patterns from titles
        title_words = Counter()
        for content in contents:
            # Simple word extraction (in production, use NLP)
            words = content.title.lower().split()
            title_words.update(words)
        
        # Find common starting phrases
        common_starts = []
        for content in contents:
            if content.title:
                start = " ".join(content.title.split()[:3])
                common_starts.append(start)
        
        # Get most common patterns
        start_counter = Counter(common_starts)
        for start, count in start_counter.most_common(3):
            if count > 1:
                hooks.append(start)
        
        # Add generic hooks based on content type
        if contents[0].content_type == ContentType.EDUCATIONAL:
            hooks.extend(["How to", "5 Ways to", "The Secret to"])
        elif contents[0].content_type == ContentType.ENTERTAINMENT:
            hooks.extend(["You won't believe", "Wait for it", "POV:"])
        
        return hooks[:5]
    
    async def predict_viral_potential(self, 
                                     title: str,
                                     content_type: ContentType,
                                     platform: PlatformName,
                                     hashtags: List[str] = None) -> Dict[str, Any]:
        """Predict viral potential of new content"""
        
        await self.cpu_manager.check_and_throttle()
        
        # Find relevant pattern
        pattern_key = f"{platform.value}_{content_type.value}"
        pattern = self.viral_patterns.get(pattern_key)
        
        score = 50.0  # Base score
        
        if pattern:
            # Check title alignment with successful hooks
            for hook in pattern.engagement_hooks:
                if hook.lower() in title.lower():
                    score += 10
                    break
            
            # Check hashtag alignment
            if hashtags and pattern.key_hashtags:
                matching_hashtags = set(hashtags) & set(pattern.key_hashtags)
                score += len(matching_hashtags) * 5
            
            # Apply success rate modifier
            score *= (1 + pattern.success_rate)
        
        # Platform-specific adjustments
        platform_modifiers = {
            PlatformName.TIKTOK: 1.3,
            PlatformName.YOUTUBE: 1.2,
            PlatformName.INSTAGRAM: 1.1,
            PlatformName.TWITTER: 1.15,
            PlatformName.REDDIT: 1.1,
            PlatformName.LINKEDIN: 0.9,
            PlatformName.FACEBOOK: 1.0,
            PlatformName.PINTEREST: 0.95
        }
        
        score *= platform_modifiers.get(platform, 1.0)
        
        # Cap at 100
        score = min(100, score)
        
        prediction = {
            "viral_potential_score": score,
            "likelihood": self._score_to_likelihood(score),
            "recommended_optimizations": [],
            "best_posting_time": pattern.best_posting_time if pattern else "12:00 PM",
            "expected_reach": self._estimate_reach_from_score(score, platform)
        }
        
        # Add optimization recommendations
        if score < 70:
            if pattern:
                prediction["recommended_optimizations"].append(
                    f"Use hooks like: {', '.join(pattern.engagement_hooks[:2])}"
                )
                prediction["recommended_optimizations"].append(
                    f"Include hashtags: {', '.join(pattern.key_hashtags[:3])}"
                )
            prediction["recommended_optimizations"].append(
                "Optimize posting time for maximum audience availability"
            )
        
        return prediction
    
    def _score_to_likelihood(self, score: float) -> str:
        """Convert score to likelihood description"""
        
        if score >= 80:
            return "Very High"
        elif score >= 60:
            return "High"
        elif score >= 40:
            return "Medium"
        elif score >= 20:
            return "Low"
        else:
            return "Very Low"
    
    def _estimate_reach_from_score(self, score: float, platform: PlatformName) -> int:
        """Estimate potential reach based on viral score"""
        
        benchmarks = self.platform_benchmarks.get(platform, {})
        viral_threshold = benchmarks.get("viral_threshold", 100000)
        
        # Exponential growth based on score
        if score >= 80:
            return int(viral_threshold * (score / 100))
        elif score >= 60:
            return int(viral_threshold * 0.1 * (score / 100))
        elif score >= 40:
            return int(viral_threshold * 0.01 * (score / 100))
        else:
            return int(viral_threshold * 0.001 * (score / 100))
    
    async def generate_viral_report(self, 
                                   platform: Optional[PlatformName] = None) -> Dict[str, Any]:
        """Generate comprehensive viral content report"""
        
        await self.cpu_manager.check_and_throttle()
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "total_content_analyzed": len(self.content_database),
            "platforms": {},
            "top_performers": [],
            "viral_patterns": [],
            "recommendations": []
        }
        
        # Analyze by platform
        platforms = [platform] if platform else list(PlatformName)
        
        for plat in platforms:
            platform_content = [c for c in self.content_database if c.platform == plat]
            
            if platform_content:
                viral_content = [c for c in platform_content if c.viral_score >= 70]
                
                report["platforms"][plat.value] = {
                    "total_content": len(platform_content),
                    "viral_content": len(viral_content),
                    "viral_rate": len(viral_content) / len(platform_content),
                    "avg_engagement_rate": statistics.mean([c.engagement_rate for c in platform_content]),
                    "avg_viral_score": statistics.mean([c.viral_score for c in platform_content]),
                    "best_content_type": self._get_best_content_type(platform_content)
                }
        
        # Get top performers
        top_content = sorted(self.content_database, key=lambda x: x.viral_score, reverse=True)[:10]
        for content in top_content:
            report["top_performers"].append({
                "title": content.title,
                "platform": content.platform.value,
                "viral_score": content.viral_score,
                "views": content.views,
                "engagement_rate": content.engagement_rate
            })
        
        # Include viral patterns
        patterns = await self.identify_viral_patterns(platform)
        for pattern in patterns:
            report["viral_patterns"].append({
                "pattern": pattern.pattern_name,
                "platform": pattern.platform.value,
                "success_rate": pattern.success_rate,
                "key_elements": pattern.common_elements
            })
        
        # Generate recommendations
        report["recommendations"] = self._generate_strategic_recommendations(report)
        
        # Save report
        await self._save_report(report)
        
        return report
    
    def _get_best_content_type(self, content_list: List[ContentMetrics]) -> str:
        """Identify best performing content type"""
        
        type_scores = defaultdict(list)
        for content in content_list:
            type_scores[content.content_type].append(content.viral_score)
        
        if type_scores:
            avg_scores = {
                ct.value: statistics.mean(scores) 
                for ct, scores in type_scores.items()
            }
            return max(avg_scores, key=avg_scores.get)
        
        return "unknown"
    
    def _generate_strategic_recommendations(self, report: Dict) -> List[str]:
        """Generate strategic recommendations based on analysis"""
        
        recommendations = []
        
        # Platform-specific recommendations
        for platform, data in report["platforms"].items():
            if data["viral_rate"] < 0.05:
                recommendations.append(
                    f"Improve {platform} content: Focus on {data['best_content_type']} format"
                )
            
            if data["avg_engagement_rate"] < 0.03:
                recommendations.append(
                    f"Boost {platform} engagement: Add stronger CTAs and hooks"
                )
        
        # Pattern-based recommendations
        if report["viral_patterns"]:
            recommendations.append(
                "Leverage identified viral patterns in future content creation"
            )
        
        # General recommendations
        if report["total_content_analyzed"] < 100:
            recommendations.append(
                "Increase content volume to gather more performance data"
            )
        
        recommendations.append(
            "A/B test different content formats to identify platform-specific preferences"
        )
        
        return recommendations[:7]
    
    async def _save_report(self, report: Dict):
        """Save viral analysis report"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"viral_report_{timestamp}.json"
        filepath = self.analytics_path / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        print(f"Viral analysis report saved to: {filepath}")
    
    async def save_data(self):
        """Save analyzer data to disk"""
        
        # Save content database
        history_data = {
            "content": [
                {
                    "platform": m.platform.value,
                    "content_id": m.content_id,
                    "title": m.title,
                    "content_type": m.content_type.value,
                    "posted_at": m.posted_at.isoformat(),
                    "views": m.views,
                    "likes": m.likes,
                    "comments": m.comments,
                    "shares": m.shares,
                    "saves": m.saves,
                    "engagement_rate": m.engagement_rate,
                    "viral_velocity": m.viral_velocity,
                    "viral_score": m.viral_score,
                    "hashtags": m.hashtags,
                    "keywords": m.keywords,
                    "media_type": m.media_type,
                    "duration_seconds": m.duration_seconds,
                    "word_count": m.word_count,
                    "completion_rate": m.completion_rate,
                    "click_through_rate": m.click_through_rate,
                    "conversion_rate": m.conversion_rate
                }
                for m in self.content_database
            ]
        }
        
        history_file = self.analytics_path / "content_history.json"
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=2)
        
        # Save viral patterns
        patterns_data = {}
        for key, pattern in self.viral_patterns.items():
            patterns_data[key] = {
                "pattern_name": pattern.pattern_name,
                "platform": pattern.platform.value,
                "content_type": pattern.content_type.value,
                "common_elements": pattern.common_elements,
                "success_rate": pattern.success_rate,
                "avg_viral_score": pattern.avg_viral_score,
                "sample_size": pattern.sample_size,
                "best_posting_time": pattern.best_posting_time,
                "optimal_length": pattern.optimal_length,
                "key_hashtags": pattern.key_hashtags,
                "engagement_hooks": pattern.engagement_hooks,
                "min_engagement_rate": pattern.min_engagement_rate,
                "avg_views": pattern.avg_views,
                "avg_shares": pattern.avg_shares
            }
        
        patterns_file = self.analytics_path / "viral_patterns.json"
        with open(patterns_file, 'w', encoding='utf-8') as f:
            json.dump(patterns_data, f, indent=2)


# Example usage
async def main():
    """Example usage of Viral Content Analyzer"""
    
    analyzer = ViralContentAnalyzer()
    
    # Create sample metrics
    sample_content = ContentMetrics(
        platform=PlatformName.TIKTOK,
        content_id="sample_001",
        title="5 Marketing Hacks That Actually Work",
        content_type=ContentType.EDUCATIONAL,
        posted_at=datetime.now() - timedelta(hours=12),
        views=150000,
        likes=22000,
        comments=1800,
        shares=3500,
        saves=5000,
        hashtags=["#MarketingTips", "#BusinessGrowth", "#Entrepreneur"],
        keywords=["marketing", "growth", "hacks", "business"],
        media_type="video",
        duration_seconds=45,
        completion_rate=0.72
    )
    
    # Analyze content
    print("Analyzing content performance...")
    analysis = await analyzer.analyze_content(sample_content)
    
    print(f"\nContent Analysis:")
    print(f"Viral Score: {analysis['viral_score']:.1f}/100")
    print(f"Status: {analysis['virality_status']}")
    print(f"Engagement Rate: {analysis['engagement_rate']:.2%}")
    
    print(f"\nSuccessful Elements:")
    for element in analysis['successful_elements']:
        print(f"  - {element}")
    
    print(f"\nImprovement Suggestions:")
    for suggestion in analysis['improvement_suggestions']:
        print(f"  - {suggestion}")
    
    # Predict viral potential
    print("\n" + "="*50)
    print("Predicting viral potential for new content...")
    
    prediction = await analyzer.predict_viral_potential(
        title="POV: You discover this one marketing secret",
        content_type=ContentType.EDUCATIONAL,
        platform=PlatformName.TIKTOK,
        hashtags=["#MarketingSecret", "#POV", "#BusinessTips"]
    )
    
    print(f"\nViral Potential Score: {prediction['viral_potential_score']:.1f}/100")
    print(f"Likelihood: {prediction['likelihood']}")
    print(f"Best Posting Time: {prediction['best_posting_time']}")
    print(f"Expected Reach: {prediction['expected_reach']:,}")
    
    # Generate report
    print("\n" + "="*50)
    print("Generating viral content report...")
    
    report = await analyzer.generate_viral_report()
    print(f"\nReport generated with {len(report['top_performers'])} top performers")
    print(f"Identified {len(report['viral_patterns'])} viral patterns")
    
    # Save data
    await analyzer.save_data()
    print("\nAnalyzer data saved successfully")

if __name__ == "__main__":
    asyncio.run(main())