#!/usr/bin/env python3
"""
OpenRouter Configuration and Integration Module
Unified API for accessing multiple AI models with intelligent routing
Includes CPU protection and rate limiting
"""

import json
import os
import time
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
from cpu_manager import get_cpu_manager
from dataclasses import dataclass
from enum import Enum
import hashlib
import random

class ModelProvider(Enum):
    """Supported model providers through OpenRouter"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    META = "meta"
    MISTRAL = "mistral"
    PERPLEXITY = "perplexity"
    COHERE = "cohere"
    NOUS = "nous"

@dataclass
class ModelConfig:
    """Configuration for individual AI models"""
    id: str
    provider: ModelProvider
    name: str
    context_window: int
    max_tokens: int
    cost_per_1k_input: float
    cost_per_1k_output: float
    capabilities: List[str]
    speed: str  # fast, medium, slow
    quality: str  # high, medium, low
    best_for: List[str]

class OpenRouterClient:
    """
    Main OpenRouter client for AI model access
    """
    
    def __init__(self, api_key: str = None):
        # API Configuration
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"
        
        # Initialize CPU manager
        self.cpu_manager = get_cpu_manager(max_cpu=80.0)
        
        # Model configurations
        self.models = self._initialize_models()
        
        # Rate limiting
        self.rate_limits = {
            "requests_per_minute": 60,
            "tokens_per_minute": 90000,
            "requests_per_day": 10000
        }
        self.request_history = []
        self.token_usage = []
        
        # Cost tracking
        self.total_cost = 0.0
        self.cost_by_model = {}
        
        # Cache configuration
        self.cache_enabled = True
        self.cache = {}
        self.cache_ttl = 3600  # 1 hour
        
        # Model routing preferences
        self.routing_preferences = {
            "creative": ["claude-3-opus", "gpt-4-turbo", "claude-3-sonnet"],
            "analytical": ["gpt-4", "claude-3-opus", "gemini-pro"],
            "fast": ["gpt-3.5-turbo", "claude-3-haiku", "mistral-7b"],
            "coding": ["claude-3-opus", "gpt-4", "codellama-70b"],
            "vision": ["gpt-4-vision", "claude-3-opus", "gemini-pro-vision"],
            "long_context": ["claude-3-opus", "gpt-4-32k", "claude-2.1"]
        }
        
        # Performance metrics
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "average_latency": 0,
            "cache_hits": 0,
            "total_tokens": 0
        }
    
    def _initialize_models(self) -> Dict[str, ModelConfig]:
        """
        Initialize available model configurations
        """
        models = {
            "claude-3-opus": ModelConfig(
                id="anthropic/claude-3-opus",
                provider=ModelProvider.ANTHROPIC,
                name="Claude 3 Opus",
                context_window=200000,
                max_tokens=4096,
                cost_per_1k_input=0.015,
                cost_per_1k_output=0.075,
                capabilities=["text", "vision", "coding", "analysis"],
                speed="medium",
                quality="high",
                best_for=["complex reasoning", "creative writing", "code generation"]
            ),
            "claude-3-sonnet": ModelConfig(
                id="anthropic/claude-3-sonnet",
                provider=ModelProvider.ANTHROPIC,
                name="Claude 3 Sonnet",
                context_window=200000,
                max_tokens=4096,
                cost_per_1k_input=0.003,
                cost_per_1k_output=0.015,
                capabilities=["text", "vision", "coding"],
                speed="fast",
                quality="high",
                best_for=["balanced tasks", "quick responses", "general purpose"]
            ),
            "claude-3-haiku": ModelConfig(
                id="anthropic/claude-3-haiku",
                provider=ModelProvider.ANTHROPIC,
                name="Claude 3 Haiku",
                context_window=200000,
                max_tokens=4096,
                cost_per_1k_input=0.00025,
                cost_per_1k_output=0.00125,
                capabilities=["text", "fast_processing"],
                speed="very_fast",
                quality="medium",
                best_for=["simple tasks", "high volume", "quick responses"]
            ),
            "gpt-4-turbo": ModelConfig(
                id="openai/gpt-4-turbo",
                provider=ModelProvider.OPENAI,
                name="GPT-4 Turbo",
                context_window=128000,
                max_tokens=4096,
                cost_per_1k_input=0.01,
                cost_per_1k_output=0.03,
                capabilities=["text", "vision", "function_calling"],
                speed="medium",
                quality="high",
                best_for=["reasoning", "math", "structured output"]
            ),
            "gpt-4": ModelConfig(
                id="openai/gpt-4",
                provider=ModelProvider.OPENAI,
                name="GPT-4",
                context_window=8192,
                max_tokens=4096,
                cost_per_1k_input=0.03,
                cost_per_1k_output=0.06,
                capabilities=["text", "analysis"],
                speed="slow",
                quality="high",
                best_for=["complex tasks", "detailed analysis"]
            ),
            "gpt-3.5-turbo": ModelConfig(
                id="openai/gpt-3.5-turbo",
                provider=ModelProvider.OPENAI,
                name="GPT-3.5 Turbo",
                context_window=16384,
                max_tokens=4096,
                cost_per_1k_input=0.0005,
                cost_per_1k_output=0.0015,
                capabilities=["text", "fast_processing"],
                speed="very_fast",
                quality="medium",
                best_for=["simple tasks", "high throughput", "cost efficiency"]
            ),
            "gemini-pro": ModelConfig(
                id="google/gemini-pro",
                provider=ModelProvider.GOOGLE,
                name="Gemini Pro",
                context_window=32000,
                max_tokens=8192,
                cost_per_1k_input=0.00025,
                cost_per_1k_output=0.0005,
                capabilities=["text", "vision", "multimodal"],
                speed="fast",
                quality="high",
                best_for=["multimodal tasks", "long context", "efficiency"]
            ),
            "mistral-medium": ModelConfig(
                id="mistralai/mistral-medium",
                provider=ModelProvider.MISTRAL,
                name="Mistral Medium",
                context_window=32000,
                max_tokens=8192,
                cost_per_1k_input=0.0027,
                cost_per_1k_output=0.0081,
                capabilities=["text", "coding"],
                speed="fast",
                quality="medium",
                best_for=["European languages", "coding", "reasoning"]
            ),
            "llama-3-70b": ModelConfig(
                id="meta-llama/llama-3-70b",
                provider=ModelProvider.META,
                name="Llama 3 70B",
                context_window=8192,
                max_tokens=4096,
                cost_per_1k_input=0.0008,
                cost_per_1k_output=0.0008,
                capabilities=["text", "open_source"],
                speed="medium",
                quality="high",
                best_for=["open source", "customization", "research"]
            ),
            "perplexity-online": ModelConfig(
                id="perplexity/llama-3-sonar-large-32k-online",
                provider=ModelProvider.PERPLEXITY,
                name="Perplexity Online",
                context_window=32000,
                max_tokens=4096,
                cost_per_1k_input=0.001,
                cost_per_1k_output=0.001,
                capabilities=["text", "web_search", "real_time"],
                speed="medium",
                quality="high",
                best_for=["current events", "fact checking", "research"]
            )
        }
        
        return models
    
    async def chat_completion(
        self,
        messages: List[Dict],
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = None,
        stream: bool = False,
        **kwargs
    ) -> Dict:
        """
        Send chat completion request to OpenRouter
        """
        # Check CPU before processing
        self.cpu_manager.wait_for_cpu()
        
        # Check rate limits
        if not self._check_rate_limits():
            return {"error": "Rate limit exceeded. Please wait before retrying."}
        
        # Select best model if not specified
        if not model:
            model = self._select_best_model(messages, kwargs.get("task_type", "general"))
        
        # Get model config
        model_config = self._get_model_config(model)
        if not model_config:
            return {"error": f"Model {model} not found"}
        
        # Check cache
        cache_key = self._generate_cache_key(messages, model, temperature)
        if self.cache_enabled and cache_key in self.cache:
            cached = self.cache[cache_key]
            if self._is_cache_valid(cached):
                self.metrics["cache_hits"] += 1
                return cached["response"]
        
        # Prepare request
        request_data = {
            "model": model_config.id,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens or model_config.max_tokens,
            "stream": stream
        }
        
        # Add optional parameters
        if "top_p" in kwargs:
            request_data["top_p"] = kwargs["top_p"]
        if "frequency_penalty" in kwargs:
            request_data["frequency_penalty"] = kwargs["frequency_penalty"]
        if "presence_penalty" in kwargs:
            request_data["presence_penalty"] = kwargs["presence_penalty"]
        
        # Make API request
        start_time = time.time()
        
        try:
            response = await self._make_api_request(request_data)
            
            # Update metrics
            latency = time.time() - start_time
            self._update_metrics(True, latency, response)
            
            # Calculate and track costs
            self._track_costs(model_config, response)
            
            # Cache response
            if self.cache_enabled:
                self.cache[cache_key] = {
                    "response": response,
                    "timestamp": datetime.now(),
                    "ttl": self.cache_ttl
                }
            
            return response
            
        except Exception as e:
            self._update_metrics(False, time.time() - start_time, None)
            return {"error": str(e)}
    
    async def _make_api_request(self, data: Dict) -> Dict:
        """
        Make async API request to OpenRouter
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://auto-marketing.ai",
            "X-Title": "Auto Marketing Workflow"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/chat/completions",
                json=data,
                headers=headers
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"API Error {response.status}: {error_text}")
    
    def _select_best_model(self, messages: List[Dict], task_type: str) -> str:
        """
        Select the best model based on task requirements
        """
        # Calculate message length
        total_tokens = sum(len(msg.get("content", "").split()) * 1.3 for msg in messages)
        
        # Determine requirements
        needs_vision = any("image" in str(msg.get("content", "")) for msg in messages)
        needs_long_context = total_tokens > 8000
        needs_speed = task_type in ["chat", "simple", "quick"]
        needs_quality = task_type in ["complex", "analysis", "creative"]
        
        # Select based on requirements
        if needs_vision:
            candidates = self.routing_preferences.get("vision", ["gpt-4-vision"])
        elif needs_long_context:
            candidates = self.routing_preferences.get("long_context", ["claude-3-opus"])
        elif needs_speed:
            candidates = self.routing_preferences.get("fast", ["gpt-3.5-turbo"])
        elif needs_quality:
            candidates = self.routing_preferences.get("creative", ["claude-3-opus"])
        else:
            candidates = ["claude-3-sonnet", "gpt-4-turbo", "gemini-pro"]
        
        # Return first available model
        for model_name in candidates:
            if model_name in self.models:
                return model_name
        
        return "gpt-3.5-turbo"  # Fallback
    
    def _get_model_config(self, model_name: str) -> Optional[ModelConfig]:
        """
        Get model configuration by name
        """
        # Handle full model IDs
        if "/" in model_name:
            for config in self.models.values():
                if config.id == model_name:
                    return config
        
        # Handle short names
        return self.models.get(model_name)
    
    def _check_rate_limits(self) -> bool:
        """
        Check if request is within rate limits
        """
        now = datetime.now()
        
        # Check requests per minute
        recent_requests = [
            req for req in self.request_history 
            if (now - req).total_seconds() < 60
        ]
        if len(recent_requests) >= self.rate_limits["requests_per_minute"]:
            return False
        
        # Check tokens per minute
        recent_tokens = sum(
            usage for timestamp, usage in self.token_usage
            if (now - timestamp).total_seconds() < 60
        )
        if recent_tokens >= self.rate_limits["tokens_per_minute"]:
            return False
        
        # Add to history
        self.request_history.append(now)
        
        # Clean old history
        self.request_history = [
            req for req in self.request_history
            if (now - req).total_seconds() < 86400  # Keep 24 hours
        ]
        
        return True
    
    def _generate_cache_key(self, messages: List[Dict], model: str, temperature: float) -> str:
        """
        Generate cache key for request
        """
        content = json.dumps({
            "messages": messages,
            "model": model,
            "temperature": temperature
        }, sort_keys=True)
        
        return hashlib.sha256(content.encode()).hexdigest()
    
    def _is_cache_valid(self, cached_item: Dict) -> bool:
        """
        Check if cached item is still valid
        """
        if not cached_item:
            return False
        
        timestamp = cached_item.get("timestamp")
        ttl = cached_item.get("ttl", self.cache_ttl)
        
        if not timestamp:
            return False
        
        age = (datetime.now() - timestamp).total_seconds()
        return age < ttl
    
    def _update_metrics(self, success: bool, latency: float, response: Optional[Dict]):
        """
        Update performance metrics
        """
        self.metrics["total_requests"] += 1
        
        if success:
            self.metrics["successful_requests"] += 1
            
            # Update average latency
            avg = self.metrics["average_latency"]
            count = self.metrics["successful_requests"]
            self.metrics["average_latency"] = (avg * (count - 1) + latency) / count
            
            # Track tokens
            if response and "usage" in response:
                tokens = response["usage"].get("total_tokens", 0)
                self.metrics["total_tokens"] += tokens
                self.token_usage.append((datetime.now(), tokens))
        else:
            self.metrics["failed_requests"] += 1
    
    def _track_costs(self, model_config: ModelConfig, response: Dict):
        """
        Track API costs
        """
        if not response or "usage" not in response:
            return
        
        usage = response["usage"]
        input_tokens = usage.get("prompt_tokens", 0)
        output_tokens = usage.get("completion_tokens", 0)
        
        # Calculate costs
        input_cost = (input_tokens / 1000) * model_config.cost_per_1k_input
        output_cost = (output_tokens / 1000) * model_config.cost_per_1k_output
        total_cost = input_cost + output_cost
        
        # Update totals
        self.total_cost += total_cost
        
        # Track by model
        model_name = model_config.name
        if model_name not in self.cost_by_model:
            self.cost_by_model[model_name] = 0
        self.cost_by_model[model_name] += total_cost
    
    def get_usage_stats(self) -> Dict:
        """
        Get usage statistics
        """
        return {
            "metrics": self.metrics,
            "total_cost": f"${self.total_cost:.4f}",
            "cost_by_model": {
                model: f"${cost:.4f}" 
                for model, cost in self.cost_by_model.items()
            },
            "cache_hit_rate": (
                self.metrics["cache_hits"] / max(self.metrics["total_requests"], 1)
            ) * 100,
            "success_rate": (
                self.metrics["successful_requests"] / max(self.metrics["total_requests"], 1)
            ) * 100,
            "average_latency": f"{self.metrics['average_latency']:.2f}s"
        }
    
    def clear_cache(self):
        """
        Clear response cache
        """
        self.cache.clear()
        print("Cache cleared")
    
    def set_routing_preference(self, task_type: str, models: List[str]):
        """
        Set model routing preference for task type
        """
        self.routing_preferences[task_type] = models
        print(f"Routing preference for {task_type} updated")


