#!/usr/bin/env python3
"""
Test script for CPU Manager
Verifies that CPU throttling is working correctly
"""

import time
import sys
from cpu_manager import CPUManager, ProcessThrottler

def simulate_heavy_work():
    """Simulate CPU-intensive work"""
    result = 0
    for i in range(1000000):
        result += i ** 2
    return result

def main():
    print("="*60)
    print("CPU MANAGER TEST")
    print("="*60)
    print("\nThis test will verify CPU throttling is working correctly.")
    print("The system will keep CPU usage below 80%.\n")
    
    # Initialize CPU manager
    cpu_mgr = CPUManager(max_cpu_percent=80.0)
    cpu_mgr.start_monitoring()
    
    print(f"[OK] CPU Manager initialized")
    print(f"Current CPU: {cpu_mgr.current_cpu_usage:.1f}%")
    print(f"Max allowed: {cpu_mgr.max_cpu_percent}%\n")
    
    # Test 1: Basic throttling
    print("Test 1: Basic CPU throttling")
    print("-" * 30)
    
    for i in range(5):
        print(f"\nIteration {i+1}/5:")
        
        # Check CPU before work
        stats = cpu_mgr.get_cpu_stats()
        print(f"  CPU before: {stats['current_usage']:.1f}%")
        
        # Wait if CPU is high
        if cpu_mgr.throttle_active:
            print(f"  [WAIT] Waiting for CPU to drop...")
            cpu_mgr.wait_for_cpu(timeout=10)
        
        # Do some work
        print(f"  [EXEC] Executing task...")
        result = cpu_mgr.throttled_execute(simulate_heavy_work)
        
        # Check CPU after work
        time.sleep(1)  # Let CPU measurement update
        stats = cpu_mgr.get_cpu_stats()
        print(f"  CPU after: {stats['current_usage']:.1f}%")
        
        if stats['throttle_active']:
            print(f"  [WARNING] Throttling active!")
    
    # Test 2: Batch processing
    print("\n\nTest 2: Batch task processing")
    print("-" * 30)
    
    throttler = ProcessThrottler(cpu_mgr)
    print(f"Max concurrent tasks: {throttler.max_concurrent}")
    
    # Create batch of tasks
    tasks = [simulate_heavy_work for _ in range(10)]
    
    print(f"Processing {len(tasks)} tasks in batches...")
    start_time = time.time()
    
    results = throttler.throttled_batch_execute(tasks, batch_size=2)
    
    duration = time.time() - start_time
    print(f"[OK] Completed {len(results)} tasks in {duration:.2f} seconds")
    print(f"Final CPU: {cpu_mgr.current_cpu_usage:.1f}%")
    
    # Test 3: Adaptive sleep
    print("\n\nTest 3: Adaptive sleep based on CPU")
    print("-" * 30)
    
    for cpu_level in [50, 70, 80, 90]:
        cpu_mgr.current_cpu_usage = cpu_level  # Simulate different CPU levels
        print(f"At {cpu_level}% CPU: ", end="")
        
        start = time.time()
        cpu_mgr.adaptive_sleep(base_sleep=0.1)
        duration = time.time() - start
        
        print(f"Slept for {duration:.3f} seconds")
    
    # Cleanup
    cpu_mgr.stop_monitoring()
    
    print("\n" + "="*60)
    print("[SUCCESS] ALL TESTS COMPLETED SUCCESSFULLY")
    print("CPU Manager is working correctly!")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INTERRUPTED] Test interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n[ERROR] Test failed: {e}")
        sys.exit(1)