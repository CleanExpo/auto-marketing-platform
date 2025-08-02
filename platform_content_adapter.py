#!/usr/bin/env python3
"""
Platform Content Adapter - Automated Multi-Platform Content Optimization
Transforms single content into platform-specific variations with CPU protection
"""

import json
import re
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import hashlib
from cpu_manager import get_cpu_manager, ProcessThrottler

@dataclass
class ContentPiece:
    """Base content structure"""
    title: str
    main_message: str
    key_points: List[str]
    call_to_action: str
    tags: List[str]
    media_assets: Optional[List[str]] = None
    brand_voice: str = "professional"
    target_audience: str = "general"

@dataclass
class PlatformContent:
    """Platform-specific content adaptation"""
    platform: str
    format_type: str
    title: str
    content: str
    hashtags: List[str]
    media_specs: Dict[str, Any]
    optimal_timing: Dict[str, Any]
    estimated_engagement: float

class PlatformContentAdapter:
    """
    Main content adaptation engine with CPU-optimized processing
    """
    
    def __init__(self):
        self.cpu_manager = get_cpu_manager(max_cpu=75.0)
        self.throttler = ProcessThrottler(self.cpu_manager)
        self.load_platform_configs()
        self.load_winning_formulas()
        
    def load_platform_configs(self):
        """Load platform-specific configurations"""
        import os
        base_path = r'C:\Auto Marketing'
        
        platform_file = os.path.join(base_path, 'platform-analysis.json')
        if os.path.exists(platform_file):
            with open(platform_file, 'r') as f:
                self.platform_data = json.load(f)
        else:
            # Use default data if file doesn't exist
            self.platform_data = {"platforms": {}}
        
        formulas_file = os.path.join(base_path, 'winning-formulas.json')
        if os.path.exists(formulas_file):
            with open(formulas_file, 'r') as f:
                self.formulas = json.load(f)
        else:
            self.formulas = {}
            
        templates_file = os.path.join(base_path, 'content-templates.json')
        if os.path.exists(templates_file):
            with open(templates_file, 'r') as f:
                self.templates = json.load(f)
        else:
            self.templates = {}
    
    def load_winning_formulas(self):
        """Load performance benchmarks and winning formulas"""
        import os
        base_path = r'C:\Auto Marketing'
        benchmarks_file = os.path.join(base_path, 'performance-benchmarks.json')
        
        if os.path.exists(benchmarks_file):
            with open(benchmarks_file, 'r') as f:
                self.benchmarks = json.load(f)
        else:
            self.benchmarks = {}
    
    def adapt_content(self, source_content: ContentPiece) -> Dict[str, PlatformContent]:
        """
        Transform single content into platform-specific variations
        Uses CPU throttling to prevent system overload
        """
        adaptations = {}
        
        # Process platforms with CPU protection
        platforms = ['youtube', 'instagram', 'tiktok', 'facebook', 
                    'twitter', 'linkedin', 'pinterest', 'reddit']
        
        for platform in platforms:
            # Wait for CPU if needed
            self.cpu_manager.wait_for_cpu()
            
            # Adapt content for platform
            adapted = self.cpu_manager.throttled_execute(
                self._adapt_for_platform,
                source_content,
                platform
            )
            
            adaptations[platform] = adapted
            
            # Brief pause between platforms
            self.cpu_manager.adaptive_sleep(0.5)
        
        return adaptations
    
    def _adapt_for_platform(self, content: ContentPiece, platform: str) -> PlatformContent:
        """Adapt content for specific platform"""
        
        if platform == 'youtube':
            return self._adapt_youtube(content)
        elif platform == 'instagram':
            return self._adapt_instagram(content)
        elif platform == 'tiktok':
            return self._adapt_tiktok(content)
        elif platform == 'facebook':
            return self._adapt_facebook(content)
        elif platform == 'twitter':
            return self._adapt_twitter(content)
        elif platform == 'linkedin':
            return self._adapt_linkedin(content)
        elif platform == 'pinterest':
            return self._adapt_pinterest(content)
        elif platform == 'reddit':
            return self._adapt_reddit(content)
    
    def _adapt_youtube(self, content: ContentPiece) -> PlatformContent:
        """Adapt content for YouTube"""
        
        # Long-form video structure
        title = self._create_youtube_title(content)
        
        script = f"""
[HOOK - 0:00-0:15]
{self._create_hook(content.main_message, 'youtube')}

[PREVIEW - 0:15-0:30]
In this video, you'll learn:
{chr(10).join(f'• {point}' for point in content.key_points[:3])}

[MAIN CONTENT - 0:30-7:30]
{self._expand_content(content, 'detailed')}

[SUMMARY - 7:30-8:00]
Key takeaways:
{chr(10).join(f'{i+1}. {point}' for i, point in enumerate(content.key_points))}

[CTA - 8:00-8:30]
{content.call_to_action}
Don't forget to subscribe and hit the notification bell!
"""
        
        return PlatformContent(
            platform='youtube',
            format_type='long_form_educational',
            title=title,
            content=script,
            hashtags=self._generate_hashtags(content.tags, 'youtube'),
            media_specs={
                'duration': '8-15 minutes',
                'resolution': '1920x1080',
                'thumbnail': 'custom_required',
                'chapters': True,
                'end_screen': True
            },
            optimal_timing={
                'best_days': ['Tuesday', 'Wednesday', 'Thursday'],
                'best_times': ['12:00 PM', '3:00 PM', '8:00 PM'],
                'frequency': 'weekly'
            },
            estimated_engagement=self._estimate_engagement('youtube', content)
        )
    
    def _adapt_instagram(self, content: ContentPiece) -> PlatformContent:
        """Adapt content for Instagram (Reels + Carousel)"""
        
        # Create both Reel and Carousel versions
        reel_hook = self._create_hook(content.main_message, 'instagram_reel')
        
        reel_script = f"""
[0-3 SEC: HOOK]
{reel_hook}

[3-20 SEC: VALUE]
{self._condense_points(content.key_points, max_points=3)}

[20-30 SEC: CTA]
{self._short_cta(content.call_to_action)}
Follow for more tips!
"""
        
        carousel_slides = self._create_carousel_slides(content)
        
        return PlatformContent(
            platform='instagram',
            format_type='reel_and_carousel',
            title=self._create_instagram_caption(content),
            content={
                'reel': reel_script,
                'carousel': carousel_slides
            },
            hashtags=self._generate_hashtags(content.tags, 'instagram', count=30),
            media_specs={
                'reel': {
                    'aspect_ratio': '9:16',
                    'duration': '30 seconds',
                    'resolution': '1080x1920'
                },
                'carousel': {
                    'slides': '6-10',
                    'aspect_ratio': '1:1',
                    'resolution': '1080x1080'
                }
            },
            optimal_timing={
                'best_times': ['11:00 AM', '2:00 PM', '7:00 PM'],
                'frequency': 'daily_reel_3x_carousel'
            },
            estimated_engagement=self._estimate_engagement('instagram', content)
        )
    
    def _adapt_tiktok(self, content: ContentPiece) -> PlatformContent:
        """Adapt content for TikTok"""
        
        hook = self._create_hook(content.main_message, 'tiktok')
        
        script = f"""
[0-3 SEC: HOOK WITH TEXT OVERLAY]
{hook}

[3-25 SEC: FAST-PACED VALUE]
{self._create_tiktok_style(content.key_points)}

[25-30 SEC: QUICK CTA]
Follow for part 2!
{self._trending_hashtag_suggestion()}
"""
        
        return PlatformContent(
            platform='tiktok',
            format_type='trend_adaptation',
            title='',  # TikTok doesn't use titles
            content=script,
            hashtags=self._generate_trending_hashtags('tiktok'),
            media_specs={
                'aspect_ratio': '9:16',
                'duration': '15-30 seconds',
                'resolution': '1080x1920',
                'effects': 'trending_required',
                'audio': 'trending_within_24h'
            },
            optimal_timing={
                'best_times': ['6:00 AM', '10:00 AM', '7:00 PM', '9:00 PM'],
                'frequency': '1-3_daily'
            },
            estimated_engagement=self._estimate_engagement('tiktok', content)
        )
    
    def _adapt_facebook(self, content: ContentPiece) -> PlatformContent:
        """Adapt content for Facebook"""
        
        # Story-based approach for Facebook
        post = f"""
{self._create_relatable_story(content.main_message)}

Here's what I learned:
{chr(10).join(f'→ {point}' for point in content.key_points[:3])}

{content.call_to_action}

What's your experience with this? Let me know below! 👇
"""
        
        return PlatformContent(
            platform='facebook',
            format_type='native_video_with_story',
            title='',
            content=post[:280],  # Keep under character limit
            hashtags=self._generate_hashtags(content.tags, 'facebook', count=5),
            media_specs={
                'video': {
                    'aspect_ratio': '1:1',
                    'duration': '60-90 seconds',
                    'captions': 'required'
                }
            },
            optimal_timing={
                'best_days': ['Tuesday', 'Wednesday', 'Thursday'],
                'best_times': ['1:00 PM', '3:00 PM', '8:00 PM'],
                'frequency': '1-2_daily'
            },
            estimated_engagement=self._estimate_engagement('facebook', content)
        )
    
    def _adapt_twitter(self, content: ContentPiece) -> PlatformContent:
        """Adapt content for Twitter/X"""
        
        # Create thread structure
        thread = []
        
        # Hook tweet
        thread.append(self._create_twitter_hook(content.main_message))
        
        # Point tweets
        for i, point in enumerate(content.key_points[:5], 1):
            thread.append(f"{i}/ {self._condense_for_twitter(point)}")
        
        # Conclusion tweet
        thread.append(f"Key takeaway: {self._short_cta(content.call_to_action)}\n\nRetweet if helpful!")
        
        return PlatformContent(
            platform='twitter',
            format_type='thread',
            title='',
            content=thread,
            hashtags=self._generate_hashtags(content.tags, 'twitter', count=2),
            media_specs={
                'thread_length': f'{len(thread)} tweets',
                'media': 'image_or_gif_recommended'
            },
            optimal_timing={
                'best_times': ['9:00 AM', '12:00 PM', '5:00 PM', '8:00 PM'],
                'frequency': '3-5_daily'
            },
            estimated_engagement=self._estimate_engagement('twitter', content)
        )
    
    def _adapt_linkedin(self, content: ContentPiece) -> PlatformContent:
        """Adapt content for LinkedIn"""
        
        # Professional long-form post
        post = f"""
{self._create_professional_hook(content.main_message)}

After {self._generate_credibility()}, I've discovered that {content.main_message.lower()}.

Here's what I've learned:

{chr(10).join(f'▪️ {self._expand_professionally(point)}' for point in content.key_points)}

{self._add_data_insights(content)}

The bottom line?

{self._professional_conclusion(content.call_to_action)}

What's been your experience with this in your industry? I'd love to hear your thoughts below.

{chr(10).join(f'#{tag}' for tag in self._generate_hashtags(content.tags, 'linkedin', count=5))}
"""
        
        return PlatformContent(
            platform='linkedin',
            format_type='long_form_insight',
            title='',
            content=post,
            hashtags=self._generate_hashtags(content.tags, 'linkedin', count=5),
            media_specs={
                'format': 'text_or_native_video',
                'video_duration': '60-120 seconds'
            },
            optimal_timing={
                'best_days': ['Tuesday', 'Wednesday', 'Thursday'],
                'best_times': ['8:00 AM', '12:00 PM', '5:00 PM'],
                'frequency': '3-5_weekly'
            },
            estimated_engagement=self._estimate_engagement('linkedin', content)
        )
    
    def _adapt_pinterest(self, content: ContentPiece) -> PlatformContent:
        """Adapt content for Pinterest"""
        
        # Create pin description
        pin_title = self._create_pinterest_title(content)
        
        description = f"""
{content.main_message}

{chr(10).join(f'✓ {point}' for point in content.key_points)}

{content.call_to_action}

Save this pin for later reference!
"""
        
        return PlatformContent(
            platform='pinterest',
            format_type='vertical_infographic',
            title=pin_title,
            content=description[:500],  # Pinterest description limit
            hashtags=self._generate_hashtags(content.tags, 'pinterest', count=20),
            media_specs={
                'aspect_ratio': '2:3',
                'dimensions': '1000x1500',
                'text_overlay': 'required',
                'branding': 'watermark'
            },
            optimal_timing={
                'seasonal': '45_days_ahead',
                'best_times': ['2:00 PM', '9:00 PM'],
                'frequency': '5-10_daily'
            },
            estimated_engagement=self._estimate_engagement('pinterest', content)
        )
    
    def _adapt_reddit(self, content: ContentPiece) -> PlatformContent:
        """Adapt content for Reddit"""
        
        # Create detailed guide format
        title = f"[Guide] {content.main_message} - Based on Real Experience"
        
        post = f"""
## Introduction

{self._create_reddit_intro(content.main_message)}

## The Problem

{self._identify_problem(content)}

## The Solution

{chr(10).join(f'### {i+1}. {point}\n{self._expand_reddit_point(point)}\n' 
              for i, point in enumerate(content.key_points))}

## Results

{self._create_results_section(content)}

## TL;DR

{content.main_message}. Key points:
{chr(10).join(f'- {point}' for point in content.key_points[:3])}

## Next Steps

{content.call_to_action}

Feel free to ask questions in the comments. I'll be around to answer!

**Edit:** Thanks for the awards! Added some clarifications based on your questions.
"""
        
        return PlatformContent(
            platform='reddit',
            format_type='detailed_guide',
            title=title,
            content=post,
            hashtags=[],  # Reddit doesn't use hashtags
            media_specs={
                'format': 'text_post',
                'formatting': 'markdown',
                'length': '800-2000_words'
            },
            optimal_timing={
                'best_times': 'subreddit_specific',
                'frequency': 'quality_over_quantity'
            },
            estimated_engagement=self._estimate_engagement('reddit', content)
        )
    
    # Helper methods
    def _create_hook(self, message: str, platform: str) -> str:
        """Create platform-specific hook"""
        hooks = {
            'youtube': f"What if I told you that {message}?",
            'instagram_reel': f"POV: You just discovered {message}",
            'tiktok': f"Nobody talks about how {message}",
            'facebook': f"I just learned something that changed everything: {message}",
            'twitter': f"Unpopular opinion: {message}",
            'linkedin': f"After 10 years in the industry, I can confirm: {message}",
            'pinterest': f"The Secret to {message}",
            'reddit': f"I spent months figuring out {message}. Here's what worked:"
        }
        return hooks.get(platform, message)
    
    def _generate_hashtags(self, tags: List[str], platform: str, count: int = 10) -> List[str]:
        """Generate platform-optimized hashtags"""
        
        # Platform-specific hashtag strategies
        if platform == 'instagram':
            # Mix of broad, niche, and branded
            return self._mix_hashtag_types(tags, count)
        elif platform == 'tiktok':
            # Trending hashtags preferred
            return self._get_trending_tags(platform)[:count]
        elif platform == 'twitter':
            # Minimal hashtags (1-2)
            return tags[:2]
        elif platform == 'linkedin':
            # Professional, industry-specific
            return [f"{tag.lower().replace(' ', '')}" for tag in tags[:5]]
        elif platform == 'pinterest':
            # SEO-optimized keywords
            return self._generate_seo_tags(tags, count)
        else:
            return tags[:count]
    
    def _estimate_engagement(self, platform: str, content: ContentPiece) -> float:
        """Estimate engagement rate based on content quality and platform"""
        
        base_rates = {
            'youtube': 0.08,
            'instagram': 0.15,
            'tiktok': 0.20,
            'facebook': 0.06,
            'twitter': 0.12,
            'linkedin': 0.08,
            'pinterest': 0.05,
            'reddit': 0.10
        }
        
        # Adjust based on content quality factors
        quality_multiplier = 1.0
        
        # Educational content bonus
        if 'educational' in content.brand_voice:
            quality_multiplier *= 1.3
        
        # Trending topic bonus
        if self._is_trending_topic(content.main_message):
            quality_multiplier *= 1.5
        
        # Visual content bonus
        if content.media_assets:
            quality_multiplier *= 1.2
        
        estimated_rate = base_rates.get(platform, 0.05) * quality_multiplier
        
        return min(estimated_rate, 0.30)  # Cap at 30% engagement
    
    def _condense_points(self, points: List[str], max_points: int = 3) -> str:
        """Condense key points for short-form content"""
        condensed = points[:max_points]
        return chr(10).join(f"💡 {point[:50]}..." if len(point) > 50 else f"💡 {point}" 
                           for point in condensed)
    
    def _short_cta(self, cta: str) -> str:
        """Shorten call-to-action for platforms with character limits"""
        if len(cta) > 30:
            return cta[:27] + "..."
        return cta
    
    def _create_carousel_slides(self, content: ContentPiece) -> List[Dict[str, str]]:
        """Create Instagram carousel slide structure"""
        slides = []
        
        # Cover slide
        slides.append({
            'type': 'cover',
            'title': content.main_message,
            'subtitle': 'Swipe for insights →'
        })
        
        # Point slides
        for i, point in enumerate(content.key_points[:8], 1):
            slides.append({
                'type': 'point',
                'number': str(i),
                'content': point,
                'visual': 'icon_or_illustration'
            })
        
        # CTA slide
        slides.append({
            'type': 'cta',
            'content': content.call_to_action,
            'prompt': 'Save & Share if helpful!'
        })
        
        return slides
    
    def _create_instagram_caption(self, content: ContentPiece) -> str:
        """Create Instagram caption with hook"""
        return f"{content.main_message} 👇\n\n[Continue reading...]"
    
    def _create_tiktok_style(self, points: List[str]) -> str:
        """Create TikTok-style fast-paced content"""
        return chr(10).join(f"Wait for it... {point[:30]}" for point in points[:3])
    
    def _trending_hashtag_suggestion(self) -> str:
        """Suggest trending hashtag usage"""
        return "#fyp #trending #viral"
    
    def _get_trending_tags(self, platform: str) -> List[str]:
        """Get current trending hashtags (would connect to real API)"""
        # Placeholder - would connect to trend detection API
        return ['fyp', 'viral', 'trending', 'foryoupage', 'trend']
    
    def _create_relatable_story(self, message: str) -> str:
        """Create relatable story opening for Facebook"""
        return f"Yesterday something happened that made me realize {message.lower()}..."
    
    def _create_twitter_hook(self, message: str) -> str:
        """Create Twitter thread hook"""
        return f"🧵 {message} (a thread)"
    
    def _condense_for_twitter(self, text: str) -> str:
        """Condense text for Twitter character limit"""
        if len(text) > 240:
            return text[:237] + "..."
        return text
    
    def _create_professional_hook(self, message: str) -> str:
        """Create LinkedIn professional hook"""
        return f"💡 {message}?"
    
    def _generate_credibility(self) -> str:
        """Generate credibility statement for LinkedIn"""
        return "15 years working with Fortune 500 companies"
    
    def _expand_professionally(self, point: str) -> str:
        """Expand point with professional context"""
        return f"{point} - This has significant implications for business growth and team productivity."
    
    def _add_data_insights(self, content: ContentPiece) -> str:
        """Add data-driven insights for LinkedIn"""
        return "According to recent industry research, companies implementing these strategies see a 47% improvement in key metrics."
    
    def _professional_conclusion(self, cta: str) -> str:
        """Create professional conclusion for LinkedIn"""
        return f"{cta}\n\nThis approach has transformed how leading companies operate in 2024."
    
    def _create_youtube_title(self, content: ContentPiece) -> str:
        """Create YouTube-optimized title"""
        return f"{content.title} (PROVEN STRATEGIES)"
    
    def _create_pinterest_title(self, content: ContentPiece) -> str:
        """Create SEO-optimized Pinterest title"""
        return f"{content.main_message} | Ultimate Guide for 2024"
    
    def _expand_content(self, content: ContentPiece, style: str) -> str:
        """Expand content based on style"""
        if style == 'detailed':
            expanded = f"{content.main_message}\n\nKey Points:\n"
            for point in content.key_points:
                expanded += f"- {point}: [Detailed explanation]\n"
            return expanded
        return content.main_message
    
    def _create_relatable_story(self, message: str) -> str:
        """Create relatable story for engagement"""
        return f"Yesterday I discovered something amazing: {message}"
    
    def _create_results_section(self, content: ContentPiece) -> str:
        """Create results section"""
        return f"Implementing {content.main_message} led to incredible results."
    
    def _is_trending_topic(self, message: str) -> bool:
        """Check if topic is trending"""
        trending = ['ai', 'automation', 'growth', 'viral']
        return any(t in message.lower() for t in trending)
    
    def _get_trending_tags(self, platform: str) -> List[str]:
        """Get trending tags for platform"""
        tags = {
            'tiktok': ['fyp', 'viral', 'trending', 'foryou'],
            'instagram': ['instagood', 'photooftheday', 'love', 'beautiful']
        }
        return tags.get(platform, [])
    
    def _generate_trending_hashtags(self, platform: str) -> List[str]:
        """Generate trending hashtags for platform"""
        return self._get_trending_tags(platform)
    
    def _create_tiktok_style(self, points: List[str]) -> str:
        """Create TikTok-style content"""
        return " → ".join(points[:3])
    
    def _trending_hashtag_suggestion(self) -> str:
        """Suggest trending hashtags"""
        return "#fyp #viral #trending"
    
    def _create_twitter_hook(self, message: str) -> str:
        """Create Twitter hook"""
        return f"🧵 {message} (thread)"
    
    def _condense_for_twitter(self, text: str) -> str:
        """Condense for Twitter"""
        return text[:240] if len(text) > 240 else text
    
    def _create_professional_hook(self, message: str) -> str:
        """Create LinkedIn hook"""
        return f"💡 {message}"
    
    def _generate_credibility(self) -> str:
        """Generate credibility statement"""
        return "Based on 10+ years of experience"
    
    def _expand_professionally(self, point: str) -> str:
        """Expand point professionally"""
        return f"{point} - with significant business impact"
    
    def _add_data_insights(self, content: ContentPiece) -> str:
        """Add data insights"""
        return "Studies show 47% improvement in key metrics"
    
    def _professional_conclusion(self, cta: str) -> str:
        """Professional conclusion"""
        return f"{cta} - Transform your business today"
    
    def _create_reddit_intro(self, message: str) -> str:
        """Create Reddit-style introduction"""
        return f"Hey everyone! After countless hours of research and testing, I've finally cracked {message.lower()}. I wanted to share what I've learned with the community."
    
    def _expand_reddit_point(self, point: str) -> str:
        """Expand Reddit point"""
        return f"{point}\n\nDetailed implementation: [step-by-step guide here]"
    
    def _create_instagram_caption(self, content: ContentPiece) -> str:
        """Create Instagram caption"""
        return f"{content.main_message} 💫\n\nSwipe for more! ✨"
    
    def _create_carousel_slides(self, content: ContentPiece) -> List[Dict]:
        """Create carousel slides"""
        slides = [{"type": "cover", "content": content.title}]
        for point in content.key_points[:5]:
            slides.append({"type": "point", "content": point})
        return slides
    
    def _mix_hashtag_types(self, tags: List[str], count: int) -> List[str]:
        """Mix hashtag types"""
        return tags[:count]
    
    def _generate_seo_tags(self, tags: List[str], count: int) -> List[str]:
        """Generate SEO tags"""
        return [f"{tag}2024" for tag in tags[:count]]
    
    def _identify_problem(self, content: ContentPiece) -> str:
        """Identify problem for Reddit post"""
        return f"Like many of you, I struggled with {content.main_message.lower()}. The existing solutions were either too complex, too expensive, or simply didn't work."
    
    def _expand_reddit_point(self, point: str) -> str:
        """Expand point with Reddit-style detail"""
        return f"{point}\n\nHere's exactly how to implement this: [detailed explanation would go here with specific steps, tools, and examples]"
    
    def _create_results_section(self, content: ContentPiece) -> str:
        """Create results section for Reddit"""
        return "After implementing these strategies, I saw a 3x improvement in results within 30 days. Your mileage may vary, but the principles are solid."
    
    def _mix_hashtag_types(self, tags: List[str], count: int) -> List[str]:
        """Mix broad, niche, and branded hashtags for Instagram"""
        broad = ['marketing', 'business', 'entrepreneur']
        niche = tags
        branded = ['yourbrand', 'brandname2024']
        
        mixed = broad[:5] + niche[:15] + branded[:5]
        return mixed[:count]
    
    def _generate_seo_tags(self, tags: List[str], count: int) -> List[str]:
        """Generate SEO-optimized tags for Pinterest"""
        seo_enhanced = []
        for tag in tags:
            seo_enhanced.append(tag.lower().replace(' ', ''))
            seo_enhanced.append(f"{tag.lower().replace(' ', '')}2024")
            seo_enhanced.append(f"{tag.lower().replace(' ', '')}ideas")
        return seo_enhanced[:count]
    
    def _is_trending_topic(self, message: str) -> bool:
        """Check if topic is currently trending (placeholder)"""
        trending_keywords = ['ai', 'sustainability', 'remote work', 'automation']
        return any(keyword in message.lower() for keyword in trending_keywords)

    def batch_process_content(self, content_list: List[ContentPiece]) -> List[Dict[str, PlatformContent]]:
        """
        Process multiple content pieces with CPU optimization
        """
        results = []
        
        # Process in batches with throttling
        batch_size = self.throttler.max_concurrent
        
        for i in range(0, len(content_list), batch_size):
            batch = content_list[i:i + batch_size]
            
            # Wait for CPU before batch
            self.cpu_manager.wait_for_cpu()
            
            for content in batch:
                adapted = self.adapt_content(content)
                results.append(adapted)
                
                # Adaptive sleep between items
                self.cpu_manager.adaptive_sleep(1.0)
            
            print(f"Processed batch {i//batch_size + 1}/{(len(content_list) + batch_size - 1)//batch_size}")
        
        return results

    def generate_posting_schedule(self, adapted_content: Dict[str, PlatformContent]) -> Dict[str, List[Dict]]:
        """
        Generate optimal posting schedule for all platforms
        """
        schedule = {}
        
        for platform, content in adapted_content.items():
            platform_schedule = []
            
            # Get optimal timing from content
            timing = content.optimal_timing
            
            # Generate schedule for next 7 days
            for day in range(7):
                for time in timing.get('best_times', ['12:00 PM']):
                    platform_schedule.append({
                        'day': day,
                        'time': time,
                        'content_type': content.format_type,
                        'estimated_engagement': content.estimated_engagement
                    })
            
            schedule[platform] = platform_schedule
        
        return schedule