class ModelOptimizer:
    """
    Optimize model selection based on performance and cost
    """
    
    def __init__(self, client: OpenRouterClient):
        self.client = client
        self.performance_history = {}
        
    def select_optimal_model(
        self,
        task_type: str,
        budget_constraint: float = None,
        speed_requirement: str = None,
        quality_requirement: str = None
    ) -> str:
        """
        Select optimal model based on constraints
        """
        candidates = []
        
        for model_name, config in self.client.models.items():
            # Check budget constraint
            if budget_constraint:
                avg_cost = (config.cost_per_1k_input + config.cost_per_1k_output) / 2
                if avg_cost > budget_constraint:
                    continue
            
            # Check speed requirement
            if speed_requirement:
                if speed_requirement == "fast" and config.speed not in ["fast", "very_fast"]:
                    continue
                elif speed_requirement == "medium" and config.speed == "slow":
                    continue
            
            # Check quality requirement
            if quality_requirement:
                if quality_requirement == "high" and config.quality != "high":
                    continue
                elif quality_requirement == "medium" and config.quality == "low":
                    continue
            
            # Check if suitable for task
            if task_type in config.best_for:
                candidates.append((model_name, config, 2))  # Higher priority
            elif any(cap in config.capabilities for cap in ["text", "analysis"]):
                candidates.append((model_name, config, 1))  # Lower priority
        
        if not candidates:
            return "gpt-3.5-turbo"  # Fallback
        
        # Sort by priority and cost
        candidates.sort(key=lambda x: (-x[2], x[1].cost_per_1k_input))
        
        return candidates[0][0]
    
    def benchmark_models(self, test_prompt: str, models: List[str] = None) -> Dict:
        """
        Benchmark multiple models for comparison
        """
        if not models:
            models = ["claude-3-haiku", "gpt-3.5-turbo", "gemini-pro", "mistral-medium"]
        
        results = {}
        
        for model in models:
            if model not in self.client.models:
                continue
            
            config = self.client.models[model]
            
            # Simulate benchmark (in production, make actual API calls)
            results[model] = {
                "model": config.name,
                "latency": random.uniform(0.5, 3.0),
                "quality_score": random.uniform(0.7, 1.0),
                "cost": (config.cost_per_1k_input + config.cost_per_1k_output) / 2,
                "tokens_per_second": random.randint(20, 100)
            }
        
        return results


