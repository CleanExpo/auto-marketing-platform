#!/usr/bin/env python3
"""
CPU Management Module for Auto Marketing Workflow
Ensures CPU usage stays below 80% to prevent system shutdowns
"""

import psutil
import time
import threading
from typing import Optional, Callable
import logging

class CPUManager:
    """
    Manages CPU usage to keep it below threshold
    """
    
    def __init__(self, max_cpu_percent: float = 80.0, check_interval: float = 1.0):
        """
        Initialize CPU Manager
        
        Args:
            max_cpu_percent: Maximum allowed CPU usage percentage (default 80%)
            check_interval: How often to check CPU usage in seconds
        """
        self.max_cpu_percent = max_cpu_percent
        self.check_interval = check_interval
        self.monitoring = False
        self.current_cpu_usage = 0.0
        self.throttle_active = False
        self.monitor_thread = None
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def start_monitoring(self):
        """Start CPU monitoring in background thread"""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self._monitor_cpu, daemon=True)
            self.monitor_thread.start()
            self.logger.info(f"CPU monitoring started (max: {self.max_cpu_percent}%)")
    
    def stop_monitoring(self):
        """Stop CPU monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        self.logger.info("CPU monitoring stopped")
    
    def _monitor_cpu(self):
        """Background thread to monitor CPU usage"""
        while self.monitoring:
            # Get CPU usage over 1 second interval
            self.current_cpu_usage = psutil.cpu_percent(interval=1)
            
            if self.current_cpu_usage >= self.max_cpu_percent:
                self.throttle_active = True
                self.logger.warning(f"CPU usage high: {self.current_cpu_usage:.1f}% - Throttling active")
            else:
                if self.throttle_active:
                    self.logger.info(f"CPU usage normal: {self.current_cpu_usage:.1f}% - Throttling disabled")
                self.throttle_active = False
            
            time.sleep(self.check_interval)
    
    def wait_for_cpu(self, timeout: Optional[float] = None):
        """
        Wait until CPU usage is below threshold
        
        Args:
            timeout: Maximum time to wait in seconds (None = infinite)
        
        Returns:
            True if CPU is below threshold, False if timeout
        """
        start_time = time.time()
        
        while self.throttle_active:
            if timeout and (time.time() - start_time) >= timeout:
                return False
            
            # Progressive sleep based on how high CPU is
            excess = self.current_cpu_usage - self.max_cpu_percent
            if excess > 20:
                sleep_time = 2.0
            elif excess > 10:
                sleep_time = 1.0
            else:
                sleep_time = 0.5
            
            self.logger.info(f"Waiting for CPU to drop below {self.max_cpu_percent}% (current: {self.current_cpu_usage:.1f}%)")
            time.sleep(sleep_time)
        
        return True
    
    def throttled_execute(self, func: Callable, *args, **kwargs):
        """
        Execute a function with CPU throttling
        
        Args:
            func: Function to execute
            *args: Arguments for the function
            **kwargs: Keyword arguments for the function
        
        Returns:
            Result of the function
        """
        # Wait for CPU if needed
        self.wait_for_cpu()
        
        # Execute function
        result = func(*args, **kwargs)
        
        # Brief pause to prevent CPU spikes
        time.sleep(0.1)
        
        return result
    
    def get_cpu_stats(self) -> dict:
        """Get current CPU statistics"""
        return {
            "current_usage": self.current_cpu_usage,
            "max_allowed": self.max_cpu_percent,
            "throttle_active": self.throttle_active,
            "cpu_count": psutil.cpu_count(),
            "cpu_freq": psutil.cpu_freq().current if psutil.cpu_freq() else None
        }
    
    def adaptive_sleep(self, base_sleep: float = 0.1):
        """
        Sleep for an adaptive duration based on CPU usage
        
        Args:
            base_sleep: Base sleep duration in seconds
        """
        if self.current_cpu_usage > 90:
            sleep_time = base_sleep * 3
        elif self.current_cpu_usage > 80:
            sleep_time = base_sleep * 2
        elif self.current_cpu_usage > 70:
            sleep_time = base_sleep * 1.5
        else:
            sleep_time = base_sleep
        
        time.sleep(sleep_time)
    
    def __enter__(self):
        """Context manager entry"""
        self.start_monitoring()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop_monitoring()


class ProcessThrottler:
    """
    Throttles process execution to manage CPU usage
    """
    
    def __init__(self, cpu_manager: CPUManager):
        self.cpu_manager = cpu_manager
        self.process_count = 0
        self.max_concurrent = self._calculate_max_concurrent()
    
    def _calculate_max_concurrent(self) -> int:
        """Calculate maximum concurrent processes based on CPU cores"""
        cpu_count = psutil.cpu_count()
        # Allow 50% of cores to be used concurrently
        return max(1, cpu_count // 2)
    
    def can_start_process(self) -> bool:
        """Check if a new process can be started"""
        return (self.process_count < self.max_concurrent and 
                not self.cpu_manager.throttle_active)
    
    def start_process(self):
        """Register a process start"""
        self.cpu_manager.wait_for_cpu()
        self.process_count += 1
    
    def end_process(self):
        """Register a process end"""
        self.process_count = max(0, self.process_count - 1)
    
    def throttled_batch_execute(self, tasks: list, batch_size: Optional[int] = None):
        """
        Execute tasks in batches with CPU throttling
        
        Args:
            tasks: List of callable tasks
            batch_size: Number of tasks per batch (None = auto)
        """
        if batch_size is None:
            batch_size = self.max_concurrent
        
        results = []
        for i in range(0, len(tasks), batch_size):
            batch = tasks[i:i + batch_size]
            
            # Wait for CPU before starting batch
            self.cpu_manager.wait_for_cpu()
            
            # Execute batch
            for task in batch:
                if callable(task):
                    result = task()
                    results.append(result)
                    # Small pause between tasks
                    self.cpu_manager.adaptive_sleep(0.2)
            
            # Longer pause between batches
            self.cpu_manager.adaptive_sleep(1.0)
        
        return results


# Singleton instance for global usage
_cpu_manager = None

def get_cpu_manager(max_cpu: float = 80.0) -> CPUManager:
    """Get or create the global CPU manager instance"""
    global _cpu_manager
    if _cpu_manager is None:
        _cpu_manager = CPUManager(max_cpu)
        _cpu_manager.start_monitoring()
    return _cpu_manager


if __name__ == "__main__":
    # Test the CPU manager
    print("Testing CPU Manager...")
    
    with CPUManager(max_cpu_percent=80) as cpu_mgr:
        print(f"Initial CPU stats: {cpu_mgr.get_cpu_stats()}")
        
        # Simulate some work
        for i in range(5):
            cpu_mgr.wait_for_cpu()
            print(f"Iteration {i+1}: CPU at {cpu_mgr.current_cpu_usage:.1f}%")
            time.sleep(2)
        
        print(f"Final CPU stats: {cpu_mgr.get_cpu_stats()}")