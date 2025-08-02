#!/usr/bin/env python3
"""
OpenRouter Workflow Integration
Seamlessly integrates OpenRouter with the Auto Marketing Workflow
"""

import json
import os
import asyncio
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
from openrouter_config import OpenRouterClient, ModelOptimizer, PromptOptimizer
from cpu_manager import get_cpu_manager

class WorkflowAIEngine:
    """
    AI Engine for workflow agents using OpenRouter
    """
    
    def __init__(self):
        # Load configuration
        self.config = self._load_config()
        
        # Initialize OpenRouter client
        api_key = os.getenv("OPENROUTER_API_KEY")
        self.client = OpenRouterClient(api_key)
        
        # Initialize optimizers
        self.model_optimizer = ModelOptimizer(self.client)
        self.prompt_optimizer = PromptOptimizer()
        
        # Initialize CPU manager
        self.cpu_manager = get_cpu_manager(max_cpu=80.0)
        
        # Agent configurations
        self.agent_configs = self.config["workflow_integration"]["agent_model_mapping"]
        
        # Usage tracking
        self.usage_by_agent = {}
        self.usage_by_phase = {}
        
    def _load_config(self) -> Dict:
        """Load OpenRouter configuration"""
        config_path = Path("C:/Auto Marketing/config/openrouter_settings.json")
        with open(config_path, 'r') as f:
            return json.load(f)
    
    async def process_agent_request(
        self,
        agent_name: str,
        prompt: str,
        context: Dict = None,
        **kwargs
    ) -> Dict:
        """
        Process request for specific agent
        """
        # Check CPU before processing
        self.cpu_manager.wait_for_cpu()
        
        # Get model for agent
        model = self.agent_configs.get(agent_name, "claude-3-sonnet")
        
        # Optimize prompt for model
        optimized_prompt = self.prompt_optimizer.optimize_prompt(prompt, model)
        
        # Prepare messages
        messages = self._prepare_messages(agent_name, optimized_prompt, context)
        
        # Set parameters based on agent type
        params = self._get_agent_parameters(agent_name)
        params.update(kwargs)
        
        # Make API call
        response = await self.client.chat_completion(
            messages=messages,
            model=model,
            **params
        )
        
        # Track usage
        self._track_usage(agent_name, model, response)
        
        # Process response
        return self._process_agent_response(agent_name, response)
    
    def _prepare_messages(
        self,
        agent_name: str,
        prompt: str,
        context: Dict = None
    ) -> List[Dict]:
        """
        Prepare messages for agent
        """
        messages = []
        
        # Add system message based on agent
        system_prompts = {
            "ux-researcher": """You are a UX Research specialist analyzing market opportunities and user needs.
Focus on data-driven insights, user psychology, and market trends.
Provide detailed personas, journey maps, and actionable recommendations.""",
            
            "content-creator": """You are a Content Creation expert generating compelling marketing content.
Create engaging hooks, narratives, and messaging that resonates with target audiences.
Focus on virality, emotional connection, and conversion optimization.""",
            
            "visual-designer": """You are a Visual Design specialist creating stunning marketing visuals.
Design with user experience, brand consistency, and conversion in mind.
Provide detailed specifications and creative direction.""",
            
            "performance-optimizer": """You are a Performance Optimization expert maximizing marketing ROI.
Focus on analytics, A/B testing, conversion optimization, and growth strategies.
Provide data-driven recommendations and measurable success metrics.""",
            
            "platform-specialist": """You are a Platform Optimization specialist for multi-channel marketing.
Understand platform algorithms, best practices, and content optimization.
Create platform-specific strategies that maximize reach and engagement."""
        }
        
        system_prompt = system_prompts.get(agent_name, "You are a helpful marketing assistant.")
        messages.append({"role": "system", "content": system_prompt})
        
        # Add context if provided
        if context:
            context_str = f"Context:\n{json.dumps(context, indent=2)}\n\n"
            messages.append({"role": "user", "content": context_str})
        
        # Add main prompt
        messages.append({"role": "user", "content": prompt})
        
        return messages
    
    def _get_agent_parameters(self, agent_name: str) -> Dict:
        """
        Get optimal parameters for agent
        """
        # Base parameters
        params = {
            "temperature": 0.7,
            "max_tokens": 4096,
            "top_p": 0.9
        }
        
        # Agent-specific adjustments
        if agent_name == "ux-researcher":
            params["temperature"] = 0.5  # More factual
            params["max_tokens"] = 8192  # Longer responses
        elif agent_name == "content-creator":
            params["temperature"] = 0.8  # More creative
            params["presence_penalty"] = 0.2  # Encourage variety
        elif agent_name == "visual-designer":
            params["temperature"] = 0.9  # Very creative
            params["top_p"] = 0.95
        elif agent_name == "performance-optimizer":
            params["temperature"] = 0.3  # Very analytical
            params["max_tokens"] = 4096
        elif agent_name == "platform-specialist":
            params["temperature"] = 0.6  # Balanced
            params["frequency_penalty"] = 0.1
        
        return params
    
    def _process_agent_response(self, agent_name: str, response: Dict) -> Dict:
        """
        Process and structure agent response
        """
        if "error" in response:
            return response
        
        # Extract content
        content = ""
        if "choices" in response and len(response["choices"]) > 0:
            content = response["choices"][0]["message"]["content"]
        
        # Structure based on agent type
        structured = {
            "agent": agent_name,
            "timestamp": datetime.now().isoformat(),
            "content": content,
            "model_used": response.get("model", "unknown"),
            "tokens_used": response.get("usage", {})
        }
        
        # Parse content based on agent
        if agent_name == "ux-researcher":
            structured["parsed"] = self._parse_research_output(content)
        elif agent_name == "content-creator":
            structured["parsed"] = self._parse_content_output(content)
        elif agent_name == "platform-specialist":
            structured["parsed"] = self._parse_platform_output(content)
        
        return structured
    
    def _parse_research_output(self, content: str) -> Dict:
        """Parse UX research output"""
        parsed = {
            "personas": [],
            "insights": [],
            "recommendations": []
        }
        
        # Simple parsing (in production, use more sophisticated parsing)
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            if "persona" in line.lower():
                current_section = "personas"
            elif "insight" in line.lower():
                current_section = "insights"
            elif "recommend" in line.lower():
                current_section = "recommendations"
            elif current_section and line.strip():
                if line.strip().startswith('-') or line.strip().startswith('•'):
                    parsed[current_section].append(line.strip()[1:].strip())
        
        return parsed
    
    def _parse_content_output(self, content: str) -> Dict:
        """Parse content creation output"""
        parsed = {
            "hooks": [],
            "narratives": [],
            "calls_to_action": []
        }
        
        # Extract structured content
        if "hook" in content.lower():
            # Extract hooks
            lines = content.split('\n')
            for line in lines:
                if line.strip() and any(char in line for char in ['1.', '2.', '•', '-']):
                    parsed["hooks"].append(line.strip())
        
        return parsed
    
    def _parse_platform_output(self, content: str) -> Dict:
        """Parse platform optimization output"""
        parsed = {
            "platforms": {},
            "strategies": [],
            "optimizations": []
        }
        
        # Extract platform-specific content
        platforms = ["youtube", "instagram", "tiktok", "linkedin", "facebook", "twitter"]
        for platform in platforms:
            if platform in content.lower():
                parsed["platforms"][platform] = "optimized"
        
        return parsed
    
    def _track_usage(self, agent_name: str, model: str, response: Dict):
        """Track usage statistics"""
        if "usage" not in response:
            return
        
        usage = response["usage"]
        
        # Track by agent
        if agent_name not in self.usage_by_agent:
            self.usage_by_agent[agent_name] = {
                "requests": 0,
                "tokens": 0,
                "cost": 0
            }
        
        self.usage_by_agent[agent_name]["requests"] += 1
        self.usage_by_agent[agent_name]["tokens"] += usage.get("total_tokens", 0)
        
        # Calculate cost
        if model in self.client.models:
            config = self.client.models[model]
            input_cost = (usage.get("prompt_tokens", 0) / 1000) * config.cost_per_1k_input
            output_cost = (usage.get("completion_tokens", 0) / 1000) * config.cost_per_1k_output
            self.usage_by_agent[agent_name]["cost"] += (input_cost + output_cost)
    
    async def process_phase(
        self,
        phase_num: str,
        phase_data: Dict,
        parallel: bool = False
    ) -> Dict:
        """
        Process entire workflow phase
        """
        phase_config = self.config["workflow_integration"]["phase_model_optimization"].get(
            f"phase_{phase_num}", {}
        )
        
        models = phase_config.get("models", ["claude-3-sonnet"])
        use_parallel = phase_config.get("parallel", parallel)
        
        results = {}
        
        if use_parallel:
            # Process in parallel
            tasks = []
            for model in models:
                task = self._process_with_model(model, phase_data)
                tasks.append(task)
            
            responses = await asyncio.gather(*tasks)
            
            # Combine results
            for i, model in enumerate(models):
                results[model] = responses[i]
        else:
            # Process sequentially
            for model in models:
                self.cpu_manager.wait_for_cpu()
                results[model] = await self._process_with_model(model, phase_data)
        
        # Track phase usage
        self.usage_by_phase[f"phase_{phase_num}"] = {
            "models_used": models,
            "parallel": use_parallel,
            "timestamp": datetime.now().isoformat()
        }
        
        return results
    
    async def _process_with_model(self, model: str, data: Dict) -> Dict:
        """Process data with specific model"""
        messages = [
            {"role": "system", "content": "You are a marketing strategist."},
            {"role": "user", "content": json.dumps(data)}
        ]
        
        return await self.client.chat_completion(
            messages=messages,
            model=model,
            temperature=0.7
        )
    
    def get_usage_report(self) -> Dict:
        """Get detailed usage report"""
        total_cost = sum(agent["cost"] for agent in self.usage_by_agent.values())
        total_tokens = sum(agent["tokens"] for agent in self.usage_by_agent.values())
        total_requests = sum(agent["requests"] for agent in self.usage_by_agent.values())
        
        return {
            "summary": {
                "total_cost": f"${total_cost:.4f}",
                "total_tokens": total_tokens,
                "total_requests": total_requests
            },
            "by_agent": self.usage_by_agent,
            "by_phase": self.usage_by_phase,
            "model_usage": self.client.get_usage_stats()
        }