class PromptOptimizer:
    """
    Optimize prompts for different models
    """
    
    def __init__(self):
        self.optimization_strategies = {
            "claude": self._optimize_for_claude,
            "gpt": self._optimize_for_gpt,
            "gemini": self._optimize_for_gemini,
            "llama": self._optimize_for_llama
        }
    
    def optimize_prompt(self, prompt: str, model_name: str) -> str:
        """
        Optimize prompt for specific model
        """
        # Determine model family
        model_family = self._get_model_family(model_name)
        
        # Apply optimization
        if model_family in self.optimization_strategies:
            return self.optimization_strategies[model_family](prompt)
        
        return prompt
    
    def _get_model_family(self, model_name: str) -> str:
        """
        Determine model family from name
        """
        if "claude" in model_name.lower():
            return "claude"
        elif "gpt" in model_name.lower():
            return "gpt"
        elif "gemini" in model_name.lower():
            return "gemini"
        elif "llama" in model_name.lower():
            return "llama"
        return "generic"
    
    def _optimize_for_claude(self, prompt: str) -> str:
        """
        Optimize prompt for Claude models
        """
        # Claude prefers clear structure and explicit instructions
        optimized = f"""<task>
{prompt}
</task>

Please provide a comprehensive response following these guidelines:
1. Be thorough and detailed
2. Use clear structure and formatting
3. Provide examples where relevant
"""
        return optimized
    
    def _optimize_for_gpt(self, prompt: str) -> str:
        """
        Optimize prompt for GPT models
        """
        # GPT works well with role-based prompts
        optimized = f"""You are an expert assistant. 

Task: {prompt}

Please provide a well-structured response with clear reasoning.
"""
        return optimized
    
    def _optimize_for_gemini(self, prompt: str) -> str:
        """
        Optimize prompt for Gemini models
        """
        # Gemini handles direct instructions well
        optimized = f"""Instructions: {prompt}

Provide a detailed response with:
- Clear explanation
- Relevant examples
- Actionable insights
"""
        return optimized
    
    def _optimize_for_llama(self, prompt: str) -> str:
        """
        Optimize prompt for Llama models
        """
        # Llama responds well to conversational style
        optimized = f"""### Human: {prompt}

### Assistant: I'll help you with that. Let me provide a comprehensive response:
"""
        return optimized