def main():
    """Test the content adapter"""
    
    # Initialize adapter
    adapter = PlatformContentAdapter()
    
    # Create sample content
    sample_content = ContentPiece(
        title="5 Marketing Strategies That Actually Work",
        main_message="Modern marketing requires authentic connection, not just promotion",
        key_points=[
            "Focus on educational content over promotional",
            "Build genuine community engagement",
            "Use data-driven decision making",
            "Leverage user-generated content",
            "Implement consistent brand storytelling"
        ],
        call_to_action="Start implementing these strategies today for better results",
        tags=["marketing", "business", "growth", "strategy", "digital"],
        brand_voice="professional yet approachable",
        target_audience="small business owners"
    )
    
    print("Adapting content for all platforms...")
    print("=" * 60)
    
    # Adapt content with CPU protection
    adapted = adapter.adapt_content(sample_content)
    
    # Display results
    for platform, content in adapted.items():
        print(f"\n{platform.upper()} Adaptation:")
        print("-" * 40)
        print(f"Format: {content.format_type}")
        print(f"Estimated Engagement: {content.estimated_engagement:.1%}")
        print(f"Optimal Times: {content.optimal_timing.get('best_times', 'N/A')}")
        
        if isinstance(content.content, str):
            preview = content.content[:200] + "..." if len(content.content) > 200 else content.content
            print(f"Content Preview: {preview}")
        elif isinstance(content.content, list):
            print(f"Thread/Slides: {len(content.content)} parts")
        elif isinstance(content.content, dict):
            print(f"Multiple Formats: {list(content.content.keys())}")
        
        print(f"Hashtags: {', '.join(content.hashtags[:5])}...")
    
    print("\n" + "=" * 60)
    print("Content adaptation complete!")
    
    # Generate posting schedule
    schedule = adapter.generate_posting_schedule(adapted)
    print("\nOptimal Posting Schedule Generated:")
    for platform, times in schedule.items():
        print(f"  {platform}: {len(times)} posts scheduled over 7 days")


if __name__ == "__main__":
    main()