class SmartRouter:
    """
    Intelligent routing for optimal model selection
    """
    
    def __init__(self, engine: WorkflowAIEngine):
        self.engine = engine
        self.routing_history = []
        self.performance_scores = {}
    
    def route_request(
        self,
        request_type: str,
        complexity: str = "medium",
        urgency: str = "normal",
        budget_conscious: bool = False
    ) -> str:
        """
        Route request to optimal model
        """
        # Check task routing configuration
        task_routing = self.engine.config["model_preferences"]["task_routing"]
        
        if request_type in task_routing:
            route_config = task_routing[request_type]
            
            # Select based on urgency and budget
            if urgency == "high" and not budget_conscious:
                model = route_config.get("primary")
            elif budget_conscious:
                model = route_config.get("fallback")
            else:
                model = route_config.get("secondary")
        else:
            # Use optimizer for unknown request types
            model = self.engine.model_optimizer.select_optimal_model(
                task_type=request_type,
                budget_constraint=0.01 if budget_conscious else None,
                speed_requirement="fast" if urgency == "high" else None,
                quality_requirement="high" if complexity == "high" else "medium"
            )
        
        # Track routing decision
        self.routing_history.append({
            "timestamp": datetime.now().isoformat(),
            "request_type": request_type,
            "selected_model": model,
            "factors": {
                "complexity": complexity,
                "urgency": urgency,
                "budget_conscious": budget_conscious
            }
        })
        
        return model
    
    def evaluate_routing_performance(self) -> Dict:
        """
        Evaluate routing decisions and optimize
        """
        if not self.routing_history:
            return {"message": "No routing history available"}
        
        # Analyze routing patterns
        model_counts = {}
        for entry in self.routing_history:
            model = entry["selected_model"]
            model_counts[model] = model_counts.get(model, 0) + 1
        
        # Calculate distribution
        total = len(self.routing_history)
        distribution = {
            model: f"{(count/total)*100:.1f}%"
            for model, count in model_counts.items()
        }
        
        return {
            "total_requests": total,
            "model_distribution": distribution,
            "most_used": max(model_counts, key=model_counts.get),
            "routing_efficiency": self._calculate_efficiency()
        }
    
    def _calculate_efficiency(self) -> float:
        """
        Calculate routing efficiency score
        """
        # Simple efficiency calculation
        # In production, use actual performance metrics
        return 0.85  # 85% efficiency