if __name__ == "__main__":
    # Test OpenRouter configuration
    print("Testing OpenRouter Configuration...")
    print("="*50)
    
    # Initialize client (API key would be set in environment)
    client = OpenRouterClient(api_key="your_api_key_here")
    
    # Show available models
    print("\nAvailable Models:")
    for model_name, config in client.models.items():
        print(f"  {config.name}:")
        print(f"    - Context: {config.context_window:,} tokens")
        print(f"    - Cost: ${config.cost_per_1k_input:.4f} input / ${config.cost_per_1k_output:.4f} output")
        print(f"    - Speed: {config.speed}, Quality: {config.quality}")
    
    # Test model selection
    print("\n" + "="*50)
    print("Model Selection Tests:")
    
    optimizer = ModelOptimizer(client)
    
    # Test different scenarios
    scenarios = [
        ("creative", None, "fast", "high"),
        ("analysis", 0.01, "medium", "high"),
        ("simple", 0.001, "fast", None),
        ("coding", None, None, "high")
    ]
    
    for task, budget, speed, quality in scenarios:
        model = optimizer.select_optimal_model(task, budget, speed, quality)
        print(f"\nTask: {task}")
        print(f"  Constraints: Budget=${budget}, Speed={speed}, Quality={quality}")
        print(f"  Selected: {model}")
    
    # Show usage stats
    print("\n" + "="*50)
    print("Usage Statistics:")
    stats = client.get_usage_stats()
    for key, value in stats.items():
        if isinstance(value, dict):
            print(f"\n{key}:")
            for k, v in value.items():
                print(f"  {k}: {v}")
        else:
            print(f"{key}: {value}")
    
    print("\n✅ OpenRouter configuration test complete!")