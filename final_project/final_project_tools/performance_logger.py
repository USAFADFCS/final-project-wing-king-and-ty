"""
Performance Logger and Statistics Module
Tracks and reports scheduling system performance metrics for scientific analysis
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any


class PerformanceLogger:
    """Tracks performance metrics and generates statistical reports."""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.phase_times = {}
        self.schedule_data = None
        self.class_data = None
        self.validation_results = {}
        self.config = {}
        self.benchmark_data = None  # For single-agent comparison
        
    def start_tracking(self):
        """Start performance tracking."""
        self.start_time = time.time()
        
    def end_tracking(self):
        """End performance tracking."""
        self.end_time = time.time()
        
    def track_phase(self, phase_name: str, duration: float):
        """Track duration of a specific phase."""
        self.phase_times[phase_name] = duration
        
    def set_schedule_data(self, schedule: Dict):
        """Store schedule data for analysis."""
        try:
            if isinstance(schedule, str):
                schedule = json.loads(schedule)
            self.schedule_data = schedule
        except:
            self.schedule_data = schedule
            
    def set_class_data(self, classes: Dict):
        """Store class data for analysis."""
        try:
            if isinstance(classes, str):
                classes = json.loads(classes)
            self.class_data = classes
        except:
            self.class_data = classes
            
    def set_validation_results(self, results: Dict):
        """Store validation results."""
        self.validation_results = results
        
    def set_config(self, config: Dict):
        """Store system configuration."""
        self.config = config
    
    def set_benchmark_data(self, benchmark: Dict):
        """Store benchmark data for comparison."""
        self.benchmark_data = benchmark
        
    def calculate_statistics(self) -> Dict[str, Any]:
        """Calculate comprehensive statistics."""
        stats = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "performance": self._calculate_performance_stats(),
            "scheduling": self._calculate_scheduling_stats(),
            "validation": self._calculate_validation_stats(),
            "capacity": self._calculate_capacity_stats(),
            "distribution": self._calculate_distribution_stats(),
        }
        return stats
    
    def _calculate_performance_stats(self) -> Dict:
        """Calculate performance metrics."""
        total_time = self.end_time - self.start_time if self.start_time and self.end_time else 0
        
        return {
            "total_runtime": round(total_time, 3),
            "scheduler_time": round(self.phase_times.get("scheduler", 0), 3),
            "validator_time": round(self.phase_times.get("validator", 0), 3),
            "formatter_time": round(self.phase_times.get("formatter", 0), 3),
            "average_agent_latency": round(sum(self.phase_times.values()) / len(self.phase_times), 3) if self.phase_times else 0,
        }
    
    def _calculate_scheduling_stats(self) -> Dict:
        """Calculate scheduling statistics."""
        if not self.schedule_data:
            return {}
            
        total_students = len(self.schedule_data)
        total_classes_assigned = 0
        classes_per_student = []
        
        for student, days in self.schedule_data.items():
            if not isinstance(days, dict):
                continue
            student_classes = sum(len(classes) for classes in days.values())
            total_classes_assigned += student_classes
            classes_per_student.append(student_classes)
        
        avg_classes = total_classes_assigned / total_students if total_students > 0 else 0
        
        return {
            "total_students": total_students,
            "total_classes_assigned": total_classes_assigned,
            "avg_classes_per_student": round(avg_classes, 2),
            "min_classes_per_student": min(classes_per_student) if classes_per_student else 0,
            "max_classes_per_student": max(classes_per_student) if classes_per_student else 0,
            "target_classes_per_student": self.config.get("classes_per_student", "N/A"),
        }
    
    def _calculate_validation_stats(self) -> Dict:
        """Calculate validation statistics."""
        total_checks = 0
        passed_checks = 0
        failed_checks = []
        
        # Parse validation results
        for check_name, result in self.validation_results.items():
            total_checks += 1
            if isinstance(result, dict):
                if result.get("valid", False):
                    passed_checks += 1
                else:
                    # Store failed check with description
                    failed_checks.append({
                        "name": check_name,
                        "description": result.get("description", "No description"),
                        "details": result
                    })
        
        success_rate = (passed_checks / total_checks * 100) if total_checks > 0 else 0
        
        return {
            "total_validation_checks": total_checks,
            "checks_passed": passed_checks,
            "checks_failed": total_checks - passed_checks,
            "success_rate": round(success_rate, 2),
            "conflicts_detected": len(failed_checks),
            "failed_checks": failed_checks,
        }
    
    def _calculate_capacity_stats(self) -> Dict:
        """Calculate capacity utilization statistics."""
        if not self.schedule_data or not self.class_data:
            return {}
        
        # Count enrollments per class
        enrollments = {}
        for student, days in self.schedule_data.items():
            if not isinstance(days, dict):
                continue
            for day, classes in days.items():
                for class_entry in classes:
                    if isinstance(class_entry, dict):
                        class_name = class_entry.get("class")
                    else:
                        class_name = class_entry
                    
                    if class_name:
                        key = (day, class_name)
                        enrollments[key] = enrollments.get(key, 0) + 1
        
        # Calculate utilization
        total_capacity = 0
        used_capacity = 0
        class_utilizations = []
        
        for day, classes in self.class_data.items():
            for class_name, info in classes.items():
                capacity = info.get("capacity", 0)
                enrolled = enrollments.get((day, class_name), 0)
                
                total_capacity += capacity
                used_capacity += enrolled
                
                if capacity > 0:
                    utilization = (enrolled / capacity) * 100
                    class_utilizations.append(utilization)
        
        overall_utilization = (used_capacity / total_capacity * 100) if total_capacity > 0 else 0
        avg_class_utilization = sum(class_utilizations) / len(class_utilizations) if class_utilizations else 0
        
        return {
            "total_capacity": total_capacity,
            "used_capacity": used_capacity,
            "overall_utilization": round(overall_utilization, 2),
            "avg_class_utilization": round(avg_class_utilization, 2),
            "min_class_utilization": round(min(class_utilizations), 2) if class_utilizations else 0,
            "max_class_utilization": round(max(class_utilizations), 2) if class_utilizations else 0,
            "classes_at_capacity": sum(1 for u in class_utilizations if u >= 100),
            "underutilized_classes": sum(1 for u in class_utilizations if u < 50),
        }
    
    def _calculate_distribution_stats(self) -> Dict:
        """Calculate class distribution statistics."""
        if not self.schedule_data:
            return {}
        
        # Track distribution across days
        day_distribution = {}
        period_distribution = {}
        
        for student, days in self.schedule_data.items():
            if not isinstance(days, dict):
                continue
            for day, classes in days.items():
                day_distribution[day] = day_distribution.get(day, 0) + len(classes)
                
                for class_entry in classes:
                    if isinstance(class_entry, dict) and "period" in class_entry:
                        period = class_entry["period"]
                        period_distribution[period] = period_distribution.get(period, 0) + 1
        
        return {
            "classes_per_day": day_distribution,
            "classes_per_period": period_distribution,
            "most_popular_period": max(period_distribution, key=period_distribution.get) if period_distribution else "N/A",
            "least_popular_period": min(period_distribution, key=period_distribution.get) if period_distribution else "N/A",
        }
    
    def print_report(self):
        """Print comprehensive performance report to console."""
        stats = self.calculate_statistics()
        
        print("\n" + "=" * 80)
        print("📊 SCHEDULING SYSTEM PERFORMANCE REPORT")
        print("=" * 80)
        print(f"Generated: {stats['timestamp']}")
        print()
        
        # Performance Metrics
        print("⏱️  RUNTIME PERFORMANCE")
        print("-" * 80)
        perf = stats["performance"]
        print(f"  Total Runtime:           {perf['total_runtime']:.3f} seconds")
        print(f"  Scheduler Agent Time:    {perf['scheduler_time']:.3f} seconds")
        print(f"  Validator Agent Time:    {perf['validator_time']:.3f} seconds")
        print(f"  Formatter Agent Time:    {perf['formatter_time']:.3f} seconds")
        print(f"  Average Agent Latency:   {perf['average_agent_latency']:.3f} seconds")
        print()
        
        # Scheduling Statistics
        print("📅 SCHEDULING STATISTICS")
        print("-" * 80)
        sched = stats["scheduling"]
        print(f"  Students Scheduled:      {sched.get('total_students', 'N/A')}")
        print(f"  Total Classes Assigned:  {sched.get('total_classes_assigned', 'N/A')}")
        print(f"  Avg Classes/Student:     {sched.get('avg_classes_per_student', 'N/A')}")
        print(f"  Min Classes/Student:     {sched.get('min_classes_per_student', 'N/A')}")
        print(f"  Max Classes/Student:     {sched.get('max_classes_per_student', 'N/A')}")
        print(f"  Target Classes/Student:  {sched.get('target_classes_per_student', 'N/A')}")
        print()
        
        # Validation Results
        print("✅ VALIDATION RESULTS")
        print("-" * 80)
        val = stats["validation"]
        print(f"  Total Validation Checks: {val.get('total_validation_checks', 'N/A')}")
        print(f"  Checks Passed:           {val.get('checks_passed', 'N/A')}")
        print(f"  Checks Failed:           {val.get('checks_failed', 'N/A')}")
        print(f"  Success Rate:            {val.get('success_rate', 'N/A')}%")
        print(f"  Conflicts Detected:      {val.get('conflicts_detected', 'N/A')}")
        
        # Show detailed information about failed checks
        if val.get('failed_checks'):
            print("\n  ❌ FAILED CHECKS:")
            for failed in val['failed_checks']:
                print(f"     • {failed['name']}: {failed['description']}")
                if failed.get('details'):
                    for key, value in failed['details'].items():
                        if key not in ['valid', 'description']:
                            print(f"       - {key}: {value}")
        print()
        
        # Capacity Utilization
        print("📊 CAPACITY UTILIZATION")
        print("-" * 80)
        cap = stats["capacity"]
        print(f"  Total Capacity:          {cap.get('total_capacity', 'N/A')} seats")
        print(f"  Used Capacity:           {cap.get('used_capacity', 'N/A')} seats")
        print(f"  Overall Utilization:     {cap.get('overall_utilization', 'N/A')}%")
        print(f"  Avg Class Utilization:   {cap.get('avg_class_utilization', 'N/A')}%")
        print(f"  Min Class Utilization:   {cap.get('min_class_utilization', 'N/A')}%")
        print(f"  Max Class Utilization:   {cap.get('max_class_utilization', 'N/A')}%")
        print(f"  Classes at Capacity:     {cap.get('classes_at_capacity', 'N/A')}")
        print(f"  Underutilized (<50%):    {cap.get('underutilized_classes', 'N/A')}")
        print()
        
        # Distribution Statistics
        print("📈 DISTRIBUTION ANALYSIS")
        print("-" * 80)
        dist = stats["distribution"]
        if dist.get('classes_per_day'):
            print("  Classes per Day:")
            for day, count in sorted(dist['classes_per_day'].items()):
                print(f"    {day}: {count} classes")
        if dist.get('classes_per_period'):
            print("  Classes per Period:")
            period_counts = sorted(dist['classes_per_period'].items())
            for period, count in period_counts[:5]:  # Show top 5
                print(f"    Period {period}: {count} classes")
            if len(period_counts) > 5:
                print(f"    ... and {len(period_counts) - 5} more periods")
        print(f"  Most Popular Period:     Period {dist.get('most_popular_period', 'N/A')}")
        print(f"  Least Popular Period:    Period {dist.get('least_popular_period', 'N/A')}")
        print()
        
        # System Configuration
        print("⚙️  SYSTEM CONFIGURATION")
        print("-" * 80)
        print(f"  Number of Students:      {self.config.get('num_students', 'N/A')}")
        print(f"  Classes per Student:     {self.config.get('classes_per_student', 'N/A')}")
        print(f"  Number of Days:          {self.config.get('num_days', 'N/A')}")
        print(f"  Periods per Day:         {self.config.get('periods_per_day', 'N/A')}")
        print(f"  Min Classes per Day:     {self.config.get('min_classes_per_day', 'N/A')}")
        print()
        
        # Benchmark Comparison (if available)
        if self.benchmark_data:
            print("🏁 BENCHMARK: Multi-Agent vs Single-Agent")
            print("-" * 80)
            bench = self.benchmark_data
            multi_time = perf['total_runtime']
            single_time = bench.get('runtime', 0)
            
            print(f"  Multi-Agent Runtime:     {multi_time:.3f} seconds")
            print(f"  Single-Agent Runtime:    {single_time:.3f} seconds")
            
            if single_time > 0:
                speedup = single_time / multi_time if multi_time > 0 else 0
                diff = abs(multi_time - single_time)
                faster = "Multi-Agent" if multi_time < single_time else "Single-Agent"
                print(f"  Difference:              {diff:.3f} seconds")
                print(f"  Faster System:           {faster}")
                if speedup > 1:
                    print(f"  Speedup Factor:          {speedup:.2f}x")
                else:
                    print(f"  Slowdown Factor:         {1/speedup:.2f}x" if speedup > 0 else "N/A")
            
            # Success rate comparison
            multi_success = val.get('success_rate', 0)
            single_success = bench.get('success_rate', 0)
            print(f"\n  Multi-Agent Success:     {multi_success}%")
            print(f"  Single-Agent Success:    {single_success}%")
            
            print(f"\n  💡 INSIGHTS:")
            if multi_time < single_time:
                print(f"     • Multi-agent system is {diff:.2f}s faster")
                print(f"     • Parallel agent processing provides efficiency gains")
            elif multi_time > single_time:
                print(f"     • Single-agent system is {diff:.2f}s faster") 
                print(f"     • Coordination overhead impacts multi-agent performance")
            else:
                print(f"     • Both systems have similar performance")
            
            if multi_success == single_success == 100:
                print(f"     • Both systems achieve perfect validation")
            elif multi_success > single_success:
                print(f"     • Multi-agent has {multi_success - single_success}% better success rate")
            elif single_success > multi_success:
                print(f"     • Single-agent has {single_success - multi_success}% better success rate")
            
            print()
        
        print("=" * 80)
        print("✨ Report generated successfully - Ready for scientific analysis!")
        print("=" * 80)
        print()
    
    def export_json(self, filename: str = None):
        """Export statistics as JSON for further analysis."""
        if filename is None:
            filename = f"schedule_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        stats = self.calculate_statistics()
        
        with open(filename, 'w') as f:
            json.dump(stats, f, indent=2)
        
        print(f"📁 Statistics exported to: {filename}")
        return filename

