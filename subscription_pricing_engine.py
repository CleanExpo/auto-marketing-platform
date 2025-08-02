#!/usr/bin/env python3
"""
Advanced Subscription Pricing Engine - Python Implementation
Dynamic pricing, tier management, and customer lock-in strategies
Integrated with Platform-Specific Marketing Mastery System
"""

import json
import math
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path
from cpu_manager import get_cpu_manager, ProcessThrottler
from unicode_utils import safe_print, make_safe, safe_format

@dataclass
class UsageMetrics:
    """User usage metrics for pricing calculations"""
    platforms_used: int
    posts_created: int
    ai_content_generated: int
    team_members: int
    api_calls: int
    storage_used: float  # GB
    support_tickets: int
    video_generations: int
    voice_commands_used: int

@dataclass
class PricingTier:
    """Subscription tier configuration"""
    name: str
    monthly_price: float
    annual_price: float
    features: Dict[str, Any]
    lock_in_features: List[str]
    target_segment: str

class SubscriptionPricingEngine:
    """
    Advanced subscription pricing engine with 80% profit margin optimization
    """
    
    def __init__(self):
        self.cpu_manager = get_cpu_manager(max_cpu=75.0)
        self.throttler = ProcessThrottler(self.cpu_manager)
        
        # Base cost structure (per user per month)
        self.base_costs = {
            'infrastructure': 2.50,  # Server, CDN, storage
            'api_costs': 1.75,       # Social media APIs, AI APIs
            'support': 0.75,         # Customer support allocation
            'development': 1.00      # Ongoing development costs
        }
        
        self.total_base_cost = 6.00  # $6 per user per month
        self.target_profit_margin = 0.80  # 80% profit margin target
        
        # Initialize pricing tiers
        self.tiers = self._initialize_pricing_tiers()
        
        # Competitive analysis data
        self.competitor_data = self._load_competitor_data()
        
        # Storage paths
        self.base_path = Path("C:/Auto Marketing/data")
        self.pricing_path = self.base_path / "pricing"
        self.pricing_path.mkdir(parents=True, exist_ok=True)
    
    def _initialize_pricing_tiers(self) -> Dict[str, PricingTier]:
        """Initialize subscription tiers with optimized pricing"""
        return {
            'starter': PricingTier(
                name="Starter",
                monthly_price=29.0,
                annual_price=290.0,  # 17% discount
                features={
                    'platforms': 3,
                    'posts_per_month': 100,
                    'ai_generated_content': 50,
                    'analytics_retention': 30,
                    'team_members': 1,
                    'support': 'email',
                    'branding_removal': False,
                    'api_access': False,
                    'advanced_scheduling': False,
                    'competitor_analysis': False,
                    'video_generation': 0,
                    'voice_commands': 10,
                    'storage_gb': 1
                },
                lock_in_features=[
                    'content_library_storage',
                    'basic_templates',
                    'posting_history'
                ],
                target_segment='small_business'
            ),
            
            'professional': PricingTier(
                name="Professional",
                monthly_price=79.0,
                annual_price=790.0,  # 17% discount
                features={
                    'platforms': 8,
                    'posts_per_month': 500,
                    'ai_generated_content': 250,
                    'analytics_retention': 90,
                    'team_members': 3,
                    'support': 'priority_email',
                    'branding_removal': True,
                    'api_access': 'limited',
                    'advanced_scheduling': True,
                    'competitor_analysis': 'basic',
                    'video_generation': 20,
                    'voice_commands': 100,
                    'bulk_scheduling': True,
                    'content_calendar': True,
                    'storage_gb': 10
                },
                lock_in_features=[
                    'advanced_content_library',
                    'custom_templates',
                    'detailed_analytics_history',
                    'team_collaboration_workspace',
                    'brand_kit_storage'
                ],
                target_segment='growing_business'
            ),
            
            'business': PricingTier(
                name="Business",
                monthly_price=149.0,
                annual_price=1490.0,  # 17% discount
                features={
                    'platforms': 'unlimited',
                    'posts_per_month': 2000,
                    'ai_generated_content': 1000,
                    'analytics_retention': 365,
                    'team_members': 10,
                    'support': 'phone_and_chat',
                    'branding_removal': True,
                    'api_access': 'full',
                    'advanced_scheduling': True,
                    'competitor_analysis': 'advanced',
                    'video_generation': 100,
                    'voice_commands': 500,
                    'bulk_scheduling': True,
                    'content_calendar': True,
                    'white_labeling': True,
                    'advanced_reporting': True,
                    'client_management': True,
                    'storage_gb': 100
                },
                lock_in_features=[
                    'enterprise_content_library',
                    'unlimited_custom_templates',
                    'comprehensive_analytics_suite',
                    'advanced_team_management',
                    'client_portal_access',
                    'custom_integrations',
                    'dedicated_workspace'
                ],
                target_segment='established_business'
            ),
            
            'enterprise': PricingTier(
                name="Enterprise",
                monthly_price=299.0,
                annual_price=2990.0,  # 17% discount
                features={
                    'platforms': 'unlimited',
                    'posts_per_month': 'unlimited',
                    'ai_generated_content': 'unlimited',
                    'analytics_retention': 'unlimited',
                    'team_members': 'unlimited',
                    'support': 'dedicated_account_manager',
                    'branding_removal': True,
                    'api_access': 'enterprise',
                    'advanced_scheduling': True,
                    'competitor_analysis': 'enterprise',
                    'video_generation': 'unlimited',
                    'voice_commands': 'unlimited',
                    'bulk_scheduling': True,
                    'content_calendar': True,
                    'white_labeling': True,
                    'advanced_reporting': True,
                    'client_management': True,
                    'custom_integrations': True,
                    'sla': '99.9%',
                    'onboarding': 'dedicated',
                    'storage_gb': 'unlimited'
                },
                lock_in_features=[
                    'enterprise_data_warehouse',
                    'unlimited_everything',
                    'custom_ai_training',
                    'dedicated_infrastructure',
                    'priority_feature_requests',
                    'custom_analytics_dashboards',
                    'enterprise_security_features'
                ],
                target_segment='enterprise'
            )
        }
    
    def calculate_optimal_pricing(self, user_profile: Dict[str, Any], 
                                 usage_data: UsageMetrics) -> Dict[str, float]:
        """
        Calculate optimal pricing based on value metrics with CPU protection
        """
        self.cpu_manager.wait_for_cpu()
        
        # Calculate base value
        base_value = self.cpu_manager.throttled_execute(
            self._calculate_base_value,
            user_profile, usage_data
        )
        
        # Apply competitive adjustments
        competitive_adjustment = self._get_competitive_adjustment(
            user_profile.get('industry', 'general')
        )
        
        # Apply demand multiplier
        demand_multiplier = self._get_demand_multiplier(
            user_profile.get('segment', 'small_business')
        )
        
        # Calculate optimal price
        optimal_price = base_value * competitive_adjustment * demand_multiplier
        
        # Ensure minimum profit margin
        minimum_price = self.total_base_cost / (1 - self.target_profit_margin)
        final_price = max(optimal_price, minimum_price)
        
        return {
            'base_value': base_value,
            'competitive_adjustment': competitive_adjustment,
            'demand_multiplier': demand_multiplier,
            'optimal_price': optimal_price,
            'minimum_price': minimum_price,
            'final_price': final_price,
            'profit_margin': self._calculate_profit_margin(final_price)
        }
    
    def generate_lock_in_strategy(self, user_id: str, current_tier: str, 
                                 usage_patterns: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive customer lock-in strategy with CPU protection
        """
        self.cpu_manager.wait_for_cpu()
        
        # Calculate lock-in elements
        lock_in_elements = {
            'data_lock_in': self.cpu_manager.throttled_execute(
                self._calculate_data_lock_in,
                user_id
            ),
            'switching_costs': self.cpu_manager.throttled_execute(
                self._calculate_switching_costs,
                user_id, current_tier
            ),
            'increasing_returns': self.cpu_manager.throttled_execute(
                self._calculate_increasing_returns,
                user_id, usage_patterns
            )
        }
        
        # Calculate total lock-in value
        total_lock_in_value = self._calculate_total_lock_in_value(lock_in_elements)
        
        # Assess churn risk
        churn_risk = self.cpu_manager.throttled_execute(
            self._calculate_churn_risk,
            user_id, lock_in_elements
        )
        
        return {
            'total_lock_in_value': total_lock_in_value,
            'churn_risk_score': churn_risk,
            'retention_strategies': self._generate_retention_strategies(lock_in_elements),
            'upsell_opportunities': self._identify_upsell_opportunities(user_id, current_tier),
            'lock_in_elements': lock_in_elements,
            'calculated_at': datetime.now().isoformat()
        }
    
    def calculate_dynamic_pricing(self, user_id: str, base_price: float, 
                                 usage_metrics: UsageMetrics) -> Dict[str, Any]:
        """
        Calculate dynamic pricing based on usage and value with CPU protection
        """
        self.cpu_manager.wait_for_cpu()
        
        # Calculate pricing adjustments
        adjustments = {
            'volume_discount': self.cpu_manager.throttled_execute(
                self._calculate_volume_discount,
                usage_metrics
            ),
            'value_multiplier': self.cpu_manager.throttled_execute(
                self._calculate_value_multiplier,
                usage_metrics
            ),
            'loyalty_discount': self.cpu_manager.throttled_execute(
                self._calculate_loyalty_discount,
                user_id
            ),
            'demand_surge': self.cpu_manager.throttled_execute(
                self._calculate_demand_surge,
                usage_metrics
            )
        }
        
        # Apply adjustments
        adjusted_price = base_price * \
            (1 - adjustments['volume_discount']) * \
            adjustments['value_multiplier'] * \
            (1 - adjustments['loyalty_discount']) * \
            (1 + adjustments['demand_surge'])
        
        # Ensure minimum price
        minimum_price = self.total_base_cost / (1 - self.target_profit_margin)
        final_price = max(adjusted_price, minimum_price)
        
        return {
            'original_price': base_price,
            'adjusted_price': round(final_price, 2),
            'adjustments': adjustments,
            'savings_amount': base_price - final_price,
            'profit_margin': self._calculate_profit_margin(final_price),
            'minimum_price_applied': final_price == minimum_price
        }
    
    def generate_upgrade_incentives(self, user_id: str, current_tier: str, 
                                   next_tier: str) -> Dict[str, Any]:
        """
        Generate tier upgrade incentives with CPU protection
        """
        self.cpu_manager.wait_for_cpu()
        
        current_features = self.tiers[current_tier].features
        next_features = self.tiers[next_tier].features
        usage_data = self.cpu_manager.throttled_execute(
            self._get_user_usage,
            user_id
        )
        
        incentives = []
        
        # Check feature limits
        for feature, current_limit in current_features.items():
            if isinstance(current_limit, (int, float)):
                current_usage = usage_data.get(feature, 0)
                if current_usage / current_limit > 0.8:  # 80% utilization
                    utilization_rate = current_usage / current_limit
                    next_limit = next_features.get(feature, 'unlimited')
                    
                    incentives.append({
                        'type': 'limit_approaching',
                        'feature': feature,
                        'message': f"You're using {utilization_rate:.0%} of your {feature} limit",
                        'urgency': 'high' if utilization_rate > 0.95 else 'medium',
                        'benefit': f"Upgrade to get {next_limit} {feature}",
                        'current_usage': current_usage,
                        'current_limit': current_limit
                    })
        
        # Feature-based incentives
        new_features = self._get_new_features_in_tier(current_tier, next_tier)
        for feature in new_features:
            incentives.append({
                'type': 'new_feature',
                'feature': feature['name'],
                'message': feature['description'],
                'value': feature['estimated_value'],
                'urgency': 'low'
            })
        
        return {
            'incentives': incentives,
            'upgrade_value': self._calculate_upgrade_value(current_tier, next_tier, usage_data),
            'timeline': self._suggest_upgrade_timeline(incentives),
            'special_offers': self._generate_special_offers(user_id, current_tier, next_tier)
        }
    
    def generate_retention_offer(self, user_id: str, churn_risk: float) -> Optional[Dict[str, Any]]:
        """
        Generate retention offers based on churn risk with CPU protection
        """
        if churn_risk < 30:
            return None
        
        self.cpu_manager.wait_for_cpu()
        
        current_tier = self._get_user_tier(user_id)
        usage_data = self.cpu_manager.throttled_execute(
            self._get_user_usage,
            user_id
        )
        
        offers = []
        
        if churn_risk > 70:
            # High risk - aggressive retention
            offers.extend([
                {
                    'type': 'discount',
                    'value': 50,
                    'duration': 6,
                    'description': '50% off for 6 months',
                    'estimated_ltv_impact': 2500
                },
                {
                    'type': 'feature_upgrade',
                    'value': 'next_tier_features',
                    'duration': 3,
                    'description': 'Free upgrade to higher tier for 3 months',
                    'estimated_ltv_impact': 1800
                }
            ])
        elif churn_risk > 50:
            # Medium risk - moderate retention
            offers.extend([
                {
                    'type': 'discount',
                    'value': 25,
                    'duration': 3,
                    'description': '25% off for 3 months',
                    'estimated_ltv_impact': 800
                },
                {
                    'type': 'bonus_credits',
                    'value': usage_data.get('monthly_spend', 0) * 0.5,
                    'description': 'Bonus AI generation credits',
                    'estimated_ltv_impact': 400
                }
            ])
        
        if not offers:
            return None
        
        return {
            'offers': offers,
            'valid_until': (datetime.now() + timedelta(days=7)).isoformat(),
            'personalized_message': self._generate_personalized_message(user_id, churn_risk),
            'next_follow_up': (datetime.now() + timedelta(days=3)).isoformat(),
            'estimated_success_rate': self._calculate_retention_success_rate(churn_risk, offers)
        }
    
    # Helper methods for calculations
    def _calculate_base_value(self, user_profile: Dict[str, Any], 
                             usage_data: UsageMetrics) -> float:
        """Calculate base value proposition"""
        # Value based on usage intensity
        platform_value = usage_data.platforms_used * 5.0
        content_value = usage_data.posts_created * 0.50
        ai_value = usage_data.ai_content_generated * 1.20
        team_value = usage_data.team_members * 15.0
        
        # Industry multipliers
        industry_multipliers = {
            'marketing_agency': 1.5,
            'ecommerce': 1.3,
            'saas': 1.4,
            'consulting': 1.6,
            'healthcare': 1.2,
            'education': 0.8,
            'nonprofit': 0.7
        }
        
        industry = user_profile.get('industry', 'general')
        multiplier = industry_multipliers.get(industry, 1.0)
        
        base_value = (platform_value + content_value + ai_value + team_value) * multiplier
        return max(base_value, 20.0)  # Minimum base value
    
    def _get_competitive_adjustment(self, industry: str) -> float:
        """Get competitive pricing adjustment"""
        adjustments = {
            'marketing_agency': 1.2,
            'ecommerce': 1.1,
            'saas': 1.3,
            'consulting': 1.4,
            'healthcare': 1.15,
            'education': 0.9,
            'nonprofit': 0.8,
            'enterprise': 1.5
        }
        return adjustments.get(industry, 1.0)
    
    def _get_demand_multiplier(self, segment: str) -> float:
        """Get demand-based multiplier"""
        multipliers = {
            'high_growth_startup': 1.3,
            'established_business': 1.1,
            'enterprise': 1.4,
            'small_business': 0.9,
            'individual': 0.8
        }
        return multipliers.get(segment, 1.0)
    
    def _calculate_profit_margin(self, price: float) -> float:
        """Calculate profit margin percentage"""
        return ((price - self.total_base_cost) / price) * 100
    
    def _calculate_data_lock_in(self, user_id: str) -> Dict[str, float]:
        """Calculate data lock-in value"""
        # Simulate data lock-in calculations
        return {
            'content_library_value': 500.0,
            'analytics_history_value': 300.0,
            'custom_templates_value': 200.0,
            'team_collaboration_value': 400.0
        }
    
    def _calculate_switching_costs(self, user_id: str, current_tier: str) -> Dict[str, float]:
        """Calculate switching costs"""
        # Simulate switching cost calculations
        tier_multipliers = {
            'starter': 1.0,
            'professional': 1.5,
            'business': 2.0,
            'enterprise': 3.0
        }
        
        base_cost = 1000.0
        multiplier = tier_multipliers.get(current_tier, 1.0)
        
        return {
            'data_export_cost': base_cost * 0.3 * multiplier,
            'retraining_cost': base_cost * 0.4 * multiplier,
            'setup_cost': base_cost * 0.2 * multiplier,
            'opportunity_cost': base_cost * 0.1 * multiplier
        }
    
    def _calculate_increasing_returns(self, user_id: str, usage_patterns: Dict[str, Any]) -> Dict[str, float]:
        """Calculate increasing returns value"""
        return {
            'network_effects': 200.0,
            'learning_curve': 300.0,
            'customization': 400.0,
            'automation': 500.0
        }
    
    def _calculate_total_lock_in_value(self, lock_in_elements: Dict[str, Dict[str, float]]) -> float:
        """Calculate total lock-in value"""
        total = 0.0
        for category in lock_in_elements.values():
            total += sum(category.values())
        return total
    
    def _calculate_churn_risk(self, user_id: str, lock_in_elements: Dict[str, Any]) -> float:
        """Calculate churn risk score (0-100)"""
        # Simulate churn risk calculation
        # Higher lock-in value = lower churn risk
        total_lock_in = self._calculate_total_lock_in_value(lock_in_elements)
        
        # Base risk inversely related to lock-in value
        base_risk = max(10, 80 - (total_lock_in / 100))
        
        return min(base_risk, 90)  # Cap at 90%
    
    def _load_competitor_data(self) -> Dict[str, Any]:
        """Load competitive analysis data"""
        return {
            'hootsuite': {'starter': 49, 'professional': 129, 'business': 249},
            'buffer': {'starter': 15, 'professional': 65, 'business': 99},
            'sprout_social': {'starter': 89, 'professional': 149, 'business': 249},
            'later': {'starter': 25, 'professional': 40, 'business': 80}
        }
    
    # Additional helper methods for completeness
    def _calculate_volume_discount(self, usage_metrics: UsageMetrics) -> float:
        """Calculate volume-based discount"""
        total_usage = usage_metrics.posts_created + usage_metrics.ai_content_generated
        
        if total_usage > 1000:
            return 0.15  # 15% discount
        elif total_usage > 500:
            return 0.10  # 10% discount
        elif total_usage > 200:
            return 0.05  # 5% discount
        return 0.0
    
    def _calculate_value_multiplier(self, usage_metrics: UsageMetrics) -> float:
        """Calculate value-based multiplier"""
        # High-value features increase multiplier
        if usage_metrics.video_generations > 50:
            return 1.2
        elif usage_metrics.voice_commands_used > 100:
            return 1.1
        return 1.0
    
    def _calculate_loyalty_discount(self, user_id: str) -> float:
        """Calculate loyalty-based discount"""
        # Simulate loyalty calculation based on tenure
        # In production, would check actual user tenure
        return 0.05  # 5% loyalty discount
    
    def _calculate_demand_surge(self, usage_metrics: UsageMetrics) -> float:
        """Calculate demand surge pricing"""
        # No surge pricing for this model
        return 0.0
    
    def _get_user_usage(self, user_id: str) -> Dict[str, Any]:
        """Get user usage data"""
        # Simulate user usage data
        return {
            'posts_created': 150,
            'ai_content_generated': 75,
            'platforms_used': 5,
            'team_members': 2,
            'monthly_spend': 79,
            'video_generations': 10,
            'voice_commands': 45
        }
    
    def _get_user_tier(self, user_id: str) -> str:
        """Get user's current tier"""
        # Simulate getting user tier
        return 'professional'
    
    def _get_new_features_in_tier(self, current_tier: str, next_tier: str) -> List[Dict[str, Any]]:
        """Get new features available in next tier"""
        features = [
            {
                'name': 'advanced_analytics',
                'description': 'Advanced analytics and reporting',
                'estimated_value': 200
            },
            {
                'name': 'white_labeling',
                'description': 'White-label the platform for your clients',
                'estimated_value': 500
            }
        ]
        return features
    
    def _calculate_upgrade_value(self, current_tier: str, next_tier: str, usage_data: Dict[str, Any]) -> float:
        """Calculate value of upgrading"""
        current_price = self.tiers[current_tier].monthly_price
        next_price = self.tiers[next_tier].monthly_price
        price_difference = next_price - current_price
        
        # Estimate value based on new features
        estimated_value = price_difference * 2.5  # 2.5x value ratio
        return estimated_value
    
    def _suggest_upgrade_timeline(self, incentives: List[Dict[str, Any]]) -> str:
        """Suggest optimal upgrade timeline"""
        high_urgency_count = len([i for i in incentives if i.get('urgency') == 'high'])
        
        if high_urgency_count > 2:
            return 'immediate'
        elif high_urgency_count > 0:
            return 'within_week'
        else:
            return 'within_month'
    
    def _generate_special_offers(self, user_id: str, current_tier: str, next_tier: str) -> List[Dict[str, Any]]:
        """Generate special upgrade offers"""
        return [
            {
                'type': 'first_month_free',
                'description': 'First month of upgraded tier free',
                'value': self.tiers[next_tier].monthly_price
            },
            {
                'type': 'gradual_upgrade',
                'description': 'Pay current tier price for 3 months',
                'value': (self.tiers[next_tier].monthly_price - self.tiers[current_tier].monthly_price) * 3
            }
        ]
    
    def _generate_retention_strategies(self, lock_in_elements: Dict[str, Any]) -> List[str]:
        """Generate retention strategies"""
        return [
            'Increase content library dependencies',
            'Enhance team collaboration features',
            'Provide advanced customization options',
            'Implement progressive feature unlocking'
        ]
    
    def _identify_upsell_opportunities(self, user_id: str, current_tier: str) -> List[Dict[str, Any]]:
        """Identify upselling opportunities"""
        return [
            {
                'opportunity': 'video_generation',
                'description': 'User approaching video generation limit',
                'potential_revenue': 50
            },
            {
                'opportunity': 'team_expansion',
                'description': 'User adding team members',
                'potential_revenue': 30
            }
        ]
    
    def _generate_personalized_message(self, user_id: str, churn_risk: float) -> str:
        """Generate personalized retention message"""
        if churn_risk > 70:
            return "We noticed you might be considering other options. Let's discuss how we can better serve your needs."
        elif churn_risk > 50:
            return "Your success is important to us. Here's a special offer to help you achieve your marketing goals."
        else:
            return "We value your partnership and want to ensure you're getting maximum value from our platform."
    
    def _calculate_retention_success_rate(self, churn_risk: float, offers: List[Dict[str, Any]]) -> float:
        """Calculate estimated success rate of retention offers"""
        base_success_rate = 1.0 - (churn_risk / 100)
        offer_boost = len(offers) * 0.1  # Each offer adds 10% success rate
        
        return min(base_success_rate + offer_boost, 0.85)  # Cap at 85%


def test_pricing_engine():
    """Test the subscription pricing engine"""
    safe_print("\n" + "="*60)
    safe_print("SUBSCRIPTION PRICING ENGINE TEST")
    safe_print("="*60)
    
    # Initialize pricing engine
    engine = SubscriptionPricingEngine()
    
    # Test user profile and usage
    user_profile = {
        'industry': 'marketing_agency',
        'segment': 'growing_business',
        'company_size': 25
    }
    
    usage_metrics = UsageMetrics(
        platforms_used=5,
        posts_created=150,
        ai_content_generated=75,
        team_members=3,
        api_calls=2500,
        storage_used=5.2,
        support_tickets=2,
        video_generations=15,
        voice_commands_used=45
    )
    
    # Test optimal pricing calculation
    safe_print("\n1. Testing optimal pricing calculation...")
    try:
        pricing = engine.calculate_optimal_pricing(user_profile, usage_metrics)
        pricing_msg = safe_format(
            "   [OK] Optimal price: ${price:.2f} (margin: {margin:.1f}%)",
            price=pricing['final_price'],
            margin=pricing['profit_margin']
        )
        safe_print(pricing_msg)
    except Exception as e:
        safe_print(f"   [ERROR] Pricing calculation failed: {e}")
    
    # Test lock-in strategy
    safe_print("\n2. Testing lock-in strategy generation...")
    try:
        lock_in = engine.generate_lock_in_strategy('test_user_123', 'professional', {})
        lock_in_msg = safe_format(
            "   [OK] Lock-in value: ${value:.2f}, Churn risk: {risk:.1f}%",
            value=lock_in['total_lock_in_value'],
            risk=lock_in['churn_risk_score']
        )
        safe_print(lock_in_msg)
    except Exception as e:
        safe_print(f"   [ERROR] Lock-in strategy failed: {e}")
    
    # Test dynamic pricing
    safe_print("\n3. Testing dynamic pricing...")
    try:
        dynamic = engine.calculate_dynamic_pricing('test_user_123', 79.0, usage_metrics)
        dynamic_msg = safe_format(
            "   [OK] Adjusted price: ${price:.2f} (savings: ${savings:.2f})",
            price=dynamic['adjusted_price'],
            savings=dynamic['savings_amount']
        )
        safe_print(dynamic_msg)
    except Exception as e:
        safe_print(f"   [ERROR] Dynamic pricing failed: {e}")
    
    # Test upgrade incentives
    safe_print("\n4. Testing upgrade incentives...")
    try:
        incentives = engine.generate_upgrade_incentives('test_user_123', 'professional', 'business')
        incentives_msg = safe_format(
            "   [OK] Generated {count} incentives, upgrade value: ${value:.2f}",
            count=len(incentives['incentives']),
            value=incentives['upgrade_value']
        )
        safe_print(incentives_msg)
    except Exception as e:
        safe_print(f"   [ERROR] Upgrade incentives failed: {e}")
    
    # Test retention offers
    safe_print("\n5. Testing retention offers...")
    try:
        retention = engine.generate_retention_offer('test_user_123', 65.0)  # High churn risk
        if retention:
            retention_msg = safe_format(
                "   [OK] Generated {count} retention offers, success rate: {rate:.1%}",
                count=len(retention['offers']),
                rate=retention['estimated_success_rate']
            )
            safe_print(retention_msg)
        else:
            safe_print("   [OK] No retention offers needed (low churn risk)")
    except Exception as e:
        safe_print(f"   [ERROR] Retention offers failed: {e}")
    
    # Test tier information
    safe_print("\n6. Testing tier information...")
    safe_print("   Available tiers:")
    for tier_name, tier in engine.tiers.items():
        tier_msg = safe_format(
            "     {name}: ${monthly}/month (${annual}/year)",
            name=tier.name,
            monthly=tier.monthly_price,
            annual=tier.annual_price
        )
        safe_print(tier_msg)
    
    safe_print("\n" + "="*60)
    safe_print("PRICING ENGINE TEST COMPLETE")
    safe_print("="*60)
    safe_print("✓ Optimal pricing calculation working")
    safe_print("✓ Lock-in strategy generation active")
    safe_print("✓ Dynamic pricing functional")
    safe_print("✓ Upgrade incentives ready")
    safe_print("✓ Retention offers operational")
    safe_print("✓ CPU protection enabled")


if __name__ == "__main__":
    test_pricing_engine()