class BatchProcessor:
    """
    Process multiple requests in batches for efficiency
    """
    
    def __init__(self, engine: WorkflowAIEngine):
        self.engine = engine
        self.batch_size = 5
        self.queue = []
    
    async def add_to_batch(self, request: Dict):
        """Add request to batch queue"""
        self.queue.append(request)
        
        if len(self.queue) >= self.batch_size:
            return await self.process_batch()
        
        return None
    
    async def process_batch(self) -> List[Dict]:
        """Process batch of requests"""
        if not self.queue:
            return []
        
        batch = self.queue[:self.batch_size]
        self.queue = self.queue[self.batch_size:]
        
        # Process in parallel
        tasks = []
        for request in batch:
            task = self.engine.process_agent_request(
                agent_name=request["agent"],
                prompt=request["prompt"],
                context=request.get("context")
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        
        return results
    
    async def flush(self) -> List[Dict]:
        """Process remaining requests"""
        if self.queue:
            return await self.process_batch()
        return []


async def test_workflow_integration():
    """Test OpenRouter workflow integration"""
    print("Testing OpenRouter Workflow Integration...")
    print("="*50)
    
    # Initialize engine
    engine = WorkflowAIEngine()
    
    # Test agent request
    print("\nTest 1: Agent Request")
    response = await engine.process_agent_request(
        agent_name="content-creator",
        prompt="Create 3 viral hooks for a productivity app targeting remote workers",
        context={"audience": "remote workers", "product": "productivity app"}
    )
    
    if "content" in response:
        print(f"✓ Response received from {response.get('model_used', 'unknown')}")
        print(f"  Tokens used: {response.get('tokens_used', {})}")
    
    # Test smart routing
    print("\nTest 2: Smart Routing")
    router = SmartRouter(engine)
    
    scenarios = [
        ("marketing_creative", "high", "normal", False),
        ("data_analysis", "medium", "high", True),
        ("quick_responses", "low", "high", True)
    ]
    
    for req_type, complexity, urgency, budget in scenarios:
        model = router.route_request(req_type, complexity, urgency, budget)
        print(f"  {req_type}: → {model}")
    
    # Test batch processing
    print("\nTest 3: Batch Processing")
    batch_processor = BatchProcessor(engine)
    
    # Add test requests
    test_requests = [
        {"agent": "ux-researcher", "prompt": "Analyze target audience"},
        {"agent": "content-creator", "prompt": "Create campaign tagline"},
        {"agent": "platform-specialist", "prompt": "Optimize for Instagram"}
    ]
    
    for req in test_requests:
        result = await batch_processor.add_to_batch(req)
    
    # Flush remaining
    final_results = await batch_processor.flush()
    print(f"  Processed {len(final_results)} requests in batch")
    
    # Get usage report
    print("\nUsage Report:")
    report = engine.get_usage_report()
    for key, value in report["summary"].items():
        print(f"  {key}: {value}")
    
    print("\n✅ OpenRouter workflow integration test complete!")


if __name__ == "__main__":
    # Run async test
    asyncio.run(test_workflow_integration())